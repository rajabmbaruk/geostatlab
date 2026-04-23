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
# USER ROLE (NEW)
# -------------------------
if "role" not in st.session_state:
    st.session_state.role = "Analyst"

with st.sidebar:
    st.markdown("## 👤 User Role")
    role = st.radio(
        "Select Role",
        ["Analyst", "Policy Maker"],
        index=0
    )
    st.session_state.role = role

# -------------------------
# FIRST-TIME USER TRIGGER
# -------------------------
if "first_visit" not in st.session_state:
    st.session_state.first_visit = True
    st.session_state.show_onboarding = True
    st.session_state.onboarding_step = 0

# -------------------------
# ONBOARDING STEPS
# -------------------------
steps = [
    ("👋 Welcome", "Explore statistics, maps, and policy simulation."),
    ("🗺️ Maps", "Compare baseline vs policy maps."),
    ("📊 Analysis", "Track rankings and disparities."),
    ("⚙️ Policy", "Simulate interventions and impacts."),
    ("🎯 Ready", "Start exploring GeoStatLab.")
]

# -------------------------
# SIDEBAR PROGRESS TRACKER
# -------------------------
with st.sidebar:
    st.markdown("## 📚 Learning Progress")

    progress = st.session_state.get("onboarding_step", 0) / (len(steps)-1)

    st.progress(progress)

    for i, (title, _) in enumerate(steps):
        if i == st.session_state.onboarding_step:
            st.markdown(f"👉 **{title}**")
        else:
            st.markdown(f"• {title}")

    st.markdown("---")
