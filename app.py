import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import json, os, time
import branca.colormap as cm
from folium.plugins import MarkerCluster
import plotly.express as px

st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
h1, h2, h3 {
    color: #0f172a;
}
</style>
""", unsafe_allow_html=True)
if "year" not in st.session_state:
    st.session_state.year = 2024
    
# GLOBAL YEAR CONTROL (top of app)
st.sidebar.markdown("## 📅 Global Year")
years = list(range(2018, 2025))
global_year = st.sidebar.slider(
    "Select Year",
    min(years),
    max(years),
    st.session_state.year,
    key="global_year"
)
if "page" not in st.session_state:
    st.session_state.page = "Home"
    
st.session_state.year = global_year

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="GeoStatLab", layout="wide")

def switch_tab(index):
    st.session_state.active_tab = index
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
if st.session_state.show_onboarding:
    step = st.session_state.onboarding_step

    if step == 1:
        switch_tab(3)
    elif step == 2:
        switch_tab(4)
    elif step == 3:
        switch_tab(5)


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
# GLOBAL NAV STATE (NEW)
# -------------------------
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0





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
        switch_tab(3)
with col2:
    if st.button("📈 Go to Analysis"):
        switch_tab(4)
with col3:
    if st.button("⚙️ Run Policy Simulation"):
        switch_tab(5)

def role_guard(required_role):
    if st.session_state.role != required_role:
        st.warning(f"🔒 This module is optimized for {required_role} role")
# -------------------------
# TABS
# -------------------------
with st.sidebar:
    st.title("📍 Navigation")

    page = st.radio(
        "Go to",
        [
            "🏠 Home",
            "📊 Dataset",
            "🧪 Survey",
            "🗺️ Maps",
            "📈 Analysis",
            "⚙️ Policy",
            "🧠 Quiz"
        ]
    )

    st.session_state.page = page
# -------------------------
# HOME
# -------------------------
if st.session_state.page == "🏠 Home":
    st.header("🌍 GeoStatLab")

    st.markdown("Interactive Spatial Statistics & Policy Simulation Platform")

    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Counties", "47")
    col2.metric("📅 Years", "2018–2024")
    col3.metric("🧠 Modules", "5 + Quiz")

    st.markdown("---")

    st.markdown("""
    ### 🎯 What is GeoStatLab?

    A learning platform for:
    - Spatial data analysis  
    - Policy simulation  
    - Statistical reasoning  
    """)

    st.success("Use the sidebar to navigate through modules.")
    
# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("GeoStatLab | KNBS-style Policy Intelligence Dashboard")

# -------------------------
# DATASET
# -------------------------
if st.session_state.page == "📊 Dataset":
    st.header("📊 Dataset Overview")
#with tabs[1]:
 #   role_guard("Analyst")
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
if st.session_state.page == "🧪 Survey":
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
if st.session_state.page == "🗺️ Maps":
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
if st.session_state.page == "📈 Analysis":
    
    
    def generate_insights(df, indicator):
        top = df.sort_values(indicator, ascending=False).iloc[0]
        bottom = df.sort_values(indicator, ascending=True).iloc[0]
    
        insight = f"""
        🔍 **AI Insights**
    
        • {top['County']} leads in {indicator}, suggesting strong performance drivers.  
        • {bottom['County']} ranks lowest, indicating potential need for intervention.  
    
        • Regional disparity remains significant.  
        • Targeted policy could reduce inequality.
        """
        return insight

def smart_insights(df):
    insights = []

    if df["Education_Level"].mean() > 0.6:
        insights.append("Higher education levels correlate with improved outcomes.")

    if df["Poverty_Rate"].mean() > 0.3:
        insights.append("High poverty persists — targeted policies are needed.")

    if df["Unemployment_Rate"].mean() < 0.1:
        insights.append("Employment programs appear effective.")

    return insights


for i in smart_insights(df_year):
    st.info(i)



st.markdown(generate_insights(df_year, indicator))

if "global_indicator" not in st.session_state:
    st.session_state.global_indicator = "Household_Income"
    st.header("📊 County Ranking Analysis")

    # -------------------------
    # INDICATOR SELECTION
    # -------------------------
    indicator_map = {
        "Household Income": ("Household_Income", False),
        "Poverty Rate": ("Poverty_Rate", True),
        "Unemployment Rate": ("Unemployment_Rate", True),
        "Agricultural Output": ("Agricultural_Output", False),
        "Education Level": ("Education_Level", False)
    }

    label = st.selectbox("Select Indicator", list(indicator_map.keys()), key="rank_indicator")
    indicator, ascending = indicator_map[label]

    # -------------------------
    # YEAR FILTER
    # -------------------------
    year = st.session_state.year
    df_year = df[df["Year"] == year].copy()

    # -------------------------
    # RANKING
    # -------------------------
    df_year["Rank"] = df_year[indicator].rank(ascending=ascending, method="min")

    df_year = df_year.sort_values("Rank")

    # -------------------------
    # COLOR CODING
    # -------------------------
    def rank_color(r):
        if r <= 5:
            return "Top Performer"
        elif r >= len(df_year) - 4:
            return "Low Performer"
        else:
            return "Mid Tier"

    df_year["Category"] = df_year["Rank"].apply(rank_color)

    # -------------------------
    # PLOTLY BAR (HORIZONTAL)
    # -------------------------
    import plotly.express as px

    fig = px.bar(
        df_year,
        x="Rank",
        y="County",
        orientation="h",
        color="Category",
        title=f"{label} Ranking ({year})",
        hover_data=[indicator],
        category_orders={"Category": ["Top Performer", "Mid Tier", "Low Performer"]}
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=700
    )

    st.plotly_chart(fig, use_container_width=True, key="policy_rank_chart")

    # -------------------------
    # TOP / BOTTOM INSIGHTS
    # -------------------------
    st.markdown("### 🔍 Key Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.success("🏆 Top 5 Counties")
        st.dataframe(df_year.head(5)[["County", indicator, "Rank"]])

    with col2:
        st.error("⚠️ Bottom 5 Counties")
        st.dataframe(df_year.tail(5)[["County", indicator, "Rank"]])

    # -------------------------
    # RANK CHANGE (YOY)
    # -------------------------
    prev_year = year - 1

    if prev_year in df["Year"].unique():
        df_prev = df[df["Year"] == prev_year].copy()
        df_prev["Rank_prev"] = df_prev[indicator].rank(ascending=ascending, method="min")

        df_merge = df_year.merge(
            df_prev[["County", "Rank_prev"]],
            on="County",
            how="left"
        )

        df_merge["Rank_Change"] = df_merge["Rank_prev"] - df_merge["Rank"]

        st.markdown("### 🔄 Rank Change (Year-on-Year)")

        fig2 = px.bar(
            df_merge,
            x="County",
            y="Rank_Change",
            color="Rank_Change",
            color_continuous_scale="RdYlGn",
            title=f"Rank Change: {prev_year} → {year}",
            hover_data=["Rank", "Rank_prev"]
        )

        st.plotly_chart(fig2, use_container_width=True, key="policy_diff_chart")

    # -------------------------
    # COUNTY DRILLDOWN
    # -------------------------
    st.markdown("### 📍 County Drilldown")

    county = st.selectbox(
        "Select County",
        df_year["County"],
        key="rank_county"
    )

    county_data = df[df["County"] == county]

    st.line_chart(
        county_data.set_index("Year")[indicator]
    )

# -------------------------
# POLICY (ADVANCED)
# -------------------------
if st.session_state.page == "⚙️ Policy":
    st.header("⚙️ Policy Intelligence Dashboard")

    # -------------------------
    # SELECT YEAR & DATA
    # -------------------------
    year = st.session_state.year
    df_before = df[df["Year"] == year].copy()
    df_after = df_before.copy()

    # -------------------------
    # POLICY CONTROLS
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        policy = st.selectbox(
            "Policy Type",
            ["Agriculture Boost", "Education Investment", "Employment Program"],
            key="policy_adv"
        )

    with col2:
        intensity = st.slider(
            "Intensity (%)",
            0, 50, 10,
            key="intensity_adv"
        )

    # -------------------------
    # APPLY POLICY LOGIC
    # -------------------------
    if policy == "Agriculture Boost":
        df_after["Agricultural_Output"] *= (1 + intensity/100)
        df_after["Household_Income"] *= (1 + intensity/200)

    elif policy == "Education Investment":
        df_after["Education_Level"] *= (1 + intensity/100)
        df_after["Household_Income"] *= (1 + intensity/300)

    elif policy == "Employment Program":
        df_after["Unemployment_Rate"] *= (1 - intensity/100)
        df_after["Household_Income"] *= (1 + intensity/150)

    # -------------------------
    # INDICATOR SELECTION
    # -------------------------
    indicator_map = {
        "Household Income": ("Household_Income", False),
        "Poverty Rate": ("Poverty_Rate", True),
        "Unemployment Rate": ("Unemployment_Rate", True),
        "Agricultural Output": ("Agricultural_Output", False),
        "Education Level": ("Education_Level", False)
    }

    label = st.selectbox(
        "Evaluation Indicator",
        list(indicator_map.keys()),
        key="policy_indicator"
    )

    indicator, ascending = indicator_map[label]

    # -------------------------
    # RANK BEFORE / AFTER
    # -------------------------
    df_before["Rank_Before"] = df_before[indicator].rank(ascending=ascending, method="min")
    df_after["Rank_After"] = df_after[indicator].rank(ascending=ascending, method="min")

    df_rank = df_before[["County", indicator, "Rank_Before"]].merge(
        df_after[["County", indicator, "Rank_After"]],
        on="County",
        suffixes=("_Before", "_After")
    )

    df_rank["Rank_Change"] = df_rank["Rank_Before"] - df_rank["Rank_After"]

    # -------------------------
    # CLASSIFY IMPACT
    # -------------------------
    def classify(change):
        if change > 0:
            return "Improved"
        elif change < 0:
            return "Declined"
        else:
            return "No Change"

    df_rank["Impact"] = df_rank["Rank_Change"].apply(classify)

    # -------------------------
    # VISUAL: RANK CHANGE
    # -------------------------
    import plotly.express as px

    fig = px.bar(
        df_rank.sort_values("Rank_Change"),
        x="Rank_Change",
        y="County",
        orientation="h",
        color="Impact",
        color_discrete_map={
            "Improved": "green",
            "Declined": "red",
            "No Change": "gray"
        },
        title=f"📊 Rank Change After {policy} ({year})",
        hover_data=["Rank_Before", "Rank_After"]
    )

    fig.update_layout(height=700)

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # SUMMARY METRICS
    # -------------------------
    st.markdown("### 📌 Policy Impact Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Counties Improved",
            int((df_rank["Impact"] == "Improved").sum())
        )

    with col2:
        st.metric(
            "Counties Declined",
            int((df_rank["Impact"] == "Declined").sum())
        )

    with col3:
        st.metric(
            "No Change",
            int((df_rank["Impact"] == "No Change").sum())
        )

    # -------------------------
    # TOP WINNERS / LOSERS
    # -------------------------
    st.markdown("### 🏆 Winners & Losers")

    col1, col2 = st.columns(2)

    with col1:
        st.success("Top 5 Improved")
        st.dataframe(
            df_rank.sort_values("Rank_Change", ascending=False).head(5)
        )

    with col2:
        st.error("Top 5 Declined")
        st.dataframe(
            df_rank.sort_values("Rank_Change").head(5)
        )

    # -------------------------
    # DIFFERENCE VIEW (HEATMAP STYLE)
    # -------------------------
    st.markdown("### 🌡️ Indicator Change (Before vs After)")

    df_rank["Indicator_Change"] = (
        df_rank[f"{indicator}_After"] - df_rank[f"{indicator}_Before"]
    )

    fig2 = px.bar(
        df_rank.sort_values("Indicator_Change"),
        x="Indicator_Change",
        y="County",
        orientation="h",
        color="Indicator_Change",
        color_continuous_scale="RdYlGn",
        title=f"{label} Change After Policy"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -------------------------
    # DOWNLOAD RESULTS
    # -------------------------
    csv = df_rank.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Policy Results",
        csv,
        "policy_results.csv",
        "text/csv"
    )
    st.plotly_chart(
    fig,
    use_container_width=True,
    key=f"policy_chart_{st.session_state.year}"
)
if st.session_state.page == "🧠 Quiz":
    st.header("🧠 Assessment & Quiz")

    score = 0

    q1 = st.radio(
        "Which method ensures representation across counties?",
        ["Simple Random", "Stratified", "Cluster", "Systematic"]
    )

    if q1 == "Stratified":
        score += 1

    q2 = st.radio(
        "If unemployment decreases, what happens?",
        ["Increase", "Decrease", "Stay same"]
    )

    if q2 == "Decrease":
        score += 1

    q3 = st.radio(
        "Best map for inequality?",
        ["Bar chart", "Choropleth map", "Line chart"]
    )

    if q3 == "Choropleth map":
        score += 1

    if st.button("Submit Quiz"):
        st.success(f"Score: {score}/3")
