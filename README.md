# 🌱 AgriCarbon-MRV: Rice Paddy Carbon Feasibility & Financial Planning Engine

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![IPCC AR6](https://img.shields.io/badge/Methodology-IPCC%202019%20%2F%20Verra%20AMS--III.AU-2D6A4F)](https://verra.org/)
[![J-Credit AG-001](https://img.shields.io/badge/Standard-J--Credit%20Scheme-1B365D)](https://japancredit.go.jp/)
[![Streamlit](https://img.shields.io/badge/Interactive%20UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Excel Model](https://img.shields.io/badge/Financial%20Model-OpenPyXL%20Automated-217346?logo=microsoftexcel&logoColor=white)](https://github.com/KiskuAryan/agricarbon-mrv)

> **An end-to-end quantitative carbon accounting, MRV (Measurement, Reporting, and Verification), and business feasibility planning engine designed for smallholder agricultural methane abatement (Alternate Wetting and Drying - AWD) across Southeast Asia and India.**
>
> Modeled after high-integrity voluntary and compliance market standards (**Verra VCS CDM AMS-III.AU** and **Japan J-Credit Scheme AG-001**) for agricultural carbon project development, institutional offtake planning, and smallholder benefit-sharing.

---

## 🖥️ Executive Platform Preview

| Interactive Streamlit Planning Engine | Automated OpenPyXL Financial Model |
| :---: | :---: |
| ![Streamlit Planning Engine](assets/dashboard_preview.png) | ![Excel Financial Model](assets/excel_preview.png) |

---

## 📌 Executive Problem Context

Continuous flooding in irrigated rice paddies creates an anoxic (oxygen-depleted) soil environment where methanogenic bacteria decompose organic biomass, emitting large quantities of **Methane ($\text{CH}_4$)**—a greenhouse gas with **27.9× the global warming potential of $\text{CO}_2$** (IPCC AR6). Globally, rice paddies account for **~8–10% of all agricultural greenhouse gas emissions**.

### The Solution: Alternate Wetting and Drying (AWD)
By allowing the field to dry until the water table drops to 15 cm below the soil surface before re-irrigation:
- **Methane Abatement:** Soil aeration introduces atmospheric oxygen, disrupting methanogenesis and cutting seasonal methane emissions by **35% to 50%**.
- **Water Conservation:** Decreases freshwater irrigation demand by **20% to 30%** without reducing crop yields.
- **$\text{N}_2\text{O}$ Accounting:** Incorporates an explicit **8.0% $\text{N}_2\text{O}$ rebound penalty** to account for temporary soil nitrification during aerobic drydowns.
- **Carbon Monetization:** Generated emission reductions are certified into high-integrity carbon credits ($\text{tCO}_2\text{e}$) sold to corporate buyers (e.g., Japanese corporations seeking Scope 3 / ESG offsets), with 55% of revenues shared directly back to smallholder farmers.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Data & Telemetry
        A[25 Smallholder Cooperatives<br>20,689 Hectares] --> B[Ground In-Situ Sensors<br>Pani-Pipe Water Table Telemetry]
        A --> C[Satellite Remote Sensing<br>Sentinel-1 SAR C-Band Radar Backscatter]
    end

    subgraph Quantitative Methodology Engine
        B & C --> D[CarbonMethodologyEngine]
        D --> E[IPCC Tier-2 Equations<br>EF_base vs. EF_project]
        E --> F[Gross Methane Reduction tCO2e]
        F --> G[N2O Rebound Penalty<br>-8.0% Conservative Deduction]
        G --> H[Regulatory Deductions<br>5% Uncertainty + 10% Buffer Pool]
    end

    subgraph Commercial & Business Planner
        H --> I[AgriCarbonFinancialModel]
        I --> J[Carbon Revenue Forecast<br>JPY ¥ & USD $]
        I --> K[Farmer Benefit Share<br>55% Smallholder Payout]
        I --> L[OPEX & MRV Costs<br>Sensors + VVB Audit + Registry]
        I --> M[5-Year Cash Flow & EBITDA]
    end

    subgraph Executive Deliverables
        I --> N[Automated Excel Model<br>.xlsx with Live Formulas]
        H --> O[Project Design Document PDD<br>Executive Proposal]
        I --> P[Minimal Streamlit Dashboard<br>Scenario Planning UI]
    end
```

---

## 🔬 Carbon Accounting & MRV Methodology

The engine calculates net certified emission reductions in accordance with **IPCC 2019 Refinement to the 2006 IPCC Guidelines (Volume 4, Chapter 5)** and **Verra CDM AMS-III.AU**:

### 1. Baseline Emissions ($E_{\text{base}}$)
Under traditional continuous flooding across cultivation duration $t$:
$$E_{\text{base}} = EF_c \times SF_w \times SF_p \times SF_o \times t \times \text{Hectares} \times GWP_{\text{CH}_4} \times 10^{-3}$$

- $EF_c = 1.30 \text{ kg }\text{CH}_4\text{/ha/day}$ (IPCC baseline emission factor for Asia)
- $SF_w = 1.00$ (continuous flooding water regime)
- $SF_p = 1.00$ (non-flooded pre-season $>180$ days)
- $SF_o = (1 + \sum ROA_i \times CFOA_i)^{0.59}$ (organic straw amendments factor, $CFOA = 0.14$)
- $GWP_{\text{CH}_4} = 27.9$ (IPCC AR6 100-year metric)

### 2. Project Emissions ($E_{\text{proj}}$)
With verified AWD field drying cycles:
$$E_{\text{proj}} = EF_c \times SF_{w,\text{eff}} \times SF_p \times SF_o \times t \times \text{Hectares} \times GWP_{\text{CH}_4} \times 10^{-3}$$
Where $SF_{w,\text{eff}} = (\text{Compliance} \times 0.52) + ((1 - \text{Compliance}) \times 1.00)$.

### 3. Net Certified Carbon Credits ($\text{Credits}_{\text{issued}}$)
$$\Delta E_{\text{gross}} = E_{\text{base}} - E_{\text{proj}}$$
$$\Delta E_{\text{net}} = \Delta E_{\text{gross}} \times (1 - \text{Penalty}_{\text{N}_2\text{O}, 8\%})$$
$$\text{Credits}_{\text{issued}} = \Delta E_{\text{net}} \times (1 - \text{Uncertainty}_{5\%}) \times (1 - \text{Buffer Pool}_{10\%})$$

---

## 📊 Portfolio Baseline vs. Project Metrics

| Metric | Single Season Portfolio (25 Cooperatives) | Unit |
| :--- | :--- | :--- |
| **Aggregated Farm Area** | **20,689** | Hectares (ha) |
| **Participating Smallholders** | **14,500+** | Smallholder Families |
| **Gross Methane ($\text{CH}_4$) Avoided** | **1,310.4** | Metric tons $\text{CH}_4$ |
| **Baseline GHG Footprint** | **104,116.8** | $\text{tCO}_2\text{e}$ |
| **Project GHG Footprint (AWD)** | **67,556.7** | $\text{tCO}_2\text{e}$ |
| **Gross Methane Reduction** | **36,560.1** | $\text{tCO}_2\text{e}$ |
| **$\text{N}_2\text{O}$ Rebound Deduction (8%)** | **-2,924.8** | $\text{tCO}_2\text{e}$ |
| **Net Certified Carbon Credits Issued** | **28,758.1** | $\text{tCO}_2\text{e}$ / season |
| **Verified Credit Yield** | **~1.39** | $\text{tCO}_2\text{e}$ / ha / season |

---

## 💼 Business Feasibility & Financial Model

The financial model projects commercial cash flows, unit economics, and benefit-sharing:

- **Carbon Price:** ¥3,500 / $\text{tCO}_2\text{e}$ (~$22.58 USD at 155 JPY/USD).
- **Gross Seasonal Revenue:** **JPY 100,653,350 (~$649,376 USD)**.
- **Smallholder Benefit Sharing (55%):** **$357,157 USD** distributed directly to smallholders (~$25–$30 USD supplementary cash transfer per farming family).
- **MRV & Monitoring Costs:** $4.50/ha ground telemetry + $1.50/ha Sentinel-1 SAR cloud analytics + $3.00/ha local coop management.
- **Registry & Audit Fees:** $20,000 fixed VVB validation audit fee + $0.25/credit issuance fee.
- **Developer Seasonal EBITDA:** **$78,430 USD (+12.1% margin)**.
- **Annual Developer EBITDA (2 Seasons):** **$156,860 USD / year**.

### 5-Year Scaling Projection

| Horizon | Farm Area (ha) | Annual Credits ($\text{tCO}_2\text{e}$) | Gross Revenue (USD) | Farmer Share (USD) | Net EBITDA (USD) | Cumulative Cash (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Year 1** | 20,689 | 57,516 | $1,298,753 | $714,314 | $156,860 | $156,860 |
| **Year 2** | 37,240 | 103,529 | $2,337,755 | $1,285,765 | $356,890 | $513,750 |
| **Year 3** | 66,205 | 184,052 | $4,156,009 | $2,285,805 | $792,440 | $1,306,190 |
| **Year 4** | 103,445 | 287,581 | $6,493,764 | $3,571,570 | $1,475,320 | $2,781,510 |
| **Year 5** | 155,168 | 431,372 | $9,740,646 | $5,357,355 | $2,490,110 | $5,271,620 |

---

## 🚀 Quickstart & Installation

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/KiskuAryan/agricarbon-mrv.git
cd agricarbon-mrv
pip install -r requirements.txt
```

### 2. Run the Quantitative Engines
```bash
# 1. Generate realistic farm cluster telemetry data
python generate_data.py

# 2. Run the IPCC & Verra methodology engine
python -m src.methodology_engine

# 3. Run the commercial financial model and export Excel workbook
python -m src.financial_model

# 4. Generate the formal Project Design Document (PDD) proposal
python -m src.pdd_generator
```

### 3. Launch the Interactive Scenario Planning Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` to test credit pricing sensitivity, AWD compliance rates, and export client deliverables.

---

## 📁 Repository Structure

```
agricarbon-mrv/
├── data/
│   └── farm_clusters.csv               # 25 smallholder cooperatives with agronomic telemetry
├── src/
│   ├── methodology_engine.py          # IPCC AR6 & Verra AMS-III.AU calculation engine
│   ├── financial_model.py             # Unit economics & automated multi-tab Excel generator
│   └── pdd_generator.py               # Formal Project Design Document (PDD) generator
├── outputs/
│   ├── AgriCarbon_Financial_Model.xlsx # Professional Excel model with formatted tabs
│   └── PDD_Executive_Proposal.md       # Client-ready PDD methodology brief
├── app.py                             # Clean, minimal 1-page Streamlit executive dashboard
├── generate_data.py                   # Field telemetry & ground pipe sensor simulator
├── requirements.txt                   # Project dependencies
└── README.md                          # Repository documentation
```

---

## 🎯 Industry & Role Alignment: Carbon Business Planning & Methodology
This project demonstrates the core quantitative, commercial, and technical competencies required in the carbon development & climate finance sector:
1. **Methodology Engineering:** Translating complex technical IPCC (Vol 4, Ch 5) and Verra VCS CDM AMS-III.AU protocols into production-grade mathematical algorithms.
2. **Quantitative Analysis & Excel Financial Modeling:** Building multi-tab, audit-ready financial models with automated currency conversions (JPY/USD), variable field OPEX, and smallholder benefit-sharing.
3. **Institutional Documentation:** Drafting client- and auditor-ready Project Design Documents (PDDs), additionality justifications, and executive briefs.
4. **Strategic Business Planning:** Modeling multi-year project scaling trajectories, farmer retention incentives, and developer EBITDA margins.

---

**Author:** Aryan Manjhi (Integrated M.Tech, Mathematics & Computing, IIT ISM Dhanbad)  
**GitHub:** [github.com/KiskuAryan](https://github.com/KiskuAryan)
