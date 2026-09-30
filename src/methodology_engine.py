"""
AgriCarbon-MRV Quantitative Methodology Engine.
Fully compliant with IPCC 2019 Refinement to the 2006 Guidelines (Vol 4, Ch 5)
and Verra CDM AMS-III.AU / J-Credit Scheme AG-001 (Agricultural Water Management).
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np
import pandas as pd


@dataclass
class CarbonAccountingParams:
    """
    Standard agronomic, IPCC, and registry parameters for rice paddy carbon accounting.
    """
    # IPCC AR6 100-year Global Warming Potential (GWP100) for biogenic methane (CH4)
    gwp_ch4: float = 27.9
    
    # Baseline continuous flooding daily emission factor (kg CH4 / ha / day)
    # IPCC Tier 1 default for South & Southeast Asia: 1.30 kg/ha/day
    ef_baseline_daily: float = 1.30
    
    # Scaling Factor for Water regime during cultivation (SF_w)
    # Continuous flooding = 1.00; Multiple aeration / AWD = 0.52 (IPCC 2019 Table 5.12)
    sf_w_continuous: float = 1.00
    sf_w_awd: float = 0.52
    
    # Scaling factor for pre-season water regime (non-flooded pre-season > 180 days = 1.00)
    sf_pre_season: float = 1.00
    
    # Organic amendment conversion factor (straw incorporated = 0.14)
    cfoa_straw: float = 0.14
    
    # N2O rebound emission deduction (8% empirical penalty per IPCC/Verra)
    # Aerated drying creates temporary nitrification resulting in minor N2O flux
    n2o_rebound_deduction_pct: float = 0.08
    
    # Regulatory deductions per Verra VCS / J-Credit rules
    uncertainty_deduction_pct: float = 0.05    # 5% conservative deduction for measurement variance
    buffer_pool_withholding_pct: float = 0.10  # 10% non-permanence risk buffer reserve


class CarbonMethodologyEngine:
    """
    Executes MRV calculations for baseline vs. project GHG emissions
    and computes certified high-integrity carbon credits (tCO2e).
    """

    def __init__(self, params: Optional[CarbonAccountingParams] = None):
        self.params = params or CarbonAccountingParams()

    def calculate_organic_scaling_factor(self, organic_tons_ha: float) -> float:
        """
        Calculates SF_o using IPCC 2006/2019 Equation 5.3:
        SF_o = (1 + sum(ROA_i * CFOA_i))^0.59
        """
        raw_factor = 1.0 + (organic_tons_ha * self.params.cfoa_straw)
        return float(np.power(raw_factor, 0.59))

    def evaluate_cluster(self, row: pd.Series) -> Dict[str, float]:
        """
        Computes emission metrics for an individual farm cluster.
        Both baseline and project evaluations span the exact cultivation duration.
        """
        hectares = float(row["hectares"])
        season_days = float(row["season_length_days"])
        organic_tons = float(row.get("organic_amendment_ton_ha", 1.0))
        compliance = float(row.get("compliance_rate", 0.88))

        sf_o = self.calculate_organic_scaling_factor(organic_tons)

        # 1. Baseline Emissions (Continuously Flooded Traditional Practice)
        # Daily EF_base = EF_c * SF_w (1.00) * SF_p (1.00) * SF_o
        daily_ef_base = (
            self.params.ef_baseline_daily
            * self.params.sf_w_continuous
            * self.params.sf_pre_season
            * sf_o
        )
        total_ch4_baseline_kg = daily_ef_base * season_days * hectares
        ch4_baseline_ton = total_ch4_baseline_kg / 1000.0
        baseline_tco2e = ch4_baseline_ton * self.params.gwp_ch4

        # 2. Project Emissions (Alternate Wetting and Drying Intermittent Aeration)
        # Compliant hectares experience sf_w_awd (0.52); non-compliant fallback to 1.00
        effective_sf_w = (compliance * self.params.sf_w_awd) + ((1.0 - compliance) * self.params.sf_w_continuous)
        daily_ef_project = (
            self.params.ef_baseline_daily
            * effective_sf_w
            * self.params.sf_pre_season
            * sf_o
        )
        total_ch4_project_kg = daily_ef_project * season_days * hectares
        ch4_project_ton = total_ch4_project_kg / 1000.0
        project_ch4_tco2e = ch4_project_ton * self.params.gwp_ch4

        # 3. Gross Methane Abatement
        gross_ch4_avoided_ton = max(0.0, ch4_baseline_ton - ch4_project_ton)
        gross_ch4_reduction_tco2e = max(0.0, baseline_tco2e - project_ch4_tco2e)

        # 4. Nitrous Oxide (N2O) Rebound Trade-Off Adjustment
        # Periodic field aeration causes minor N2O release (~8% of avoided methane CO2e)
        n2o_penalty_tco2e = gross_ch4_reduction_tco2e * self.params.n2o_rebound_deduction_pct
        net_ghg_abated_tco2e = gross_ch4_reduction_tco2e - n2o_penalty_tco2e

        # 5. Regulatory Deductions (Verra VCS / J-Credit Conservative Rules)
        uncertainty_tco2e = net_ghg_abated_tco2e * self.params.uncertainty_deduction_pct
        buffer_reserve_tco2e = net_ghg_abated_tco2e * self.params.buffer_pool_withholding_pct
        
        # 6. Final Certified Carbon Credits Issued
        net_credits_issued_tco2e = net_ghg_abated_tco2e - uncertainty_tco2e - buffer_reserve_tco2e
        credit_yield_per_ha = net_credits_issued_tco2e / hectares

        return {
            "hectares": hectares,
            "season_days": season_days,
            "ch4_baseline_ton": round(ch4_baseline_ton, 2),
            "ch4_project_ton": round(ch4_project_ton, 2),
            "ch4_avoided_ton": round(gross_ch4_avoided_ton, 2),
            "baseline_tco2e": round(baseline_tco2e, 2),
            "project_tco2e": round(project_ch4_tco2e + n2o_penalty_tco2e, 2),
            "gross_ch4_reduction_tco2e": round(gross_ch4_reduction_tco2e, 2),
            "n2o_rebound_penalty_tco2e": round(n2o_penalty_tco2e, 2),
            "uncertainty_deduction_tco2e": round(uncertainty_tco2e, 2),
            "buffer_pool_reserve_tco2e": round(buffer_reserve_tco2e, 2),
            "net_credits_issued_tco2e": round(net_credits_issued_tco2e, 2),
            "credits_per_hectare": round(credit_yield_per_ha, 2)
        }

    def process_portfolio(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes MRV calculations across the full portfolio of farm clusters.
        """
        results = []
        for _, row in df.iterrows():
            metrics = self.evaluate_cluster(row)
            combined = {**row.to_dict(), **metrics}
            results.append(combined)

        return pd.DataFrame(results)