# -------------------------
# HEADER
# -------------------------
st.title("🌍 GeoStatLab – Policy Intelligence Dashboard")
# -------------------------
# FLOATING MODAL (SIMULATED)
# -------------------------
if st.session_state.get("show_onboarding", False):

    step = st.session_state.onboarding_step
    title, content = steps[step]

    with st.container():
        st.markdown(
            f"""
            <div style="
                position: fixed;
                top: 20%;
                left: 25%;
                width: 50%;
                background-color: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0px 8px 30px rgba(0,0,0,0.2);
                z-index: 9999;
            ">
                <h3>{title}</h3>
                <p>{content}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("⬅ Back", disabled=(step == 0)):
            st.session_state.onboarding_step -= 1

    with col2:
        if st.button("Next ➡"):
            if step < len(steps) - 1:
                st.session_state.onboarding_step += 1
            else:
                st.session_state.show_onboarding = False
                st.session_state.first_visit = False

    with col3:
        if st.button("⏭ Skip"):
            st.session_state.show_onboarding = False
            st.session_state.first_visit = False

    with col4:
        if st.button("🔄 Restart"):
            st.session_state.onboarding_step = 0
            st.session_state.show_onboarding = True

# -------------------------
# TOOLTIP GUIDANCE
# -------------------------
st.markdown("## 🧭 Navigation Guide")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🗺️ Maps → Explore spatial patterns")

with col2:
    st.info("📈 Analysis → Rankings & trends")

with col3:
    st.info("⚙️ Policy → Simulate interventions")

# -------------------------
# ROLE-BASED DASHBOARD CONTENT
# -------------------------
st.markdown("---")

if st.session_state.role == "Analyst":

    st.subheader("📊 Analyst View")

    st.markdown("""
    Focus:
    - Data exploration  
    - Statistical analysis  
    - Trend evaluation  
    """)

    st.success("Tip: Use Analysis tab for deep insights")

elif st.session_state.role == "Policy Maker":

    st.subheader("🏛️ Policy Maker View")

    st.markdown("""
    Focus:
    - Policy scenarios  
    - Impact comparison  
    - Decision insights  
    """)

    st.warning("Tip: Start with Policy tab to simulate interventions")

# -------------------------
# QUICK START ACTIONS
# -------------------------
st.markdown("---")
st.markdown("## 🚀 Quick Start")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🗺️ Open Maps"):
        st.session_state.onboarding_step = 1

with col2:
    if st.button("📈 Go to Analysis"):
        st.session_state.onboarding_step = 2

with col3:
    if st.button("⚙️ Run Policy Simulation"):
        st.session_state.onboarding_step = 3

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

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("GeoStatLab | KNBS-style Policy Intelligence Dashboard")

# -------------------------
# DATASET
# -------------------------
with tab1:
    st.header("📊 Dataset Overview")

    # -------------------------
    # FILTERS (TOP BAR)
    # -------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_year = st.selectbox(
            "📅 Select Year",
            sorted(df["Year"].unique()),
            key="dataset_year"
        )

    with col2:
        counties = sorted(df["County"].unique())
        selected_counties = st.multiselect(
            "🏞️ Select Counties",
            counties,
            default=counties[:5]
        )

    with col3:
        indicator = st.selectbox(
            "📌 Focus Indicator",
            ["Household_Income", "Poverty_Rate", "Agricultural_Output",
             "Education_Level", "Unemployment_Rate"]
        )

    df_filtered = df[
        (df["Year"] == selected_year) &
        (df["County"].isin(selected_counties))
    ]

    st.markdown("---")

    # -------------------------
    # KPI CARDS
    # -------------------------
    st.subheader("📌 Key Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Population",
        f"{int(df_filtered['Population'].mean()):,}"
    )

    col2.metric(
        "💰 Avg Income",
        f"KES {int(df_filtered['Household_Income'].mean()):,}"
    )

    col3.metric(
        "📉 Poverty Rate",
        f"{df_filtered['Poverty_Rate'].mean()*100:.1f}%"
    )

    col4.metric(
        "📊 Unemployment",
        f"{df_filtered['Unemployment_Rate'].mean()*100:.1f}%"
    )

    st.markdown("---")

    # -------------------------
    # DISTRIBUTION ANALYSIS
    # -------------------------
    st.subheader("📊 Indicator Distribution")

    st.bar_chart(
        df_filtered.set_index("County")[indicator]
    )

    # -------------------------
    # TOP & BOTTOM COUNTIES
    # -------------------------
    st.subheader("🏆 Top & Bottom Performers")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔝 Top Counties")
        st.dataframe(
            df_filtered.sort_values(indicator, ascending=False).head(5)
        )

    with col2:
        st.markdown("### 🔻 Bottom Counties")
        st.dataframe(
            df_filtered.sort_values(indicator, ascending=True).head(5)
        )

    st.markdown("---")

    # -------------------------
    # TREND ANALYSIS
    # -------------------------
    st.subheader("📈 Trends Over Time")

    trend_df = df[df["County"].isin(selected_counties)]

    st.line_chart(
        trend_df.groupby("Year")[indicator].mean()
    )

    st.markdown("---")

    # -------------------------
    # DATA TABLE (EXPANDABLE)
    # -------------------------
    with st.expander("📂 View Full Dataset"):
        st.dataframe(df_filtered)

        csv = df_filtered.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download Filtered Dataset",
            csv,
            f"dataset_{selected_year}.csv",
            "text/csv"
        )

    # -------------------------
    # INSIGHTS PANEL
    # -------------------------
    st.subheader("💡 Key Insights")

    top_county = df_filtered.sort_values(indicator, ascending=False).iloc[0]["County"]
    bottom_county = df_filtered.sort_values(indicator, ascending=True).iloc[0]["County"]

    st.success(f"Highest {indicator}: {top_county}")
    st.warning(f"Lowest {indicator}: {bottom_county}")

    st.info("Use the Maps tab to visualize these disparities spatially.")



# -------------------------
# SURVEY
# -------------------------
with tab2:
    st.header("🧪 Survey Simulation Lab")

    # -------------------------
    # CONTROLS
    # -------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        size = st.slider(
            "Sample Size",
            min_value=5,
            max_value=len(df),
            value=20,
            key="sample_size"
        )

    with col2:
        method = st.selectbox(
            "Sampling Method",
            ["Simple Random", "Stratified", "Cluster", "Systematic"],
            key="sampling_method"
        )

    with col3:
        indicator = st.selectbox(
            "Indicator",
            ["Household_Income", "Poverty_Rate", "Agricultural_Output"],
            key="sampling_indicator"
        )

    # -------------------------
    # SAMPLING LOGIC
    # -------------------------
    size = min(size, len(df))

    if method == "Simple Random":
        sample = df.sample(n=size, replace=False)

    elif method == "Stratified":
        sample = df.groupby("County", group_keys=False).apply(
            lambda x: x.sample(min(len(x), max(1, size // df["County"].nunique())))
        )

    elif method == "Cluster":
        clusters = np.random.choice(
            df["County"].unique(),
            size=min(3, df["County"].nunique()),
            replace=False
        )
        sample = df[df["County"].isin(clusters)]

    elif method == "Systematic":
        k = max(1, len(df) // size)
        sample = df.iloc[::k].head(size)

    st.markdown("---")

    # -------------------------
    # DISPLAY SAMPLE
    # -------------------------
    st.subheader("📋 Sample Data")
    st.dataframe(sample)

    # -------------------------
    # COMPARISON METRICS
    # -------------------------
    st.subheader("📊 Sample vs Population")

    col1, col2 = st.columns(2)

    pop_mean = df[indicator].mean()
    sample_mean = sample[indicator].mean()

    with col1:
        st.metric(
            "Population Mean",
            f"{pop_mean:,.2f}"
        )

    with col2:
        st.metric(
            "Sample Mean",
            f"{sample_mean:,.2f}",
            delta=f"{sample_mean - pop_mean:,.2f}"
        )

    # -------------------------
    # VISUAL COMPARISON
    # -------------------------
    st.subheader("📈 Distribution Comparison")

    chart_df = pd.DataFrame({
        "Type": ["Population", "Sample"],
        "Mean": [pop_mean, sample_mean]
    })

    st.bar_chart(chart_df.set_index("Type"))

    # -------------------------
    # BIAS INSIGHT
    # -------------------------
    st.subheader("💡 Sampling Insight")

    diff = abs(sample_mean - pop_mean)

    if diff < 0.05 * pop_mean:
        st.success("✅ Sample is representative of the population.")
    elif diff < 0.15 * pop_mean:
        st.warning("⚠️ Moderate sampling bias detected.")
    else:
        st.error("❌ High sampling bias — consider better sampling method.")

    # -------------------------
    # EDUCATIONAL NOTES
    # -------------------------
    st.markdown("### 📘 Method Explanation")

    if method == "Simple Random":
        st.info("Each unit has equal probability of selection.")

    elif method == "Stratified":
        st.info("Ensures representation across counties (strata).")

    elif method == "Cluster":
        st.info("Selects groups (counties) instead of individuals.")

    elif method == "Systematic":
        st.info("Selects every k-th observation from the dataset.")

    # -------------------------
    # DOWNLOAD SAMPLE
    # -------------------------
    csv = sample.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Sample",
        csv,
        "sample_data.csv",
        "text/csv"
    )



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
    st.header("📊 Ranking Analysis Dashboard")

    # -------------------------
    # CONTROLS
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        indicator = st.selectbox(
            "Select Indicator",
            ["Household_Income", "Poverty_Rate",
             "Agricultural_Output", "Education_Level",
             "Unemployment_Rate"],
            key="rank_indicator"
        )

    with col2:
        year = st.selectbox(
            "Select Year",
            sorted(df["Year"].unique()),
            index=len(df["Year"].unique()) - 1,
            key="rank_year"
        )

    df_year = df[df["Year"] == year].copy()

    # -------------------------
    # RANK CALCULATION
    # -------------------------
    ascending = True if indicator in ["Poverty_Rate", "Unemployment_Rate"] else False

    df_year["Rank"] = df_year[indicator].rank(
        ascending=ascending,
        method="min"
    )

    df_year = df_year.sort_values("Rank")

    # -------------------------
    # COLOR LOGIC
    # -------------------------
    df_year["Category"] = df_year["Rank"].apply(
        lambda x: "Top Performers" if x <= 10 else "Others"
    )

    # -------------------------
    # INTERACTIVE BAR CHART
    # -------------------------
    fig = px.bar(
        df_year,
        x="County",
        y="Rank",
        color="Category",
        title=f"{indicator} Ranking ({year})",
        hover_data=[indicator],
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="Rank (Lower is Better)",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # TOP / BOTTOM TABLES
    # -------------------------
    st.markdown("### 🏆 Top & Bottom Counties")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔝 Top Performers")
        st.dataframe(df_year.head(5))

    with col2:
        st.markdown("#### 🔻 Bottom Performers")
        st.dataframe(df_year.tail(5))

    st.markdown("---")

    # -------------------------
    # RANK CHANGE (TIME COMPARISON)
    # -------------------------
    st.subheader("🔄 Rank Change Over Time")

    col1, col2 = st.columns(2)

    with col1:
        year1 = st.selectbox("From Year", sorted(df["Year"].unique()), key="year1")

    with col2:
        year2 = st.selectbox("To Year", sorted(df["Year"].unique()), key="year2")

    df1 = df[df["Year"] == year1].copy()
    df2 = df[df["Year"] == year2].copy()

    df1["Rank"] = df1[indicator].rank(ascending=ascending)
    df2["Rank"] = df2[indicator].rank(ascending=ascending)

    df_compare = df1[["County", "Rank"]].merge(
        df2[["County", "Rank"]],
        on="County",
        suffixes=("_Start", "_End")
    )

    df_compare["Rank_Change"] = df_compare["Rank_Start"] - df_compare["Rank_End"]

    # -------------------------
    # COLOR-CODED CHANGE
    # -------------------------
    df_compare["Trend"] = df_compare["Rank_Change"].apply(
        lambda x: "Improved" if x > 0 else ("Declined" if x < 0 else "No Change")
    )

    fig2 = px.bar(
        df_compare,
        x="County",
        y="Rank_Change",
        color="Trend",
        title=f"Ranking Change ({year1} → {year2})",
        hover_data=["Rank_Start", "Rank_End"]
    )

    fig2.update_layout(
        xaxis_tickangle=-45,
        height=500
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -------------------------
    # INSIGHTS
    # -------------------------
    st.subheader("💡 Insights")

    top_gainer = df_compare.sort_values("Rank_Change", ascending=False).iloc[0]["County"]
    top_loser = df_compare.sort_values("Rank_Change").iloc[0]["County"]

    st.success(f"📈 Most Improved County: {top_gainer}")
    st.error(f"📉 Most Declined County: {top_loser}")

    st.info("Use Policy Simulation tab to understand drivers of these changes.")



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
