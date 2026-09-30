"""
PDD (Project Design Document) Executive Proposal Generator.
Generates an institutional-grade methodology and commercial proposal
for voluntary and compliance carbon credit creation under Verra AMS-III.AU / J-Credit.
"""

from pathlib import Path
from typing import Dict, Any


def generate_pdd_markdown(metrics: Dict[str, Any], output_path: Path):
    """
    Creates a formal Markdown proposal document ready for executive review.
    """
    total_ha = metrics.get('total_hectares', 21100)
    total_farmers = metrics.get('total_farmers', 14500)
    baseline_tco2e = metrics.get('baseline_tco2e', 98000)
    project_tco2e = metrics.get('project_tco2e', 58000)
    gross_ch4_red = metrics.get('gross_ch4_reduction_tco2e', 40000)
    n2o_penalty = metrics.get('n2o_rebound_penalty_tco2e', 3200)
    net_credits = metrics.get('total_net_credits_tco2e', 31280)
    credit_yield = metrics.get('credits_per_hectare', 1.48)
    gross_rev_jpy = metrics.get('gross_revenue_jpy', 109480000)
    gross_rev_usd = metrics.get('gross_revenue_usd', 706322)
    farmer_payout_usd = metrics.get('farmer_payout_usd', 388477)
    farmer_uplift = metrics.get('farmer_income_uplift_usd', 26.8)
    developer_ebitda = metrics.get('developer_ebitda_usd', 98000)
    ebitda_margin = metrics.get('ebitda_margin_pct', 13.9)

    sections = [
        "# PROJECT DESIGN DOCUMENT (PDD) & METHODOLOGY PROPOSAL",
        "## Smallholder Rice Paddy Methane Abatement & High-Integrity Carbon Credit Creation",
        "**Target Host Geography:** Indo-Gangetic Basin (India) & Southeast Asia (Mekong Delta & Central Luzon)  ",
        "**Standard & Methodology:** Verra VCS (CDM AMS-III.AU) / J-Credit Scheme (AG-001)  ",
        "**Project Developer:** AgriCarbon Project Consortium / Nature-Based Solutions Developer  ",
        "**Lead Quantitative Analyst:** Aryan Manjhi (Integrated B.Tech + M.Tech in IT, ABV-IIITM Gwalior)  ",
        "**Document Classification:** Confidential Commercial Proposal & Methodology Feasibility Brief  ",
        "",
        "---",
        "",
        "### Executive Summary",
        "",
        "| Parameter | Value / Metric | Description |",
        "| :--- | :--- | :--- |",
        "| **Project Type** | Nature-Based Solution (NbS) / Agriculture Methane Avoidance | Alternate Wetting and Drying (AWD) in irrigated rice |",
        f"| **Aggregated Farm Area** | **{total_ha:,.0f} Hectares** | Across 25 smallholder cooperatives |",
        f"| **Participating Smallholders** | **{total_farmers:,} Farmers** | Average landholding of 1.45 ha per family |",
        f"| **Baseline GHG Footprint** | **{baseline_tco2e:,.1f} tCO2e / season** | Continuous flooding practice (anaerobic methanogenesis) |",
        f"| **Gross Methane Reduction** | **{gross_ch4_red:,.1f} tCO2e / season** | Aerated field drydown disrupting methanogens |",
        f"| **N2O Rebound Deduction** | **-{n2o_penalty:,.1f} tCO2e (8.0%)** | Conservative IPCC trade-off deduction for soil aeration |",
        f"| **Net Certified Credits** | **{net_credits:,.1f} tCO2e / season** | Post 5% uncertainty & 10% permanence buffer deductions |",
        f"| **Average Credit Yield** | **{credit_yield:.2f} tCO2e / ha / season** | Fully aligned with empirical IRRI validation benchmarks |",
        f"| **Seasonal Gross Revenue** | **JPY {gross_rev_jpy:,.0f} (~${gross_rev_usd:,.0f} USD)** | Tokyo market valuation @ ¥3,500/credit ($22.58 USD) |",
        f"| **Smallholder Benefit Share** | **55.0% (${farmer_payout_usd:,.0f} USD)** | Direct financial transfers (~${farmer_uplift:.1f}/farmer/season) |",
        f"| **Developer EBITDA** | **${developer_ebitda:,.0f} USD ({ebitda_margin}%)** | Net operating profit after full MRV, audit, and admin |",
        "",
        "---",
        "",
        "### 1. Project Background & Additionality Justification",
        "",
        "#### 1.1 The Baseline Challenge: Rice Paddy Methane Emissions",
        "In traditional irrigated rice agriculture across South and Southeast Asia, fields are continuously submerged under 5 to 10 cm of standing water from transplanting until pre-harvest. This produces anoxic (oxygen-depleted) soil conditions where archaeal methanogens anaerobically decompose organic straw and root exudates, generating large volumes of **Methane (CH4)**.",
        "",
        "Methane possesses a 100-year Global Warming Potential (**GWP100**) of **27.9x CO2** under the IPCC Sixth Assessment Report (AR6). Globally, rice paddies emit approximately 30-35 million metric tons of CH4 annually, accounting for **~8-10% of total agricultural greenhouse gas emissions**.",
        "",
        "#### 1.2 Project Activity: Alternate Wetting and Drying (AWD)",
        "Under the project activity, participating farmers adopt Alternate Wetting and Drying (AWD), an agronomic water-saving protocol engineered by the International Rice Research Institute (IRRI). Rather than continuous submersion, irrigation is paused, allowing the field water table to naturally subside to **15 cm below the soil surface** (monitored via field perforated 'Pani-pipe' tubes) before re-flooding.",
        "",
        "- **Methanogenesis Disruption:** Re-introducing atmospheric oxygen into the topsoil oxidizes methanotrophic bacteria, terminating methane generation during each drying cycle.",
        "- **Empirical Emission Reductions:** Verified continuous field measurements indicate a **35% to 50% net reduction in seasonal methane emissions**.",
        "- **Water Conservation:** Saves **20% to 30% of freshwater irrigation volume**, reducing groundwater depletion and pumping diesel costs.",
        "- **Yield Parity:** Agronomic studies confirm that re-flooding at the -15 cm threshold avoids water stress and maintains 100% grain yield.",
        "",
        "#### 1.3 Additionality Analysis (Tool for the Demonstration and Assessment of Additionality)",
        "- **Investment Barrier:** Smallholders lack capital for monitoring tubes, training, and remote sensing verification infrastructure.",
        "- **Perceived Risk Barrier:** Farmers fear that allowing water to drop below the soil surface will trigger drought stress or reduce harvest weight.",
        "- **Additionality Conclusion:** Carbon finance creates a direct financial incentive (55% revenue share) that offsets risk, provides technical extension services, and makes AWD adoption permanent and verifiable.",
        "",
        "---",
        "",
        "### 2. Methodological GHG Accounting Framework",
        "",
        "The project applies **Verra CDM AMS-III.AU (Version 4.0)** and the **IPCC 2019 Refinement to the 2006 Guidelines for National Greenhouse Gas Inventories (Volume 4, Chapter 5)**:",
        "",
        "```",
        "Baseline CH4 Emissions (kg) = EF_c * SF_w,base * SF_p * SF_o * Days_cultivation * Hectares",
        "Project  CH4 Emissions (kg) = EF_c * SF_w,eff  * SF_p * SF_o * Days_cultivation * Hectares",
        "```",
        "",
        "Where:",
        "- `EF_c` = 1.30 kg CH4/ha/day (IPCC Tier-1 Asian baseline daily emission factor)",
        "- `SF_w,base` = 1.00 (Continuous flooding)",
        "- `SF_w,eff` = [Compliance * 0.52] + [(1 - Compliance) * 1.00] (Multiple aeration AWD factor = 0.52)",
        "- `SF_p` = 1.00 (Non-flooded pre-season > 180 days)",
        "- `SF_o` = (1 + sum(ROA_i * CFOA_i))^0.59 (Organic straw incorporation factor, CFOA = 0.14)",
        "- `GWP_CH4` = 27.9 (IPCC AR6 metric)",
        "",
        "#### Methodological Rigor & Deductions:",
        "1. **Nitrous Oxide (N2O) Rebound Trade-Off (8.0%):** Draining flooded soils can stimulate microbial nitrification-denitrification. To maintain conservatism, an 8% deduction is subtracted from gross methane reductions to account for the N2O trade-off.",
        "2. **Measurement Uncertainty Deduction (5.0%):** Standard Verra conservative deduction for sensor sampling variance.",
        "3. **Buffer Pool Reserve (10.0%):** Deposited into the registry non-permanence risk buffer pool account.",
        "",
        "---",
        "",
        "### 3. Measurement, Reporting, and Verification (MRV) Architecture",
        "",
        "To minimize monitoring costs while satisfying strict VVB (Validation and Verification Body) audit requirements, a hybrid ground-and-satellite MRV architecture is deployed:",
        "",
        "1. **In-Situ 'Pani-Pipe' Telemetry:**",
        "   - Perforated 30-cm PVC tubes installed in sample plots across each 20-hectare grid.",
        "   - Local cooperative field scouts take periodic time-stamped and geo-tagged water level readings via a mobile app to confirm drying depth (-15 cm).",
        "2. **Satellite Remote Sensing (Synthetic Aperture Radar - SAR):**",
        "   - **Sentinel-1 SAR (C-band)** radar penetrates monsoon cloud cover, measuring surface backscatter changes.",
        "   - High backscatter indicates dry/rough soil; low backscatter indicates specular standing water reflections.",
        "   - Automated algorithms verify whether declared AWD drying windows correspond with satellite-detected surface drainage.",
        "3. **Smart Benefit Distribution Ledger:**",
        "   - Once telemetry and SAR data match, compliance is certified, triggering automated direct deposits to smallholder bank or mobile money accounts.",
        "",
        "---",
        "",
        "### 4. Sustainable Development Goals (UN SDGs) & Co-Benefits",
        "",
        "- **SDG 1 (No Poverty):** Directly injects ~$25-$30 supplementary cash per season into rural farming households.",
        "- **SDG 6 (Clean Water and Sanitation):** Conserves up to 3,000 m³ of freshwater per hectare per season.",
        "- **SDG 12 (Responsible Consumption & Production):** Promotes sustainable agronomic water stewardship.",
        f"- **SDG 13 (Climate Action):** Mitigates {net_credits:,.0f} tCO2e of high-potency greenhouse gases per season.",
        "",
        "---",
        "",
        "### 5. Implementation Roadmap & Project Lifecycle",
        "",
        "| Phase | Milestone Description | Duration | Key Deliverables |",
        "| :--- | :--- | :--- | :--- |",
        "| **Phase 1** | Smallholder cooperative onboarding & GIS boundary mapping | Months 1–2 | Signed farmer agreements, digitized polygon shapefiles |",
        "| **Phase 2** | Pani-pipe installation, baseline survey, and scout training | Months 2–3 | Telemetry calibrated, farmer training workshops complete |",
        "| **Phase 3** | Cropping season execution & continuous telemetry monitoring | Months 3–6 | Weekly Pani-pipe logs & Sentinel-1 SAR drydown maps |",
        "| **Phase 4** | Third-party VVB field audit & registry issuance | Months 7–8 | Verification Report & Certified Carbon Credit Issuance |",
        "| **Phase 5** | Offtake settlement with Tokyo corporate buyers & farmer payout | Month 9 | Corporate offtake revenue received & 55% distributed to co-ops |",
        "",
        "*Prepared by: Aryan Manjhi | Quantitative Carbon Project Feasibility & Modeling*",
        ""
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sections))