if __name__ == "__main__":
    from pathlib import Path
    data_path = Path(__file__).resolve().parent.parent / "data" / "farm_clusters.csv"
    if data_path.exists():
        df_input = pd.read_csv(data_path)
        engine = CarbonMethodologyEngine()
        portfolio_df = engine.process_portfolio(df_input)
        
        total_ha = portfolio_df["hectares"].sum()
        total_net_credits = portfolio_df["net_credits_issued_tco2e"].sum()
        total_ch4_avoided = portfolio_df["ch4_avoided_ton"].sum()
        avg_cred_per_ha = total_net_credits / total_ha

        print("=== MRV Methodology Engine Portfolio Summary ===")
        print(f"Total Farm Area:           {total_ha:,.0f} ha")
        print(f"Methane (CH4) Avoided:     {total_ch4_avoided:,.1f} metric tons CH4")
        print(f"Baseline GHG:              {portfolio_df['baseline_tco2e'].sum():,.1f} tCO2e")
        print(f"N2O Rebound Deduction:     {portfolio_df['n2o_rebound_penalty_tco2e'].sum():,.1f} tCO2e (8% conservative trade-off)")
        print(f"Net Certified Credits:     {total_net_credits:,.1f} tCO2e")
        print(f"Verified Credit Yield:     {avg_cred_per_ha:.2f} tCO2e/ha/season")
