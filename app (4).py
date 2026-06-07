import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Carbon Footprint Tracker",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS THEME ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

    /* Global background */
    .stApp {
        background: linear-gradient(135deg, #0a0f0a 0%, #0d1a0d 40%, #0a1510 100%);
        color: #e0ffe0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #061006 0%, #0a1a0a 100%);
        border-right: 1px solid #1a4d1a;
    }

    /* Main title */
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00ff88, #00cc66, #009944);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: 2px;
        margin-bottom: 0;
        padding-top: 10px;
    }

    .sub-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        color: #66bb6a;
        text-align: center;
        letter-spacing: 4px;
        margin-bottom: 30px;
    }

    /* Section headers */
    .section-header {
        font-family: 'Orbitron', monospace;
        font-size: 1rem;
        color: #00ff88;
        letter-spacing: 3px;
        border-left: 3px solid #00ff88;
        padding-left: 12px;
        margin: 20px 0 15px 0;
        text-transform: uppercase;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #0d2a0d, #0a1f0a);
        border: 1px solid #1a5c1a;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 255, 136, 0.08);
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        border-color: #00ff88;
        box-shadow: 0 4px 30px rgba(0, 255, 136, 0.2);
    }

    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #00ff88;
    }

    .metric-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.85rem;
        color: #66bb6a;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .metric-unit {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.8rem;
        color: #44884;
        color: #448844;
    }

    /* Status badge */
    .status-good {
        background: linear-gradient(90deg, #0a3d0a, #0d520d);
        border: 1px solid #00cc44;
        color: #00ff66;
        padding: 6px 18px;
        border-radius: 20px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
        display: inline-block;
    }

    .status-warning {
        background: linear-gradient(90deg, #3d2e0a, #524000);
        border: 1px solid #ccaa00;
        color: #ffdd00;
        padding: 6px 18px;
        border-radius: 20px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
        display: inline-block;
    }

    .status-danger {
        background: linear-gradient(90deg, #3d0a0a, #520d0d);
        border: 1px solid #cc2200;
        color: #ff4422;
        padding: 6px 18px;
        border-radius: 20px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
        display: inline-block;
    }

    /* Info box */
    .info-box {
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid #1a5c1a;
        border-radius: 10px;
        padding: 15px 20px;
        margin: 10px 0;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.95rem;
        color: #aaffaa;
    }

    /* Team card */
    .team-card {
        background: linear-gradient(135deg, #0d2a0d, #061006);
        border: 1px solid #1a4d1a;
        border-radius: 10px;
        padding: 12px 18px;
        margin: 6px 0;
        font-family: 'Rajdhani', sans-serif;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .team-name {
        color: #ccffcc;
        font-weight: 600;
        font-size: 1rem;
    }

    .team-reg {
        color: #00ff88;
        font-family: 'Orbitron', monospace;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }

    /* Divider */
    .green-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
        margin: 25px 0;
    }

    /* Recommendation box */
    .rec-box {
        background: linear-gradient(135deg, #061a06, #0a260a);
        border-left: 4px solid #00ff88;
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin: 8px 0;
        font-family: 'Rajdhani', sans-serif;
        color: #aaffaa;
        font-size: 1rem;
    }

    /* Streamlit widget labels */
    label, .stSlider label, .stNumberInput label {
        font-family: 'Rajdhani', sans-serif !important;
        color: #88cc88 !important;
        font-size: 0.9rem !important;
        letter-spacing: 1px !important;
    }

    /* Input fields */
    .stNumberInput input {
        background: #0d1a0d !important;
        border: 1px solid #1a5c1a !important;
        color: #00ff88 !important;
        border-radius: 6px !important;
        font-family: 'Rajdhani', sans-serif !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #0d1a0d !important;
        border: 1px solid #1a5c1a !important;
        color: #00ff88 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #061006;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #66bb6a;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        letter-spacing: 2px;
        font-size: 0.85rem;
        border-radius: 8px;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0d3d0d, #1a5c1a) !important;
        color: #00ff88 !important;
        border: 1px solid #00ff88 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0d3d0d, #1a5c1a);
        color: #00ff88;
        border: 1px solid #00ff88;
        border-radius: 8px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
        font-size: 1rem;
        padding: 10px 30px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1a5c1a, #226622);
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
        transform: translateY(-2px);
    }

    /* Footer */
    .footer {
        text-align: center;
        font-family: 'Rajdhani', sans-serif;
        color: #336633;
        font-size: 0.8rem;
        letter-spacing: 2px;
        padding: 20px 0 10px 0;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── EMISSION FACTORS (kg CO2 per unit) ────────────────────────────────────────
EMISSION_FACTORS = {
    "Electricity (kWh)":        0.82,
    "Natural Gas (m³)":         2.00,
    "Diesel Fuel (L)":          2.68,
    "Petrol/Gasoline (L)":      2.31,
    "Coal (kg)":                2.42,
    "LPG (kg)":                 2.98,
    "Furnace Oil (L)":          3.15,
    "Steam (kg)":               0.27,
}

INDUSTRY_BENCHMARKS = {
    "Steel / Metal":      50000,
    "Cement":             80000,
    "Textile":            20000,
    "Chemical":           60000,
    "Food Processing":    15000,
    "Paper / Pulp":       30000,
    "Automotive":         40000,
    "Other / General":    25000,
}

TEAM = [
    ("Muhammad Abdullah", "25-ME-51"),
    ("Syed Talha Umer",   "25-ME-99"),
    ("Muhammad Saad Khan","25-ME-71"),
    ("Ali Zaib",          "25-ME-135"),
    ("Imran Ali",         "25-ME-191"),
]

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-header">🏭 Company Info</div>', unsafe_allow_html=True)
    company_name = st.text_input("Company / Facility Name", value="UET Industries Ltd.")
    industry_type = st.selectbox("Industry Type", list(INDUSTRY_BENCHMARKS.keys()))
    report_period = st.selectbox("Reporting Period", ["Monthly", "Quarterly", "Annually"])
    st.markdown('<hr class="green-divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-header">👥 Project Team</div>', unsafe_allow_html=True)
    for name, reg in TEAM:
        st.markdown(f"""
        <div class="team-card">
            <span class="team-name">🔬 {name}</span>
            <span class="team-reg">{reg}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="green-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Rajdhani',sans-serif; color:#336633; font-size:0.78rem; text-align:center; letter-spacing:1px;">
        ICT for Climate Tech<br>Mechanical Engineering<br>2025
    </div>""", unsafe_allow_html=True)

# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🌍 CARBON FOOTPRINT TRACKER</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">INDUSTRIAL EMISSIONS MONITORING SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<hr class="green-divider">', unsafe_allow_html=True)

# ─── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  CALCULATOR",
    "📈  ANALYTICS",
    "💡  RECOMMENDATIONS",
    "ℹ️  ABOUT"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">⚡ Energy Consumption Inputs</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    inputs = {}

    sources = list(EMISSION_FACTORS.keys())
    half = len(sources) // 2

    with col1:
        for src in sources[:half]:
            unit = src.split("(")[1].replace(")", "")
            inputs[src] = st.number_input(
                f"{src}", min_value=0.0, value=0.0, step=10.0,
                help=f"Enter consumption in {unit}"
            )

    with col2:
        for src in sources[half:]:
            unit = src.split("(")[1].replace(")", "")
            inputs[src] = st.number_input(
                f"{src}", min_value=0.0, value=0.0, step=10.0,
                help=f"Enter consumption in {unit}"
            )

    st.markdown('<hr class="green-divider">', unsafe_allow_html=True)

    # Additional industrial sources
    st.markdown('<div class="section-header">🏗️ Process & Industrial Emissions</div>', unsafe_allow_html=True)
    col3, col4, col5 = st.columns(3)
    with col3:
        waste_tonnes = st.number_input("Industrial Waste (tonnes)", min_value=0.0, value=0.0, step=1.0)
    with col4:
        water_m3 = st.number_input("Water Usage (m³)", min_value=0.0, value=0.0, step=10.0)
    with col5:
        transport_km = st.number_input("Fleet Transport (km)", min_value=0.0, value=0.0, step=50.0)

    st.markdown('<hr class="green-divider">', unsafe_allow_html=True)

    # ── CALCULATE ─────────────────────────────────────────────────────────────
    if st.button("🔬  CALCULATE EMISSIONS", use_container_width=True):
        # Core emissions
        emission_breakdown = {}
        for src, consumption in inputs.items():
            if consumption > 0:
                emission_breakdown[src.split(" (")[0]] = consumption * EMISSION_FACTORS[src]

        # Additional
        if waste_tonnes > 0:
            emission_breakdown["Industrial Waste"] = waste_tonnes * 580
        if water_m3 > 0:
            emission_breakdown["Water Treatment"] = water_m3 * 0.34
        if transport_km > 0:
            emission_breakdown["Fleet Transport"] = transport_km * 0.21

        total_kg   = sum(emission_breakdown.values())
        total_tonnes = total_kg / 1000
        benchmark  = INDUSTRY_BENCHMARKS[industry_type]

        # Multiplier for period
        period_mult = {"Monthly": 1, "Quarterly": 3, "Annually": 12}[report_period]
        annual_est  = total_tonnes * period_mult if report_period != "Annually" else total_tonnes

        # Store in session
        st.session_state["results"] = {
            "breakdown": emission_breakdown,
            "total_kg": total_kg,
            "total_tonnes": total_tonnes,
            "annual_est": annual_est,
            "benchmark": benchmark,
            "industry": industry_type,
            "company": company_name,
            "period": report_period,
        }

        st.markdown('<hr class="green-divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📊 Results</div>', unsafe_allow_html=True)

        # KPI cards
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{total_tonnes:,.1f}</div>
                <div class="metric-unit">tonnes CO₂e</div>
                <div class="metric-label">Total Emissions</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{total_kg:,.0f}</div>
                <div class="metric-unit">kg CO₂e</div>
                <div class="metric-label">In Kilograms</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{annual_est:,.0f}</div>
                <div class="metric-unit">tonnes CO₂e/yr</div>
                <div class="metric-label">Annual Estimate</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            pct = (annual_est / benchmark * 100) if benchmark else 0
            color = "#00ff88" if pct < 80 else ("#ffdd00" if pct < 100 else "#ff4422")
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value" style="color:{color}">{pct:.1f}%</div>
                <div class="metric-unit">of industry avg</div>
                <div class="metric-label">Benchmark</div>
            </div>""", unsafe_allow_html=True)

        # Status
        st.markdown("<br>", unsafe_allow_html=True)
        if pct < 60:
            st.markdown('<div style="text-align:center"><span class="status-good">✅ EXCELLENT — Well Below Industry Average</span></div>', unsafe_allow_html=True)
        elif pct < 85:
            st.markdown('<div style="text-align:center"><span class="status-good">✅ GOOD — Below Industry Average</span></div>', unsafe_allow_html=True)
        elif pct < 100:
            st.markdown('<div style="text-align:center"><span class="status-warning">⚠️ MODERATE — Approaching Industry Average</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center"><span class="status-danger">🚨 HIGH — Exceeds Industry Average</span></div>', unsafe_allow_html=True)

        if total_kg == 0:
            st.markdown('<div class="info-box">⚠️ No consumption data entered. Please fill in at least one field above.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    if "results" not in st.session_state:
        st.markdown('<div class="info-box">💡 Run the Calculator first to see analytics.</div>', unsafe_allow_html=True)
    else:
        r = st.session_state["results"]
        bd = r["breakdown"]

        if not bd:
            st.markdown('<div class="info-box">⚠️ No data to visualize. Enter consumption values.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="section-header">📈 Emissions Analytics — {r["company"]}</div>', unsafe_allow_html=True)

            col_a, col_b = st.columns(2)

            # Pie chart
            with col_a:
                fig_pie = px.pie(
                    names=list(bd.keys()),
                    values=list(bd.values()),
                    title="Emissions by Source",
                    color_discrete_sequence=px.colors.sequential.Greens_r,
                    hole=0.45,
                )
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#aaffaa", family="Rajdhani"),
                    title_font=dict(color="#00ff88", size=16),
                    legend=dict(font=dict(color="#88cc88")),
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            # Bar chart
            with col_b:
                fig_bar = px.bar(
                    x=list(bd.keys()),
                    y=[v/1000 for v in bd.values()],
                    title="Emissions by Source (tonnes CO₂e)",
                    labels={"x": "Source", "y": "tonnes CO₂e"},
                    color=[v/1000 for v in bd.values()],
                    color_continuous_scale="Greens",
                )
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#aaffaa", family="Rajdhani"),
                    title_font=dict(color="#00ff88", size=16),
                    xaxis=dict(gridcolor="#1a3d1a"),
                    yaxis=dict(gridcolor="#1a3d1a"),
                    coloraxis_showscale=False,
                )
                fig_bar.update_traces(marker_line_color="#00ff88", marker_line_width=1)
                st.plotly_chart(fig_bar, use_container_width=True)

            # Benchmark gauge
            st.markdown('<div class="section-header">🎯 Industry Benchmark Comparison</div>', unsafe_allow_html=True)

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=r["annual_est"],
                delta={"reference": r["benchmark"], "valueformat": ".0f"},
                title={"text": f"Annual Emissions vs {r['industry']} Benchmark<br><span style='font-size:0.8em;color:#66bb6a'>tonnes CO₂e / year</span>"},
                gauge={
                    "axis": {"range": [0, r["benchmark"] * 1.5], "tickcolor": "#66bb6a"},
                    "bar": {"color": "#00ff88"},
                    "bgcolor": "#0d1a0d",
                    "bordercolor": "#1a5c1a",
                    "steps": [
                        {"range": [0, r["benchmark"] * 0.6],              "color": "#0a2a0a"},
                        {"range": [r["benchmark"] * 0.6, r["benchmark"]],  "color": "#1a3d0a"},
                        {"range": [r["benchmark"], r["benchmark"] * 1.5],   "color": "#3d0a0a"},
                    ],
                    "threshold": {
                        "line": {"color": "#ff4422", "width": 3},
                        "thickness": 0.75,
                        "value": r["benchmark"],
                    }
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#aaffaa", family="Rajdhani"),
                height=320,
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Equivalencies
            st.markdown('<div class="section-header">🌳 Real-World Equivalencies</div>', unsafe_allow_html=True)
            total_kg = r["total_kg"]
            eq1, eq2, eq3, eq4 = st.columns(4)
            with eq1:
                trees = int(total_kg / 21)
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-value">🌳 {trees:,}</div>
                    <div class="metric-label">Trees needed to offset</div>
                </div>""", unsafe_allow_html=True)
            with eq2:
                cars = int(total_kg / 4600)
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-value">🚗 {cars:,}</div>
                    <div class="metric-label">Cars driven for a year</div>
                </div>""", unsafe_allow_html=True)
            with eq3:
                flights = int(total_kg / 255)
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-value">✈️ {flights:,}</div>
                    <div class="metric-label">Flights (KHI → ISB)</div>
                </div>""", unsafe_allow_html=True)
            with eq4:
                homes = int(total_kg / 7300)
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-value">🏠 {homes:,}</div>
                    <div class="metric-label">Homes powered (1 yr)</div>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">💡 Smart Reduction Strategies</div>', unsafe_allow_html=True)

    if "results" in st.session_state:
        r  = st.session_state["results"]
        bd = r["breakdown"]
        top_sources = sorted(bd.items(), key=lambda x: x[1], reverse=True)[:3]

        st.markdown(f"""<div class="info-box">
        🎯 Based on your data for <b>{r['company']}</b>, your top emission sources are:
        <b>{', '.join([s[0] for s in top_sources]) if top_sources else 'N/A'}</b>. 
        Focus on these for maximum impact.
        </div>""", unsafe_allow_html=True)

    recs = [
        ("⚡", "Switch to Renewable Energy",
         "Install solar panels or purchase green energy certificates. Solar can reduce electricity emissions by 80–100%."),
        ("🔋", "Energy Efficiency Audit",
         "Conduct an ISO 50001 energy audit. Upgrading motors, compressors, and HVAC can cut energy use by 20–30%."),
        ("🔥", "Fuel Switching",
         "Replace diesel/coal with natural gas or biomass. Natural gas emits ~45% less CO₂ than coal per unit of energy."),
        ("♻️", "Waste Heat Recovery",
         "Install heat exchangers to capture and reuse waste heat from industrial processes — can save 10–20% on fuel."),
        ("🚛", "Green Logistics",
         "Optimize fleet routes, switch to CNG/EV vehicles, and consolidate shipments to reduce transport emissions."),
        ("💧", "Water & Waste Management",
         "Treat and recycle industrial wastewater on-site. Reduce solid waste sent to landfill through recycling programs."),
        ("📊", "Emissions Monitoring",
         "Install real-time IoT sensors for continuous emissions monitoring. Data-driven decisions reduce emissions 15–25%."),
        ("🌱", "Carbon Offsetting",
         "Invest in verified carbon offset projects (forestry, renewable energy) to neutralize unavoidable emissions."),
    ]

    for icon, title, desc in recs:
        st.markdown(f"""<div class="rec-box">
            <b style="color:#00ff88; font-size:1.05rem;">{icon} {title}</b><br>
            <span style="color:#aaffaa;">{desc}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="green-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🎯 Pakistan-Specific Targets</div>', unsafe_allow_html=True)
    st.markdown("""<div class="info-box">
    🇵🇰 Pakistan's NDC target: <b>50% reduction in projected emissions by 2030</b> (with international support).<br>
    📋 Industries should align with <b>NEQS (National Environmental Quality Standards)</b> set by SEPA/EPA.<br>
    🏭 Consider ISO 14001 Environmental Management System certification for your facility.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ABOUT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">🌍 About This Project</div>', unsafe_allow_html=True)
    st.markdown("""<div class="info-box">
    This <b>Industrial Carbon Footprint Tracker</b> is developed as part of the 
    <b>ICT for Climate Tech</b> course project. It enables industrial facilities to 
    measure, analyze, and reduce their greenhouse gas (GHG) emissions across multiple 
    energy and process sources.<br><br>
    The tool follows <b>GHG Protocol Scope 1 & 2</b> methodology and uses 
    Pakistan-relevant emission factors for accurate local calculations.
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">👥 Development Team</div>', unsafe_allow_html=True)
    for name, reg in TEAM:
        st.markdown(f"""<div class="team-card" style="padding:16px 22px;">
            <span class="team-name" style="font-size:1.1rem;">🔬 {name}</span>
            <span class="team-reg" style="font-size:0.9rem;">{reg}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="green-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📚 Emission Factors Used</div>', unsafe_allow_html=True)
    ef_df = pd.DataFrame([
        {"Energy Source": k, "Emission Factor": f"{v} kg CO₂e / unit"}
        for k, v in EMISSION_FACTORS.items()
    ])
    st.dataframe(ef_df, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-header">🏭 Industry Benchmarks</div>', unsafe_allow_html=True)
    bm_df = pd.DataFrame([
        {"Industry": k, "Annual Benchmark": f"{v:,} tonnes CO₂e / year"}
        for k, v in INDUSTRY_BENCHMARKS.items()
    ])
    st.dataframe(bm_df, use_container_width=True, hide_index=True)

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="green-divider">', unsafe_allow_html=True)
st.markdown(f"""<div class="footer">
    🌱 ICT FOR CLIMATE TECH &nbsp;|&nbsp; INDUSTRIAL CARBON FOOTPRINT TRACKER &nbsp;|&nbsp; 
    MECHANICAL ENGINEERING &nbsp;|&nbsp; {datetime.now().year}
</div>""", unsafe_allow_html=True)