if __name__ == "__main__":
    import sys
    import pandas as pd
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from src.methodology_engine import CarbonMethodologyEngine
    from src.financial_model import AgriCarbonFinancialModel
    
    data_file = Path(__file__).resolve().parent.parent / "data" / "farm_clusters.csv"
    if data_file.exists():
        df_raw = pd.read_csv(data_file)
        engine = CarbonMethodologyEngine()
        portfolio_df = engine.process_portfolio(df_raw)
        
        fin_model = AgriCarbonFinancialModel()
        fin_summary = fin_model.evaluate_season_economics(portfolio_df)
        
        live_metrics = {
            **fin_summary,
            "baseline_tco2e": portfolio_df["baseline_tco2e"].sum(),
            "project_tco2e": portfolio_df["project_tco2e"].sum(),
            "gross_ch4_reduction_tco2e": portfolio_df["gross_ch4_reduction_tco2e"].sum(),
            "n2o_rebound_penalty_tco2e": portfolio_df["n2o_rebound_penalty_tco2e"].sum()
        }
        
        out_file = Path(__file__).resolve().parent.parent / "outputs" / "PDD_Executive_Proposal.md"
        generate_pdd_markdown(live_metrics, out_file)
        print(f"Generated live-synchronized PDD Executive Proposal -> {out_file}")
