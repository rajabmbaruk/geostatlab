import streamlit as st
import pandas as pd
import folium
from pandas import DataFrame
from pandas.io.parsers import TextFileReader
from streamlit_folium import st_folium
import json
import numpy as np
import branca.colormap as cm
import io

st.set_page_config(
    page_title="GeoStatLab",
    page_icon="📊",
    layout="wide"
)
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

#import json
import os

@st.cache_data
def load_geojson():
 file_path = os.path.join(os.path.dirname(__file__), "kenya_counties.geojson")
 with open(file_path) as f:
     return json.load(f)
 
geojson = load_geojson()
df = load_data()


# -------------------------
# UI HEADER
# -------------------------
# Style
st.markdown("""
<style>
.main {
    background-color: #f4f6f9;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background-color: grey;
    padding: 1.2rem;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}
h1, h2, h3 {
    color: #1f4e79;
}
</style>
""", unsafe_allow_html=True)

# Re-usable Card Wrapper
def card(title, content):
    st.markdown(f"""
    <div class="card">
        <h4>{title}</h4>
        {content}
    </div>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
# 🌍 GeoStatLab  
### *Spatial Statistics & Policy Simulation Platform*
""")
st.markdown("""---""")
# Sidebar

tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Home",
    "📊 Dataset Overview",
    "🧪 Survey Simulation",
    "🗺️ Spatial Map",
    "📈 Data Analysis",
    "⚙️ Policy Simulation",
    "📖 Story Mode"
])
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"
# -------------------------
# Learning Guide
# -------------------------
with tab0:
    st.title("🌍 GeoStatLab")
    st.subheader("Spatial Statistics & Policy Simulation Platform")

    st.markdown("""
    ### 📘 Learning Guide

    Welcome to **GeoStatLab**, an interactive platform designed to help users explore the integration of **statistics, geospatial data, and policy simulation**.

    This tool is inspired by the work of national statistical systems such as the Kenya National Bureau of Statistics (KNBS), and aims to support learning, decision-making, and data-driven policy design.
    """)

    st.markdown("---")

    st.markdown("### 🧭 How to Use This Tool")

    st.markdown("""
    **1️⃣ Dataset Overview**
    - Explore socio-economic indicators across counties  
    - Understand the structure of official statistics  

    **2️⃣ Spatial Map**
    - Visualize geographic patterns  
    - Hover to view indicators  
    - Click a county to interact with the dashboard  

    **3️⃣ Data Analysis**
    - View detailed statistics for selected counties  
    - Compare indicators across regions  

    **4️⃣ Policy Simulation**
    - Adjust policy variables (e.g. agriculture investment)  
    - Observe simulated impact on poverty and production  

    **5️⃣ Story Mode**
    - Follow a guided learning journey from data → insights → policy  
    """)

    st.markdown("---")

    st.markdown("### 🎯 Learning Objectives")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        - Understand spatial distribution of socio-economic indicators  
        - Interpret official statistics  
        - Explore relationships between variables  
        """)

    with col2:
        st.markdown("""
        - Apply data to policy scenarios  
        - Strengthen evidence-based decision making  
        - Build intuition in geospatial analytics  
        """)

    st.markdown("---")

    st.markdown("### 🚀 Quick Start")

    st.info("""
    👉 Go to the **🗺️ Spatial Map** tab  
    👉 Click on any county  
    👉 Then explore **📈 Data Analysis** and **⚙️ Policy Simulation**
    """)
    st.success("💡 Tip: The selected county will update across all modules automatically.")
    
    st.markdown("## 📘 Learning Guide")

    with st.expander("📊 Dataset Overview"):
        st.write("Explore indicators across counties")

    with st.expander("🗺️ Spatial Map"):
        st.write("Interact with geospatial data")

    st.markdown("---")
    st.caption("Developed as part of CATCON 9 – ISPRS 2026 | GeoStatLab Prototype")
# -------------------------
# Dataset Overview
# -------------------------
with tab1:
    #elif module == "📊 Dataset Overview":
 st.header("Dataset Overview")

 
 st.dataframe(df)
 csv_full = df.to_csv(index=False).encode("utf-8")

 st.download_button(
        "📥 Download Dataset",
        csv_full,
        "dataset.csv",
        "text/csv"
 )

 st.subheader("Key Indicators")
 st.write("Population Mean:", int(df["Population"].mean()))
 st.write("Average Income (KES)", int(df["Household_Income"].mean()))
 st.write("Average Poverty Rate (%)", round(df["Poverty_Rate"].mean(), 2))


# -------------------------
# Survey Simulation
# -------------------------
with tab2:
    #elif module == "🧪 Survey Simulation":
 st.header("Survey Simulation")


 sample_size = st.slider("Sample Size", 5, len(df), 10)

 sampling_method = st.selectbox(
     "Select Sampling Method",
     ["Simple Random", "Stratified", "Cluster", "Systematic"]
     )

 
 sample_size = min(sample_size, len(df))  # safety check
     
 if sampling_method == "Simple Random":
         sample = df.sample(n=sample_size, replace=False)
     
 elif sampling_method == "Stratified":
         sample = df.groupby("County", group_keys=False).apply(
             lambda x: x.sample(min(len(x), max(1, sample_size // df["County"].nunique())))
         )
     
 elif sampling_method == "Cluster":
         clusters = np.random.choice(
             df["County"].unique(),
             size=min(3, df["County"].nunique()),
             replace=False
         )
         sample = df[df["County"].isin(clusters)]
     
 elif sampling_method == "Systematic":
         k = max(1, len(df) // sample_size)
         sample = df.iloc[::k].head(sample_size)
     
 st.dataframe(sample)  
 st.write("Sample Population Mean:", int(sample["Population"].mean()))
 st.write("Sample Average Income (KES)", int(sample["Household_Income"].mean()))
 st.write("Sample Poverty Rate (%)", round(sample["Poverty_Rate"].mean(), 2))

 st.info("Compare this with full dataset to understand sampling bias")
 st.success("Learning Insight: Spatial disparities highlight regional inequalities.")
 if sampling_method == "Stratified":
     st.info("Stratified sampling ensures representation across regions.")

 elif sampling_method == "Cluster":
     st.info("Cluster sampling is cost-effective for large geographic surveys.")
 
 elif sampling_method == "Systematic":
     st.info("Systematic sampling selects every k-th unit from the population.")
# -------------------------
# Data Analysis
# -------------------------
with tab4:
    #elif module == "📈 Data Analysis":
  st.header("Data Analysis")
  
  indicator_map = {
   "Household Income (KES)": "Household_Income",
       "Poverty Rate (%)": "Poverty_Rate",
       "Agricultural Output (%)":"Agricultural_Output",
       "Education Level":"Education_Level", 
       "Unemployment Rate (%)": "Unemployment_Rate"
  }
  
  selected_label = st.selectbox("Select Indicator", list(indicator_map.keys()))
  indicator = indicator_map[selected_label]
  
  
  st.bar_chart(df.set_index("County")[indicator])
  
  st.markdown("### Insights")
#  col1, col2, col3 = st.columns(3)

 # col1.metric("Income", f"KES {int(indicator['Household_Income'].values[0]):,}")
  #col2.metric("Poverty Rate", f"{indicator['Poverty_Rate'].values[0]*100:.1f}%")
  #col3.metric("Agriculture", f"{int(indicator['Agricultural_Output'].values[0]):,}")  

  st.write(df.sort_values(indicator, ascending=False).head(3))
   
  st.success("Learning Insight: Spatial disparities highlight regional inequalities.")
  county_list = df["County"].tolist()

    # Ensure valid selection
  #county_list = df["County"].tolist()

  selected = st.session_state.get("selected_county", county_list[0])

  # Ensure it's valid
  if selected not in county_list:
    selected = county_list[0]
    st.session_state.selected_county = selected
  

  selected = st.selectbox(
    "Select County for Details",
    county_list,
    index=county_list.index(selected)
  )

  # Sync
  st.session_state.selected_county = selected

  county_data = df[df["County"] == selected]

  if not county_data.empty:
    row = county_data.iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        card("💰 Income", f"<h3>KES {int(row['Household_Income']):,}</h3>")

    with col2:
        card("📉 Poverty", f"<h3>{row['Poverty_Rate']*100:.1f}%</h3>")

    with col3:
        card("🌾 Agriculture", f"<h3>{int(row['Agricultural_Output']):,}tons</h3>")

        st.dataframe(county_data)

        csv = county_data.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download County Data",
            csv,
            f"{selected}.csv",
            "text/csv"
       )
  else:
        st.warning("No data available")
# -------------------------
# INTERACTIVE MAP
# -------------------------
with tab3:
    #elif module == "🗺️ Interactive Map":
 st.header("Kenya Spatial Analysis")


 indicator_map = {
 "Poverty Rate (%)": "Poverty_Rate",
 "Household Income (KES)": "Household_Income",
 "Unemployment Rate (%)": "Unemployment_Rate",
 "Agricultural Output (%)": "Agricultural_Output",
  "Education Level":   "Education_Level"
 }

 selected_label = st.selectbox("Select Indicator", list(indicator_map.keys()))
 indicator = indicator_map[selected_label]

 # Clean dataset county names (important for matching)
 
 df["County"] = df["County"].str.strip()
 
 if "selected_county" not in st.session_state:
   st.session_state.selected_county = df["County"].iloc[0]
    
 # Create lookup from dataframe
 data_lookup = df.set_index("County")[indicator].to_dict()

 def format_value(indicator, value):
     if indicator == "Household_Income":
         return f"KES {value:,.0f}"
     elif indicator == "Poverty_Rate":
         return f"{value*100:.1f}%"
     elif indicator == "Education_Level":
         return f"{value*100:.1f}%"
     elif indicator == "Agricultural_Output":
         return f"{value:,.0f} tons"
     else:
         return str(value)
         
 # Inject values into GeoJSON
 for feature in geojson["features"]:
     county_name = feature["properties"]["NAME_1"]
     raw_value = data_lookup.get(county_name, 0)

     feature["properties"][indicator] = format_value(indicator, raw_value)        

 # Create color scale
 min_val = df[indicator].min()
 max_val = df[indicator].max()
 colormap = cm.linear.YlOrRd_09.scale(min_val, max_val)
 colormap.caption = indicator

 m = folium.Map(location=[0.5, 37.8], zoom_start=6)

 folium.Choropleth(
     geo_data=geojson,
     data=df,
     columns=["County", indicator],
     key_on="feature.properties.NAME_1",  # adjust if needed
     fill_color="YlOrRd",
     legend_name=indicator
 ).add_to(m)

 #st_folium(m, width=900, height=500)

 folium.GeoJson(
     geojson,
     name="NAME_1"
 ).add_to(m)

 

 # Enhanced GeoJson (Tooltip + Highlight)
 folium.GeoJson(
     geojson,
     name="NAME_1",
     style_function=lambda x: {
         "fillColor": "transparent",
         "color": "black",
         "weight": 0.5
     },
     highlight_function=lambda x: {
         "fillColor": "#ffff00",
         "color": "black",
         "weight": 2,
         "fillOpacity": 0.5
     },
     tooltip=folium.GeoJsonTooltip(
         fields=["NAME_1", indicator],
         aliases=["County:", "Value:"],
         localize=True,
         sticky=True,
         labels=True,
         style="""
             background-color: white;
             border: 1px solid black;
             border-radius: 3px;
             box-shadow: 3px;
         """
     )
 ).add_to(m)
 
 
 #Render the map
 st_folium(m, width=900, height=500)
 # Add markers with detailed info
 for _, row in df.iterrows():
     folium.Marker(
         location=[-0.5 + hash(row["County"]) % 5, 36 + hash(row["County"]) % 5],
         popup=f"""
         <b>{row['County']}</b><br>
         Income: {row['Household_Income']}<br>
         Poverty: {row['Poverty_Rate']}<br>
         Agriculture: {row['Agricultural_Output']}<br>
         Education: {row['Education_Level']}
         """
     ).add_to(m)

 colormap.add_to(m)

 map_data = st_folium(m, width=700, height=500)
 
 
 st.info("Darker regions indicate higher values of the selected indicator.")
 st.success("Learning Insight: Spatial disparities highlight regional inequalities.")

 # Click interaction feedback
 st.subheader("Selected County Insights")
 # --- MAP CLICK FEEDBACK ---
 if map_data and map_data.get("last_active_drawing"):
    feature = map_data["last_active_drawing"]
    if "properties" in feature:
            clicked = feature["properties"].get("NAME_1")

            if clicked:
                st.session_state.selected_county = clicked.strip().title()

 # --- DROPDOWN (SYNCED WITH MAP) ---
 #selected = st.selectbox(
  #      "Select County for Details",
   #     df["County"],
  #  index=list(df["County"]).index(st.session_state.selected_county)
 #)

 # Update session state if user changes dropdown
# st.session_state.selected_county = selected

 # --- USE SINGLE SOURCE ---
 county_data = df[df["County"] == st.session_state.selected_county]

 st.write("### 📊 County Statistics")
 st.write(county_data)
# -------------------------
# Policy Simulation
# -------------------------
with tab5:
    #elif module == "🏛️ Policy Simulation":
 st.header("Policy Simulation")

 #selected = st.session_state.selected_county
 #st.subheader(f"Policy Impact for {selected}")

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
 csv_sim = df_sim.to_csv(index=False).encode("utf-8")

 st.download_button(
        "📥 Download Simulation",
        csv_sim,
        "simulation.csv",
        "text/csv"

 )
 st.success("Policy simulation demonstrates data-driven decision making")

with tab6:
    st.header("Guided Story Mode")

    step = st.radio("Step", [
        "1. Dataset",
        "2. Map",
        "3. Analysis",
        "4. Policy"
    ])

    if step == "1. Dataset":
        st.write("Explore national statistics")

    elif step == "2. Map":
        st.write("Understand spatial patterns")

    elif step == "3. Analysis":
        st.write(f"Current county: {st.session_state.selected_county}")

    elif step == "4. Policy":
        st.write("Simulate interventions")
