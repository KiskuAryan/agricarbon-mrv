"""
AgriCarbon-MRV Financial & Business Planning Model.
Calculates project unit economics, smallholder benefit-sharing,
5-year scaling cash flows, and exports an automated multi-tab Excel model.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


@dataclass
class FinancialAssumptions:
    """Commercial assumptions for rice paddy carbon credit development."""
    credit_price_jpy: float = 3500.0         # J-Credit / Tokyo voluntary offtake price (¥/tCO2e)
    usd_to_jpy_rate: float = 155.0           # Currency exchange rate
    farmer_revenue_share_pct: float = 0.55   # 55% distributed to smallholder farmers
    
    # OPEX parameters per hectare per season
    ground_mrv_cost_per_ha_usd: float = 4.50 # Ground Pani-pipe monitoring & field audits
    remote_sensing_per_ha_usd: float = 1.50  # Sentinel-1 SAR & Sentinel-2 cloud analytics
    local_coop_mgmt_per_ha_usd: float = 3.00 # Cooperative administration & outreach
    
    # Registry & Validation fees
    vvb_audit_fixed_cost_usd: float = 20000.0        # Third-party VVB validation audit fee
    registry_issuance_fee_per_credit_usd: float = 0.25 # Registry credit issuance fee (Verra/J-Credit)
    
    # Agronomic calendar
    seasons_per_year: int = 2                # Double-cropping (Wet & Dry seasons / Kharif & Rabi)


class AgriCarbonFinancialModel:
    """
    Evaluates commercial feasibility, smallholder community cash flows,
    and institutional investor returns for carbon credit projects.
    """

    def __init__(self, assumptions: Optional[FinancialAssumptions] = None):
        self.assumptions = assumptions or FinancialAssumptions()

    def evaluate_season_economics(self, portfolio_df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculates unit economics for a single cropping season across the portfolio.
        """
        total_ha = float(portfolio_df["hectares"].sum())
        total_net_credits = float(portfolio_df["net_credits_issued_tco2e"].sum())
        total_farmers = int(portfolio_df["num_smallholders"].sum())
        
        # Credit price in USD
        credit_price_usd = self.assumptions.credit_price_jpy / self.assumptions.usd_to_jpy_rate
        
        # Gross Revenues
        gross_revenue_jpy = total_net_credits * self.assumptions.credit_price_jpy
        gross_revenue_usd = total_net_credits * credit_price_usd
        
        # Farmer Community Benefit Sharing (55%)
        farmer_payout_usd = gross_revenue_usd * self.assumptions.farmer_revenue_share_pct
        farmer_payout_jpy = gross_revenue_jpy * self.assumptions.farmer_revenue_share_pct
        farmer_income_uplift_usd = farmer_payout_usd / total_farmers if total_farmers > 0 else 0.0
        
        # Operational Costs (USD)
        ground_mrv_usd = total_ha * self.assumptions.ground_mrv_cost_per_ha_usd
        remote_sensing_usd = total_ha * self.assumptions.remote_sensing_per_ha_usd
        coop_mgmt_usd = total_ha * self.assumptions.local_coop_mgmt_per_ha_usd
        variable_opex_usd = ground_mrv_usd + remote_sensing_usd + coop_mgmt_usd
        
        registry_fees_usd = total_net_credits * self.assumptions.registry_issuance_fee_per_credit_usd
        vvb_audit_usd = self.assumptions.vvb_audit_fixed_cost_usd
        
        total_opex_usd = variable_opex_usd + registry_fees_usd + vvb_audit_usd
        total_opex_jpy = total_opex_usd * self.assumptions.usd_to_jpy_rate
        
        # Developer Operating Profit (EBITDA)
        developer_ebitda_usd = gross_revenue_usd - farmer_payout_usd - total_opex_usd
        developer_ebitda_jpy = developer_ebitda_usd * self.assumptions.usd_to_jpy_rate
        ebitda_margin_pct = (developer_ebitda_usd / gross_revenue_usd * 100.0) if gross_revenue_usd > 0 else 0.0

        return {
            "total_hectares": total_ha,
            "total_farmers": total_farmers,
            "total_net_credits_tco2e": total_net_credits,
            "credits_per_hectare": round(total_net_credits / total_ha, 2),
            "credit_price_jpy": self.assumptions.credit_price_jpy,
            "credit_price_usd": round(credit_price_usd, 2),
            "gross_revenue_jpy": round(gross_revenue_jpy, 0),
            "gross_revenue_usd": round(gross_revenue_usd, 0),
            "farmer_payout_jpy": round(farmer_payout_jpy, 0),
            "farmer_payout_usd": round(farmer_payout_usd, 0),
            "farmer_income_uplift_usd": round(farmer_income_uplift_usd, 2),
            "variable_opex_usd": round(variable_opex_usd, 0),
            "fixed_audit_and_registry_usd": round(registry_fees_usd + vvb_audit_usd, 0),
            "total_opex_usd": round(total_opex_usd, 0),
            "total_opex_jpy": round(total_opex_jpy, 0),
            "developer_ebitda_usd": round(developer_ebitda_usd, 0),
            "developer_ebitda_jpy": round(developer_ebitda_jpy, 0),
            "ebitda_margin_pct": round(ebitda_margin_pct, 1),
            "annual_gross_revenue_usd": round(gross_revenue_usd * self.assumptions.seasons_per_year, 0),
            "annual_ebitda_usd": round(developer_ebitda_usd * self.assumptions.seasons_per_year, 0)
        }

    def generate_5year_projection(self, base_metrics: Dict[str, float]) -> pd.DataFrame:
        """
        Generates a 5-year scaling trajectory with economies of scale.
        """
        growth_factors = [1.0, 1.8, 3.2, 5.0, 7.5]
        records = []
        cumulative_cash_usd = 0.0

        for yr_idx, factor in enumerate(growth_factors, start=1):
            ha = int(base_metrics["total_hectares"] * factor)
            credits = round(base_metrics["total_net_credits_tco2e"] * factor, 0)
            rev_usd = round(base_metrics["gross_revenue_usd"] * factor * self.assumptions.seasons_per_year, 0)
            farmer_usd = round(base_metrics["farmer_payout_usd"] * factor * self.assumptions.seasons_per_year, 0)
            
            # Unit OPEX decreases by up to 25% with scale (satellite automation)
            scale_factor = max(0.75, 1.0 - (yr_idx - 1) * 0.06)
            opex_usd = round(base_metrics["total_opex_usd"] * factor * self.assumptions.seasons_per_year * scale_factor, 0)
            
            ebitda_usd = rev_usd - farmer_usd - opex_usd
            cumulative_cash_usd += ebitda_usd

            records.append({
                "Year": f"Year {yr_idx}",
                "Aggregated Area (ha)": ha,
                "Annual Credits (tCO2e)": credits * self.assumptions.seasons_per_year,
                "Annual Gross Revenue (USD)": rev_usd,
                "Annual Gross Revenue (JPY)": round(rev_usd * self.assumptions.usd_to_jpy_rate, 0),
                "Farmer Community Payout (USD)": farmer_usd,
                "Total OPEX & MRV (USD)": opex_usd,
                "Net Developer EBITDA (USD)": ebitda_usd,
                "EBITDA Margin (%)": f"{round((ebitda_usd / rev_usd) * 100, 1)}%",
                "Cumulative Free Cash (USD)": round(cumulative_cash_usd, 0)
            })

        return pd.DataFrame(records)

    def export_excel_model(self, portfolio_df: pd.DataFrame, file_path: Path):
        """
        Exports a multi-tab, professionally styled financial workbook in Excel.
        """
        base_metrics = self.evaluate_season_economics(portfolio_df)
        proj_5yr = self.generate_5year_projection(base_metrics)

        wb = openpyxl.Workbook()
        
        # Color Palette
        navy_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
        forest_fill = PatternFill(start_color="2D6A4F", end_color="2D6A4F", fill_type="solid")
        
        white_bold_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        title_font = Font(name="Calibri", size=15, bold=True, color="1B365D")
        bold_font = Font(name="Calibri", size=11, bold=True)
        regular_font = Font(name="Calibri", size=11)
        
        thin_border = Border(
            left=Side(style='thin', color='D9D9D9'),
            right=Side(style='thin', color='D9D9D9'),
            top=Side(style='thin', color='D9D9D9'),
            bottom=Side(style='thin', color='D9D9D9')
        )

        # -------------------------------------------------------------
        # TAB 1: Executive Summary & Unit Economics
        # -------------------------------------------------------------
        ws_exec = wb.active
        ws_exec.title = "Executive_Summary"
        ws_exec.views.sheetView[0].showGridLines = True

        ws_exec["B2"] = "AgriCarbon-MRV - Rice Paddy AWD Feasibility & Commercial Model"
        ws_exec["B2"].font = title_font
        ws_exec["B3"] = "Commercial Unit Economics, Smallholder Benefit-Sharing, and Scaling Projections"
        ws_exec["B3"].font = Font(name="Calibri", size=11, italic=True, color="555555")

        summary_rows = [
            ("Project Parameter", "Value", "Currency / Metric"),
            ("Aggregated Smallholder Farm Area", base_metrics["total_hectares"], "Hectares (ha)"),
            ("Participating Smallholder Farmers", base_metrics["total_farmers"], "Smallholder Families"),
            ("Annual Cropping Cycles", self.assumptions.seasons_per_year, "Seasons / Year (Double-Cropping)"),
            ("Net Certified Credits (Single Season)", base_metrics["total_net_credits_tco2e"], "tCO2e / season"),
            ("Average Verified Credit Yield", base_metrics["credits_per_hectare"], "tCO2e / ha / season"),
            ("Carbon Credit Market Price (Tokyo)", self.assumptions.credit_price_jpy, "JPY (¥) / tCO2e"),
            ("Equivalent Market Price (USD)", base_metrics["credit_price_usd"], "USD ($) / tCO2e"),
            ("Seasonal Gross Carbon Revenue (JPY)", base_metrics["gross_revenue_jpy"], "JPY (¥)"),
            ("Seasonal Gross Carbon Revenue (USD)", base_metrics["gross_revenue_usd"], "USD ($)"),
            ("Farmer Community Benefit Share (55%)", base_metrics["farmer_payout_usd"], "USD ($) / season"),
            ("Seasonal Income Uplift per Smallholder", base_metrics["farmer_income_uplift_usd"], "USD ($) / farmer"),
            ("Field MRV & Technology OPEX (USD)", base_metrics["variable_opex_usd"], "USD ($) / season"),
            ("Fixed Validation Audit & Registry Fees", base_metrics["fixed_audit_and_registry_usd"], "USD ($) / season"),
            ("Total Project OPEX (USD)", base_metrics["total_opex_usd"], "USD ($) / season"),
            ("Developer Operating Margin (EBITDA USD)", base_metrics["developer_ebitda_usd"], "USD ($) / season"),
            ("Developer Operating Margin (EBITDA JPY)", base_metrics["developer_ebitda_jpy"], "JPY (¥) / season"),
            ("EBITDA Margin Percentage", f"{base_metrics['ebitda_margin_pct']}%", "% of Gross Revenue"),
            ("Annual Developer EBITDA (2 Seasons)", base_metrics["annual_ebitda_usd"], "USD ($) / year")
        ]

        for r_idx, (param, val, unit) in enumerate(summary_rows, start=5):
            cell_a = ws_exec.cell(row=r_idx, column=2, value=param)
            cell_b = ws_exec.cell(row=r_idx, column=3, value=val)
            cell_c = ws_exec.cell(row=r_idx, column=4, value=unit)

            if r_idx == 5:
                for c in [cell_a, cell_b, cell_c]:
                    c.fill = navy_fill
                    c.font = white_bold_font
            else:
                cell_a.font = regular_font
                cell_b.font = bold_font
                cell_c.font = regular_font
                if "JPY" in str(unit) and isinstance(val, (int, float)):
                    cell_b.number_format = '¥#,##0'
                elif "USD" in str(unit) and isinstance(val, (int, float)):
                    cell_b.number_format = '$#,##0'
                elif isinstance(val, (int, float)):
                    cell_b.number_format = '#,##0.0'
                for c in [cell_a, cell_b, cell_c]:
                    c.border = thin_border

        # -------------------------------------------------------------
        # TAB 2: Cluster Performance Breakdown
        # -------------------------------------------------------------
        ws_clust = wb.create_sheet(title="Cluster_Breakdown")
        ws_clust.views.sheetView[0].showGridLines = True

        clust_cols = [
            "Cluster ID", "Region", "Country", "Hectares", "Farmers", 
            "Compliance %", "Methane Avoided (tCH4)", "N2O Penalty (tCO2e)",
            "Net Credits (tCO2e)", "Yield (t/ha)", "Gross Rev (JPY)", "Farmer Share (USD)"
        ]

        for col_idx, col_name in enumerate(clust_cols, start=1):
            cell = ws_clust.cell(row=2, column=col_idx, value=col_name)
            cell.fill = forest_fill
            cell.font = white_bold_font
            cell.alignment = Alignment(horizontal="center")

        for r_idx, (_, row) in enumerate(portfolio_df.iterrows(), start=3):
            rev_jpy = row["net_credits_issued_tco2e"] * self.assumptions.credit_price_jpy
            f_share_usd = (rev_jpy / self.assumptions.usd_to_jpy_rate) * self.assumptions.farmer_revenue_share_pct
            
            row_data = [
                row["cluster_id"], row["region"], row["country"],
                row["hectares"], row["num_smallholders"],
                f"{row['compliance_rate']*100:.1f}%",
                row["ch4_avoided_ton"], row["n2o_rebound_penalty_tco2e"],
                row["net_credits_issued_tco2e"], row["credits_per_hectare"],
                rev_jpy, f_share_usd
            ]

            for c_idx, val in enumerate(row_data, start=1):
                c = ws_clust.cell(row=r_idx, column=c_idx, value=val)
                c.font = regular_font
                c.border = thin_border
                if c_idx in [4, 5]:
                    c.number_format = '#,##0'
                elif c_idx in [7, 8, 9, 10]:
                    c.number_format = '#,##0.0'
                elif c_idx == 11:
                    c.number_format = '¥#,##0'
                elif c_idx == 12:
                    c.number_format = '$#,##0'

        # -------------------------------------------------------------
        # TAB 3: 5-Year Financial Projection
        # -------------------------------------------------------------
        ws_proj = wb.create_sheet(title="5Year_Scaling_Projection")
        ws_proj.views.sheetView[0].showGridLines = True

        proj_cols = list(proj_5yr.columns)
        for col_idx, col_name in enumerate(proj_cols, start=1):
            cell = ws_proj.cell(row=2, column=col_idx, value=col_name)
            cell.fill = navy_fill
            cell.font = white_bold_font
            cell.alignment = Alignment(horizontal="center")

        for r_idx, (_, row) in enumerate(proj_5yr.iterrows(), start=3):
            for c_idx, col_name in enumerate(proj_cols, start=1):
                c = ws_proj.cell(row=r_idx, column=c_idx, value=row[col_name])
                c.font = regular_font
                c.border = thin_border
                if "JPY" in col_name:
                    c.number_format = '¥#,##0'
                elif "USD" in col_name:
                    c.number_format = '$#,##0'
                elif "ha" in col_name or "tCO2e" in col_name:
                    c.number_format = '#,##0'

        # Auto-adjust column widths
        for ws in [ws_exec, ws_clust, ws_proj]:
            for col in ws.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = get_column_letter(col[0].column)
                ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

        file_path.parent.mkdir(parents=True, exist_ok=True)
        wb.save(file_path)


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from src.methodology_engine import CarbonMethodologyEngine
    
    data_file = Path(__file__).resolve().parent.parent / "data" / "farm_clusters.csv"
    if data_file.exists():
        df_in = pd.read_csv(data_file)
        engine = CarbonMethodologyEngine()
        portfolio_metrics = engine.process_portfolio(df_in)
        
        fin_model = AgriCarbonFinancialModel()
        summary = fin_model.evaluate_season_economics(portfolio_metrics)
        print("=== Financial Feasibility Summary ===")
        print(f"Aggregated Area:        {summary['total_hectares']:,.0f} ha ({summary['total_farmers']:,} farmers)")
        print(f"Seasonal Net Credits:   {summary['total_net_credits_tco2e']:,.1f} tCO2e ({summary['credits_per_hectare']} t/ha)")
        print(f"Gross Seasonal Revenue: JPY {summary['gross_revenue_jpy']:,.0f} (${summary['gross_revenue_usd']:,.0f} USD)")
        print(f"Farmer Payout (55%):    ${summary['farmer_payout_usd']:,.0f} USD (~${summary['farmer_income_uplift_usd']:.1f}/farmer)")
        print(f"Total Project OPEX:     ${summary['total_opex_usd']:,.0f} USD")
        print(f"Developer EBITDA:       ${summary['developer_ebitda_usd']:,.0f} USD ({summary['ebitda_margin_pct']}%)")
        print(f"Annual EBITDA (2 Seas): ${summary['annual_ebitda_usd']:,.0f} USD")
        
        output_excel = Path(__file__).resolve().parent.parent / "outputs" / "AgriCarbon_Financial_Model.xlsx"
        fin_model.export_excel_model(portfolio_metrics, output_excel)
        print(f"Exported Excel financial model -> {output_excel}")
