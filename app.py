
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from pandas import DataFrame
from pandas.io.parsers import TextFileReader
from streamlit_folium import st_folium
import json


data = {'time': pd.Timestamp.now()}
# default=str converts the Timestamp object to a string automatically
json_string = json.dumps(data, default=str)




st.set_page_config(page_title="GeoStatLab", layout="wide")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    return pd.read_csv("geostatlab_data.csv")

@st.cache_data
def load_geojson():
    with open("kenya_counties.geojson") as f:
        return json.load(f)

geojson = load_geojson()
df: TextFileReader | DataFrame = load_data()
geo = load_geojson()

# Normalize column names (adjust if needed)
geo.columns = geo.columns.str.lower()

# Try to match county names
if "county" not in geo.columns:
    if "name_1" in geo.columns:
        geo = geo.rename(columns={"name_1": "county"})

# Merge
geo["county"] = geo["county"].str.strip()
df["County"] = df["County"].str.strip()

gdf = geo.merge(df, left_on="county", right_on="County")

# -------------------------
# UI HEADER
# -------------------------
st.title("🌍 GeoStatLab")
st.markdown("**Interactive Platform for Teaching Spatial Statistics & Policy Analysis (KNBS Simulation)**")

# Sidebar
st.sidebar.title("Navigation")
module = st.sidebar.radio("Select Module", [
    "📘 Learning Guide",
    "📊 Dataset Overview",
    "🧪 Survey Simulation",
    "📈 Data Analysis",
    "🗺️ Interactive Map",
    "🏛️ Policy Simulation"
])

# -------------------------
# Learning Guide
# -------------------------
if module == "📘 Learning Guide":
    st.header("Learning Guide")

    st.markdown("""
    ### 🎓 What You Will Learn
    - Survey design & sampling
    - Data analysis & visualization
    - Spatial thinking using GIS
    - Policy impact evaluation

    ### 🔄 Recommended Flow
    1. Explore dataset  
    2. Simulate survey  
    3. Analyze indicators  
    4. Explore map  
    5. Test policies  

    👉 This mirrors real workflows used by National Statistical Offices.
    """)

# -------------------------
# Dataset Overview
# -------------------------
elif module == "📊 Dataset Overview":
    st.header("Dataset Overview")

    st.dataframe(df)

    st.subheader("Key Indicators")
    st.metric("Avg Income (KES)", int(df["Household_Income"].mean()))
    st.metric("Avg Poverty Rate", round(df["Poverty_Rate"].mean(), 2))

# -------------------------
# Survey Simulation
# -------------------------
elif module == "🧪 Survey Simulation":
    st.header("Survey Simulation")

    sample_size = st.slider("Sample Size", 2, len(df), 5)
    method = st.selectbox("Method", ["Random", "High Poverty Focus"])

    if method == "Random":
        sample = df.sample(sample_size)
    else:
        sample = df.sort_values("Poverty_Rate", ascending=False).head(sample_size)

    st.dataframe(sample)

    st.metric("Sample Avg Income", int(sample["Household_Income"].mean()))
    st.metric("Sample Poverty", round(sample["Poverty_Rate"].mean(), 2))

    st.info("Compare this with full dataset to understand sampling bias")

# -------------------------
# Data Analysis
# -------------------------
elif module == "📈 Data Analysis":
    st.header("Data Analysis")

    indicator = st.selectbox("Indicator", [
        "Household_Income", "Poverty_Rate",
        "Agricultural_Output", "Education_Level", "Unemployment_Rate"
    ])

    st.bar_chart(df.set_index("County")[indicator])

    st.markdown("### Insights")
    st.write(df.sort_values(indicator, ascending=False).head(3))

# -------------------------
# INTERACTIVE MAP
# -------------------------
elif module == "🗺️ Interactive Map":
    st.header("Kenya Spatial Analysis")

    indicator = st.selectbox("Select Indicator", [
        "Poverty_Rate", "Household_Income", "Unemployment_Rate"
    ])

    m = folium.Map(location=[0.5, 37.8], zoom_start=6)

    folium.Choropleth(
        geo_data=geojson,
        data=df,
        columns=["County", indicator],
        key_on="feature.properties.NAME_1",
        fill_color="YlOrRd",
        legend_name=indicator
    ).add_to(m)
    
    st_folium(m, width=900, height=500)

    folium.GeoJson(
        gdf,
        tooltip=folium.GeoJsonTooltip(
            fields=["County", indicator],
            aliases=["County:", "Value:"]
        )
    ).add_to(m)

    st_folium(m, width=900, height=500)

# -------------------------
# Policy Simulation
# -------------------------
elif module == "🏛️ Policy Simulation":
    st.header("Policy Simulation")

    policy = st.selectbox("Policy Type", [
        "Agricultural Investment",
        "Education Improvement",
        "Employment Program"
    ])

    intensity = st.slider("Intensity (%)", 0, 50, 10)

    df_sim = df.copy()

    if policy == "Agricultural Investment":
        df_sim["Agricultural_Output"] *= (1 + intensity/100)
        df_sim["Poverty_Rate"] *= (1 - intensity/200)

    elif policy == "Education Improvement":
        df_sim["Education_Level"] *= (1 + intensity/100)
        df_sim["Poverty_Rate"] *= (1 - intensity/300)

    elif policy == "Employment Program":
        df_sim["Unemployment_Rate"] *= (1 - intensity/100)
        df_sim["Household_Income"] *= (1 + intensity/150)

    st.subheader("Impact on Poverty")
    st.bar_chart(df_sim.set_index("County")["Poverty_Rate"])

    st.success("Policy simulation demonstrates data-driven decision making")
