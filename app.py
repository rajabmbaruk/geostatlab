
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
st.title("GeoStatLab: NSO Simulation Platform ")

st.markdown("""
This platform is An interactive tool for Teaching Spatial Statistics using KNBS-style Data, how spatial data analysis, survey simulation,
and policy modeling can support evidence-based decision making.
""")
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


 sample_size = st.slider("Sample Size", 5, len(df), 20)

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
 st.write("Population Mean:", int(df["Population"].mean()))
 st.write("Sample Mean:", int(sample["Population"].mean()))
 st.write("Sample Avg Income", int(sample["Household_Income"].mean()))
 st.write("Sample Poverty", round(sample["Poverty_Rate"].mean(), 2))

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
elif module == "📈 Data Analysis":
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
  st.write(df.sort_values(indicator, ascending=False).head(3))
  
   
  st.success("Learning Insight: Spatial disparities highlight regional inequalities.")
# -------------------------
# INTERACTIVE MAP
# -------------------------
elif module == "🗺️ Interactive Map":
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

 if map_data and map_data.get("last_clicked"):
     st.write("Map clicked - explore county patterns above")

 # Optional: dropdown for deeper dive
 selected = st.selectbox("Select County for Details", df["County"])

 county_data = df[df["County"] == selected]

 st.write("### County Statistics")
 st.write(county_data)
 
# -------------------------
# Policy Simulation
# -------------------------
elif module == "🏛️ Policy Simulation":
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

 st.success("Policy simulation demonstrates data-driven decision making")
