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

# -------------------------
# CONTROLS
# -------------------------
colA, colB, colC = st.columns([1,1,2])

with colA:
    if st.button("▶️ Play", key="play_btn"):
        st.session_state.playing = True

with colB:
    if st.button("⏹ Stop", key="stop_btn"):
        st.session_state.playing = False

# Auto-play
if st.session_state.playing:
    idx = years.index(st.session_state.year)
    st.session_state.year = years[(idx + 1) % len(years)]
    time.sleep(0.5)
    st.rerun()

# Year slider
selected_year = st.slider(
    "📅 Year",
    min_value=min(years),
    max_value=max(years),
    value=st.session_state.year,
    key="year_slider_main"
)

st.session_state.year = selected_year
df_year = df[df["Year"] == selected_year]

# -------------------------
# INDICATORS
# -------------------------
indicator_map = {
    "Income": "Household_Income",
    "Poverty": "Poverty_Rate",
    "Agriculture": "Agricultural_Output",
    "Education": "Education_Level",
    "Unemployment": "Unemployment_Rate"
}

col1, col2 = st.columns(2)

with col1:
    indicator_left = st.selectbox(
        "Baseline Indicator",
        list(indicator_map.keys()),
        key="indicator_left"
    )

with col2:
    indicator_right = st.selectbox(
        "Policy Indicator",
        list(indicator_map.keys()),
        key="indicator_right"
    )

ind_left = indicator_map[indicator_left]
ind_right = indicator_map[indicator_right]

# -------------------------
# POLICY SIMULATION
# -------------------------
policy = st.selectbox(
    "Policy",
    ["Agriculture", "Education", "Jobs"],
    key="policy_select_unique"
)

intensity = st.slider(
    "Intensity (%)",
    0, 50, 10,
    key="policy_intensity_unique"
)

df_policy = df_year.copy()

if policy == "Agriculture":
    df_policy["Agricultural_Output"] *= (1 + intensity/100)
    df_policy["Poverty_Rate"] *= (1 - intensity/200)

elif policy == "Education":
    df_policy["Education_Level"] *= (1 + intensity/100)
    df_policy["Poverty_Rate"] *= (1 - intensity/300)

elif policy == "Jobs":
    df_policy["Unemployment_Rate"] *= (1 - intensity/100)
    df_policy["Household_Income"] *= (1 + intensity/150)

# -------------------------
# SIDE-BY-SIDE MAPS
# -------------------------
st.subheader("🗺️ Before vs After Policy Maps")

colL, colR = st.columns(2)

with colL:
    st.markdown("### Baseline")
    m1 = build_map(df_year, ind_left)
    st_folium(m1, height=450, key="map_left")

with colR:
    st.markdown("### Policy Scenario")
    m2 = build_map(df_policy, ind_right)
    st_folium(m2, height=450, key="map_right")

# -------------------------
# DIFFERENCE HEATMAP
# -------------------------
st.subheader("🔥 Policy Impact Heatmap")

df_diff = df_policy.copy()
df_diff["Impact"] = df_policy[ind_right] - df_year[ind_right]

m_diff = build_map(df_diff.rename(columns={"Impact": ind_right}), ind_right)
st_folium(m_diff, height=500, key="map_diff")

# -------------------------
# RANKING ANALYSIS
# -------------------------
st.subheader("📊 County Ranking Analysis")

df_year["Rank"] = df_year[ind_left].rank(ascending=False)
df_policy["Rank"] = df_policy[ind_right].rank(ascending=False)

df_rank = df_year[["County", "Rank"]].merge(
    df_policy[["County", "Rank"]],
    on="County",
    suffixes=("_Before", "_After")
)

df_rank["Rank_Change"] = df_rank["Rank_After"] - df_rank["Rank_Before"]

# -------------------------
# PLOTLY VISUAL
# -------------------------
df_rank["Color"] = df_rank["Rank_Change"].apply(
    lambda x: "Improved" if x < 0 else ("Declined" if x > 0 else "No Change")
)

color_map = {"Improved": "green", "Declined": "red", "No Change": "gray"}

fig = px.bar(
    df_rank,
    x="County",
    y="Rank_Change",
    color="Color",
    color_discrete_map=color_map,
    hover_data=["Rank_Before", "Rank_After"],
    title="Rank Change by County"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# ANIMATION
# -------------------------
st.subheader("🎬 Rank Change Over Time")

df_anim = df.copy()

df_anim["Rank"] = df_anim.groupby("Year")[ind_left].rank(ascending=False)

fig_anim = px.bar(
    df_anim,
    x="County",
    y="Rank",
    animation_frame="Year",
    color="Rank",
    title="Ranking Evolution"
)

st.plotly_chart(fig_anim, use_container_width=True)

# -------------------------
# COUNTY DETAIL PANEL
# -------------------------
st.subheader("📍 County Insights")

county_list = sorted(df_year["County"].unique())

selected = st.selectbox(
    "Select County",
    county_list,
    index=county_list.index(st.session_state.selected_county),
    key="county_select_main"
)

st.session_state.selected_county = selected

county_data = df[df["County"] == selected]

st.line_chart(
    county_data.set_index("Year")[ind_left]
)

st.dataframe(county_data)

# -------------------------
# DOWNLOADS
# -------------------------
st.download_button(
    "📥 Download Dataset",
    df.to_csv(index=False).encode("utf-8"),
    "geostatlab_full.csv"
)

st.success("✅ Full KNBS-grade policy dashboard loaded successfully.")
