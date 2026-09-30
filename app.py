"""
AgriCarbon-MRV Minimal Executive Dashboard.
Streamlit application for carbon credit feasibility, MRV accounting, and financial planning.
Designed for Agricultural Carbon Project Planning & MRV workflows.
"""

from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.methodology_engine import CarbonAccountingParams, CarbonMethodologyEngine
from src.financial_model import FinancialAssumptions, AgriCarbonFinancialModel
from src.pdd_generator import generate_pdd_markdown

# Page Configuration - Minimal & Clean
st.set_page_config(
    page_title="AgriCarbon-MRV | Feasibility & Planning",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimal corporate styling
st.markdown("""
<style>
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 8px;
        padding: 16px 20px;
        border: 1px solid #E9ECEF;
    }
    .metric-title {
        font-size: 0.82rem;
        color: #6C757D;
        margin-bottom: 4px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.65rem;
        font-weight: 700;
        color: #1B365D;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #2D6A4F;
        margin-top: 4px;
        font-weight: 500;
    }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.markdown("### 🌾 Project Parameters")
st.sidebar.caption("Commercial & Agronomic Sensitivity Controls:")

# 1. Commercial controls
credit_price_jpy = st.sidebar.slider(
    "Carbon Credit Price (JPY / tCO2e)",
    min_value=2000,
    max_value=6000,
    value=3500,
    step=250,
    help="Current voluntary and J-Credit prices in Tokyo range from ¥3,000 to ¥4,500/tCO2e."
)

farmer_share_pct = st.sidebar.slider(
    "Farmer Community Share (%)",
    min_value=40,
    max_value=75,
    value=55,
    step=5,
    help="Percentage of carbon revenue distributed to participating smallholders."
)

usd_jpy_rate = st.sidebar.number_input(
    "USD/JPY FX Rate",
    value=155.0,
    step=1.0
)

# 2. Agronomic Sensitivity Controls
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔬 Field & Agronomy")
awd_compliance_override = st.sidebar.slider(
    "Target AWD Compliance Rate (%)",
    min_value=60,
    max_value=100,
    value=88,
    step=2,
    help="Field compliance verified by Pani-pipe sensors and Sentinel-1 SAR satellite telemetry."
)

# ----------------- LOAD & PROCESS DATA -----------------
base_dir = Path(__file__).resolve().parent
data_file = base_dir / "data" / "farm_clusters.csv"

if not data_file.exists():
    st.error("Data file not found. Please run generate_data.py first.")
    st.stop()

raw_df = pd.read_csv(data_file)
adjusted_df = raw_df.copy()
# Adjust compliance dynamically based on slider
adjusted_df["compliance_rate"] = (adjusted_df["compliance_rate"] * (awd_compliance_override / 88.0)).clip(0.60, 0.99)

# Execute Methodology Engine
engine = CarbonMethodologyEngine()
portfolio_df = engine.process_portfolio(adjusted_df)

# Execute Financial Model
fin_assumptions = FinancialAssumptions(
    credit_price_jpy=float(credit_price_jpy),
    usd_to_jpy_rate=float(usd_jpy_rate),
    farmer_revenue_share_pct=float(farmer_share_pct) / 100.0
)
fin_model = AgriCarbonFinancialModel(fin_assumptions)
fin_summary = fin_model.evaluate_season_economics(portfolio_df)
proj_5yr = fin_model.generate_5year_projection(fin_summary)

# ----------------- MAIN CONTENT -----------------
st.title("AgriCarbon-MRV : Feasibility & Business Planner")
st.markdown("**Empirical MRV & Commercial Planning Engine** | Smallholder Rice Paddy AWD Methane Abatement")
st.markdown("---")

# Row 1: KPI Ribbon
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Aggregated Farm Area</div>
        <div class="metric-value">{fin_summary['total_hectares']:,.0f} ha</div>
        <div class="metric-sub">{fin_summary['total_farmers']:,} participating smallholders</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Net Certified Credits</div>
        <div class="metric-value">{fin_summary['total_net_credits_tco2e']:,.0f} tCO₂e</div>
        <div class="metric-sub">{fin_summary['credits_per_hectare']:.2f} tCO₂e / ha / season (post-deductions)</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Gross Carbon Revenue</div>
        <div class="metric-value">¥{fin_summary['gross_revenue_jpy']/1e6:.1f}M</div>
        <div class="metric-sub">${fin_summary['gross_revenue_usd']:,.0f} USD (@ ¥{credit_price_jpy:,}/t)</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Smallholder Payout</div>
        <div class="metric-value">${fin_summary['farmer_payout_usd']:,.0f}</div>
        <div class="metric-sub">{farmer_share_pct}% share (~${fin_summary['farmer_income_uplift_usd']:.1f}/farmer/season)</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Row 2: Two Clean Analytical Visualizations
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("1. Emissions Accounting: Baseline vs. AWD Practice")
    fig_emissions = go.Figure()
    
    baseline_tot = portfolio_df["baseline_tco2e"].sum()
    project_tot = portfolio_df["project_tco2e"].sum()
    gross_abatement = portfolio_df["gross_ch4_reduction_tco2e"].sum()
    net_credits_tot = portfolio_df["net_credits_issued_tco2e"].sum()
    
    fig_emissions.add_trace(go.Bar(
        x=["Continuous Flooding (Baseline)", "AWD Practice (Project)", "Gross Abatement", "Certified Credits"],
        y=[baseline_tot, project_tot, gross_abatement, net_credits_tot],
        text=[f"{baseline_tot:,.0f} t", f"{project_tot:,.0f} t", f"{gross_abatement:,.0f} t", f"{net_credits_tot:,.0f} t"],
        textposition="auto",
        marker_color=["#9E9E9E", "#2D6A4F", "#1B365D", "#457B9D"]
    ))
    fig_emissions.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis_title="tCO₂e / season",
        plot_bgcolor="#FAFAFA"
    )
    st.plotly_chart(fig_emissions, use_container_width=True)

with col_chart2:
    st.subheader("2. 5-Year Scaling Cash Flow Projections")
    fig_fin = go.Figure()
    fig_fin.add_trace(go.Bar(
        x=proj_5yr["Year"],
        y=proj_5yr["Annual Gross Revenue (USD)"],
        name="Gross Revenue",
        marker_color="#1B365D"
    ))
    fig_fin.add_trace(go.Bar(
        x=proj_5yr["Year"],
        y=proj_5yr["Farmer Community Payout (USD)"],
        name="Farmer Payout (55%)",
        marker_color="#2D6A4F"
    ))
    fig_fin.add_trace(go.Scatter(
        x=proj_5yr["Year"],
        y=proj_5yr["Net Developer EBITDA (USD)"],
        name="Developer EBITDA",
        mode="lines+markers",
        line=dict(color="#E63946", width=2.5)
    ))
    fig_fin.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis_title="USD ($)",
        barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="#FAFAFA"
    )
    st.plotly_chart(fig_fin, use_container_width=True)

# Row 3: Cluster Performance Table
st.subheader("3. Smallholder Cooperative Telemetry & Verification")
display_cols = [
    "cluster_id", "region", "country", "hectares", "num_smallholders",
    "compliance_rate", "avg_drying_depth_cm", "sentinel1_sar_verification_score",
    "ch4_avoided_ton", "net_credits_issued_tco2e", "credits_per_hectare"
]
table_df = portfolio_df[display_cols].copy()
table_df.columns = [
    "Cluster ID", "Region", "Country", "Area (ha)", "Farmers",
    "Compliance", "Pani-Pipe Depth", "SAR Score", "CH₄ Avoided (t)", "Net Credits (tCO₂e)", "Yield (t/ha)"
]
table_df["Compliance"] = (table_df["Compliance"] * 100).map("{:.1f}%".format)
table_df["Pani-Pipe Depth"] = table_df["Pani-Pipe Depth"].map("-{:.1f} cm".format)
st.dataframe(table_df, use_container_width=True, height=240)

# Row 4: Executive Deliverables & Downloads
st.markdown("---")
st.subheader("4. Deliverables & Documentation")

col_d1, col_d2, col_d3 = st.columns([1, 1, 2])

# Export fresh Excel model
excel_path = base_dir / "outputs" / "AgriCarbon_Financial_Model.xlsx"
fin_model.export_excel_model(portfolio_df, excel_path)

with open(excel_path, "rb") as f:
    excel_bytes = f.read()

# Export fresh PDD Markdown
pdd_path = base_dir / "outputs" / "PDD_Executive_Proposal.md"
metrics_dict = {
    **fin_summary,
    "baseline_tco2e": portfolio_df["baseline_tco2e"].sum(),
    "project_tco2e": portfolio_df["project_tco2e"].sum(),
    "gross_ch4_reduction_tco2e": portfolio_df["gross_ch4_reduction_tco2e"].sum(),
    "n2o_rebound_penalty_tco2e": portfolio_df["n2o_rebound_penalty_tco2e"].sum()
}
generate_pdd_markdown(metrics_dict, pdd_path)

with open(pdd_path, "r", encoding="utf-8") as f:
    pdd_text = f.read()

with col_d1:
    st.download_button(
        label="📥 Download Excel Model (.xlsx)",
        data=excel_bytes,
        file_name="AgriCarbon_Financial_Model.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

with col_d2:
    st.download_button(
        label="📄 Download PDD Proposal (.md)",
        data=pdd_text,
        file_name="PDD_Executive_Proposal.md",
        mime="text/markdown",
        use_container_width=True
    )

with col_d3:
    with st.expander("🔍 Scientific Standard & Verification Details"):
        st.markdown("""
        - **Standard:** Verra Verified Carbon Standard (VCS) & J-Credit Scheme (Japan)
        - **Methodology:** CDM AMS-III.AU (Verra) & AG-001 (J-Credit Agriculture)
        - **GWP Metric:** IPCC AR6 100-year ($GWP_{\\text{CH}_4} = 27.9$)
        - **N2O Rebound Penalty:** 8.0% conservative deduction for aerobic soil nitrification
        - **MRV Telemetry:** In-situ Pani-pipe water table sensors + Sentinel-1 C-Band SAR
        - **Permanence & Risk:** 10.0% pooled buffer reserve + 5.0% uncertainty deduction
        """)
