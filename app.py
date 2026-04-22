import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import json, os, time
import branca.colormap as cm
from folium.plugins import MarkerCluster
import plotly.express as px

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="GeoStatLab", layout="wide")

# -------------------------
# ONBOARDING STATE
# -------------------------
if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 0

if "show_onboarding" not in st.session_state:
    st.session_state.show_onboarding = True

onboarding_steps = [
    {
        "title": "👋 Welcome to GeoStatLab",
        "content": """
This platform helps you explore **statistics, maps, and policy simulation**.

You’ll learn how data drives decision-making in national statistical systems.
"""
    },
    {
        "title": "🗺️ Step 1: Explore Maps",
        "content": """
Go to the **Maps tab**.

- Select a year  
- Choose indicators  
- Compare **baseline vs policy maps**
"""
    },
    {
        "title": "📊 Step 2: Analyze Data",
        "content": """
Open the **Analysis tab**.

- View county rankings  
- Identify top & bottom performers  
- Track disparities
"""
    },
    {
        "title": "⚙️ Step 3: Simulate Policy",
        "content": """
Go to the **Policy tab**.

- Apply a policy (e.g. agriculture, education)  
- Adjust intensity  
- Observe impact on rankings
"""
    },
    {
        "title": "🎯 You're Ready!",
        "content": """
You can now:

✅ Explore data  
✅ Run simulations  
✅ Generate insights  

Use the Maps tab to start.
"""
    }
]
tab_map = {
    1: 3,  # Maps
    2: 4,  # Analysis
    3: 5   # Policy
}

if st.session_state.show_onboarding:
    step = st.session_state.onboarding_step
    if step in tab_map:
        st.info(f"👉 Switch to tab #{tab_map[step]} to continue")


# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    return pd.read_csv("geostatlab_data.csv")

@st.cache_data
def load_geojson():
    path = os.path.join(os.path.dirname(__file__), "kenya_counties.geojson")
    with open(path) as f:
        return json.load(f)

df_base = load_data()
geojson = load_geojson()

# -------------------------
# PANEL DATA
# -------------------------
years = list(range(2018, 2025))
panel = []

for _, row in df_base.iterrows():
    for i, year in enumerate(years):
        r = row.copy()
        r["Year"] = year
        r["Household_Income"] *= (1 + 0.05 * i)
        r["Poverty_Rate"] *= (1 - 0.02 * i)
        r["Agricultural_Output"] *= (1 + np.random.uniform(-0.1, 0.1))
        r["Education_Level"] = min(1, r["Education_Level"] * (1 + 0.015 * i))
        r["Unemployment_Rate"] *= (1 + np.random.uniform(-0.05, 0.05))
        panel.append(r)

df = pd.DataFrame(panel).sort_values(["County", "Year"])

# -------------------------
# SESSION STATE
# -------------------------
if "year" not in st.session_state:
    st.session_state.year = max(years)

if "playing" not in st.session_state:
    st.session_state.playing = False

if "selected_county" not in st.session_state:
    st.session_state.selected_county = df["County"].iloc[0]

# -------------------------
# MAP BUILDER
# -------------------------
def build_map(data, indicator):
    m = folium.Map(location=[0.5, 37.8], zoom_start=6)
    folium.Choropleth(
        geo_data=geojson,
        data=data,
        columns=["County", indicator],
        key_on="feature.properties.NAME_1",
        fill_color="YlOrRd",
        legend_name=indicator
    ).add_to(m)
    return m

# -------------------------
# HEADER
# -------------------------
st.title("🌍 GeoStatLab – Policy Intelligence Dashboard")
if st.session_state.show_onboarding:

    step = st.session_state.onboarding_step
    current = onboarding_steps[step]

    st.markdown("---")

    with st.container():
        st.markdown(f"## {current['title']}")
        st.markdown(current["content"])

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("⬅ Back", disabled=(step == 0)):
                st.session_state.onboarding_step -= 1

        with col2:
            if st.button("Next ➡"):
                if step < len(onboarding_steps) - 1:
                    st.session_state.onboarding_step += 1
                else:
                    st.session_state.show_onboarding = False

        with col3:
            if st.button("⏭ Skip"):
                st.session_state.show_onboarding = False

        with col4:
            if st.button("🔄 Restart"):
                st.session_state.onboarding_step = 0
                st.session_state.show_onboarding = True

    st.markdown("---")

# -------------------------
# TABS
# -------------------------
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Home",
    "📊 Dataset",
    "🧪 Survey",
    "🗺️ Maps",
    "📈 Analysis",
    "⚙️ Policy"
])

# -------------------------
# HOME
# -------------------------

with tab0:
    st.header("Welcome to GeoStatLab")
    st.info("Explore spatial statistics, simulate policy, and analyze impact.")
    if st.button("🎓 Start Guided Tour"):
        st.session_state.show_onboarding = True
        st.session_state.onboarding_step = 0

    st.markdown("""
    ### 📘 Learning Guide

    Welcome to **GeoStatLab**, an interactive platform designed to explore the integration of  
    **statistics, geospatial data, and policy simulation**.

    This platform is inspired by national statistical systems such as the  
    Kenya National Bureau of Statistics (KNBS) and supports:
    
    - Evidence-based decision making  
    - Spatial data analysis  
    - Policy impact simulation  
    """)

    st.markdown("---")

    # -------------------------
    # HOW TO USE
    # -------------------------
    st.markdown("### 🧭 How to Use This Tool")

    st.markdown("""
    **1️⃣ Dataset**
    - Explore socio-economic indicators across counties  
    - Understand structure of official statistics  

    **2️⃣ Survey Simulation**
    - Learn sampling techniques (random, stratified)  
    - Compare sample vs population statistics  

    **3️⃣ Maps**
    - Visualize spatial patterns  
    - Compare baseline vs policy scenarios  
    - Use time animation  

    **4️⃣ Analysis**
    - Examine rankings and trends  
    - Identify regional disparities  

    **5️⃣ Policy**
    - Simulate interventions  
    - Analyze impact on counties  
    - Track ranking changes  
    """)

    st.markdown("---")

    # -------------------------
    # OBJECTIVES
    # -------------------------
    st.markdown("### 🎯 Learning Objectives")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        - Understand spatial distribution of socio-economic indicators  
        - Interpret official statistics  
        - Analyze relationships between variables  
        """)

    with col2:
        st.markdown("""
        - Apply data to policy scenarios  
        - Strengthen evidence-based decision making  
        - Build intuition in geospatial analytics  
        """)

    st.markdown("---")

    # -------------------------
    # QUICK START
    # -------------------------
    st.markdown("### 🚀 Quick Start")

    st.info("""
    👉 Go to the **🗺️ Maps** tab  
    👉 Select a year and indicator  
    👉 Compare baseline vs policy maps  
    👉 Explore **📈 Analysis** and **⚙️ Policy** tabs  
    """)

    st.success("💡 Tip: Your selected year and county will update across all modules automatically.")

    st.markdown("---")

    # -------------------------
    # EXPANDABLE GUIDE
    # -------------------------
    st.markdown("### 📚 Module Guide")

    with st.expander("📊 Dataset"):
        st.write("Explore full national dataset and download for analysis.")

    with st.expander("🧪 Survey Simulation"):
        st.write("Understand sampling methods and bias.")

    with st.expander("🗺️ Maps"):
        st.write("Visualize spatial distribution and policy impact.")

    with st.expander("📈 Analysis"):
        st.write("Examine rankings, trends, and disparities.")

    with st.expander("⚙️ Policy"):
        st.write("Simulate interventions and compare outcomes.")

    st.markdown("---")

    st.caption("Developed for CATCON 9 – ISPRS 2026 | GeoStatLab Prototype")
# -------------------------
# DATASET
# -------------------------
with tab1:
    st.header("Dataset Overview")
    st.dataframe(df)
    st.download_button("Download", df.to_csv(index=False), "dataset.csv")

# -------------------------
# SURVEY
# -------------------------
with tab2:
    st.header("Survey Simulation")

    size = st.slider("Sample Size", 5, len(df), 20, key="sample_size")
    method = st.selectbox("Method", ["Random", "Stratified"], key="sampling_method")

    if method == "Random":
        sample = df.sample(size)
    else:
        sample = df.groupby("County").sample(1)

    st.dataframe(sample)

# -------------------------
# MAPS (MAIN FEATURE)
# -------------------------
with tab3:
    st.header("🗺️ Spatial Policy Dashboard")

    colA, colB = st.columns(2)

    with colA:
        if st.button("▶️ Play", key="play_maps"):
            st.session_state.playing = True
    with colB:
        if st.button("⏹ Stop", key="stop_maps"):
            st.session_state.playing = False

    if st.session_state.playing:
        idx = years.index(st.session_state.year)
        st.session_state.year = years[(idx + 1) % len(years)]
        time.sleep(0.5)
        st.rerun()

    year = st.slider(
        "Year",
        min(years),
        max(years),
        st.session_state.year,
        key="year_slider_maps"
    )

    st.session_state.year = year
    df_year = df[df["Year"] == year]

    indicator_map = {
        "Income": "Household_Income",
        "Poverty": "Poverty_Rate",
        "Agriculture": "Agricultural_Output"
    }

    col1, col2 = st.columns(2)

    ind_left = indicator_map[
        st.selectbox("Baseline Indicator", list(indicator_map.keys()), key="ind_left")
    ]

    ind_right = indicator_map[
        st.selectbox("Policy Indicator", list(indicator_map.keys()), key="ind_right")
    ]

    # POLICY
    policy = st.selectbox("Policy", ["Agriculture", "Education", "Jobs"], key="policy_main")
    intensity = st.slider("Intensity", 0, 50, 10, key="intensity_main")

    df_policy = df_year.copy()

    if policy == "Agriculture":
        df_policy["Agricultural_Output"] *= (1 + intensity/100)
    elif policy == "Education":
        df_policy["Education_Level"] *= (1 + intensity/100)
    elif policy == "Jobs":
        df_policy["Unemployment_Rate"] *= (1 - intensity/100)

    # MAPS SIDE BY SIDE
    colL, colR = st.columns(2)

    with colL:
        st.subheader("Baseline")
        st_folium(build_map(df_year, ind_left), height=400, key="map_left")

    with colR:
        st.subheader("Policy")
        st_folium(build_map(df_policy, ind_right), height=400, key="map_right")

    # DIFFERENCE MAP
    st.subheader("Impact Heatmap")

    df_diff = df_policy.copy()
    df_diff[ind_right] = df_policy[ind_right] - df_year[ind_right]

    st_folium(build_map(df_diff, ind_right), height=450, key="map_diff")

# -------------------------
# ANALYSIS
# -------------------------
with tab4:
    st.header("📊 Ranking Analysis")

    indicator = "Household_Income"

    df_year = df[df["Year"] == st.session_state.year]
    df_year["Rank"] = df_year[indicator].rank(ascending=False)

    df_rank = df_year[["County", "Rank"]]

    fig = px.bar(df_rank, x="County", y="Rank", title="County Ranking")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# POLICY (ADVANCED)
# -------------------------
with tab5:
    st.header("⚙️ Policy Intelligence")

    df_year = df[df["Year"] == st.session_state.year]
    df_policy = df_year.copy()

    policy = st.selectbox("Policy Type", ["Agriculture", "Education", "Jobs"], key="policy_adv")
    intensity = st.slider("Intensity %", 0, 50, 10, key="intensity_adv")

    if policy == "Agriculture":
        df_policy["Agricultural_Output"] *= (1 + intensity/100)

    df_year["Rank"] = df_year["Household_Income"].rank(ascending=False)
    df_policy["Rank"] = df_policy["Household_Income"].rank(ascending=False)

    df_rank = df_year.merge(df_policy, on="County", suffixes=("_Before", "_After"))
    df_rank["Change"] = df_rank["Rank_After"] - df_rank["Rank_Before"]

    df_rank["Color"] = df_rank["Change"].apply(
        lambda x: "Improved" if x < 0 else "Declined"
    )

    fig = px.bar(
        df_rank,
        x="County",
        y="Change",
        color="Color",
        title="Rank Change After Policy"
    )

    st.plotly_chart(fig, use_container_width=True)
