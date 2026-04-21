import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np
import json, os
import branca.colormap as cm
from folium.plugins import MarkerCluster

st.set_page_config(page_title="GeoStatLab", page_icon="📊", layout="wide")

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

#---------------------------
# Panel Data
#---------------------------
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

#----------------------------
# Global State
#----------------------------
county_list = sorted(df["County"].unique())

if "selected_county" not in st.session_state:
    st.session_state.selected_county = county_list[0]

if "year" not in st.session_state:
    st.session_state.year = df["Year"].max()

#-----------------------------
# Centroid
#--------------------------------
def get_centroid(feature):
    coords = feature["geometry"]["coordinates"]

    if feature["geometry"]["type"] == "MultiPolygon":
        coords = coords[0][0]
    else:
        coords = coords[0]

    lons = [p[0] for p in coords]
    lats = [p[1] for p in coords]

    return [np.mean(lats), np.mean(lons)]

#------------------------------
# Centroid Lookup
#------------------------------
centroid_lookup = {
    f["properties"]["NAME_1"].strip(): get_centroid(f)
    for f in geojson["features"]
}

#-----------------------------------
# Map Builder
#-------------------------------
def build_map(df_year, indicator):

    m = folium.Map(location=[0.5, 37.8], zoom_start=6)

    folium.Choropleth(
        geo_data=geojson,
        data=df_year,
        columns=["County", indicator],
        key_on="feature.properties.NAME_1",
        fill_color="YlOrRd"
    ).add_to(m)

    marker_cluster = MarkerCluster().add_to(m)

    min_val = df_year[indicator].min()
    max_val = df_year[indicator].max()

    colormap = cm.linear.YlOrRd_09.scale(min_val, max_val)

    for _, row in df_year.iterrows():
        county = row["County"]
        value = row[indicator]

        if county in centroid_lookup:
            color = colormap(value)

            folium.CircleMarker(
                location=centroid_lookup[county],
                radius=6 + 10 * (value - min_val) / (max_val - min_val + 1e-6),
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=county
            ).add_to(marker_cluster)

    folium.LayerControl().add_to(m)

    return m
#-----------------------------------
#Spatial Map
#---------------------------------
with tab3:
    st.header("Kenya Spatial Analysis")

    years = sorted(df["Year"].unique())

    import time
    
    st.subheader("⏱️ Time Animation")
    
    col1, col2 = st.columns([1,1])
    
    with col1:
        play = st.button("▶️ Play")
    
    with col2:
        stop = st.button("⏹️ Stop")
    
    if "playing" not in st.session_state:
        st.session_state.playing = False
    
    if play:
        st.session_state.playing = True
    
    if stop:
        st.session_state.playing = False
        
    years = sorted(df["Year"].unique())
    
    if st.session_state.playing:
        current_index = years.index(st.session_state.year)
    
        next_index = (current_index + 1) % len(years)
        st.session_state.year = years[next_index]
    
        time.sleep(0.6)  # speed control
        st.rerun()
    
    selected_year = st.slider(
        "📅 Select Year",
        min_value=min(years),
        max_value=max(years),
        value=st.session_state.year,
        step=1
    )
    
    st.session_state.year = selected_year
    df_year = df[df["Year"] == selected_year]

    indicator_map = {
        "Income": "Household_Income",
        "Poverty": "Poverty_Rate",
        "Agriculture": "Agricultural_Output",
        "Education": "Education_Level",
        "Unemployment": "Unemployment_Rate"
    }

    label = st.selectbox("Indicator", list(indicator_map.keys()))
    indicators = list(indicator_map.values())
    
    if "indicator_index" not in st.session_state:
        st.session_state.indicator_index = 0
    
    if st.session_state.playing:
        st.session_state.indicator_index = (st.session_state.indicator_index + 1) % len(indicators)
    
    indicator = indicators[st.session_state.indicator_index]
    
    st.caption(f"🗓️ Year: {st.session_state.year}")
    st.progress((years.index(st.session_state.year)+1)/len(years))
    # BUILD MAP
    m = build_map(df_year, indicator)

    map_data = st_folium(m, width=900, height=500)

    # ✅ FIXED CLICK HANDLING
    if map_data and map_data.get("last_object_clicked"):
        clicked = map_data["last_object_clicked"].get("popup")

        if clicked and clicked in county_list:
            st.session_state.selected_county = clicked
            st.rerun()
#----------------------------
#County Panel
#---------------------------------
    st.subheader("Selected County Insights")

    selected = st.selectbox(
        "Select County",
        county_list,
        index=county_list.index(st.session_state.selected_county)
    )

    st.session_state.selected_county = selected

    county_data = df_year[df_year["County"] == selected]

    st.write(f"### 📊 {selected} ({selected_year})")
    st.dataframe(county_data)
# -------------------------
# INTERACTIVE MAP
# -------------------------
#with tab3:
    #elif module == "🗺️ Interactive Map":
     st.header("Kenya Spatial Analysis")
     
     years = sorted(df["Year"].unique())
    
     selected_year = st.slider(
        "📅 Select Year",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=int(max(years)),
        step=1
     )
     df_year = df[df["Year"] == selected_year]
        
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
     
     df_year["County"] = df_year["County"].str.strip()
     
     if "selected_county" not in st.session_state:
       st.session_state.selected_county = df_year["County"].iloc[0]
        
     # Create lookup from dataframe
     data_lookup = df_year.set_index("County")[indicator].to_dict()
    
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
     min_val = df_year[indicator].min()
     max_val = df_year[indicator].max()
     colormap = cm.linear.YlOrRd_09.scale(min_val, max_val)
     colormap.caption = indicator
    
     m = folium.Map(location=[0.5, 37.8], zoom_start=6)
    
     folium.Choropleth(
         geo_data=geojson,
         data=df_year,
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
        name="Counties",
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
            sticky=True
        )
     ).add_to(m)
    
     
     
     #Render the map
     #st_folium(m, width=900, height=500)
     # Add markers with detailed info
     #import numpy as np
    
     def get_centroid(feature):
        coords = feature["geometry"]["coordinates"]
    
        # Handle MultiPolygon
        if feature["geometry"]["type"] == "MultiPolygon":
            coords = coords[0][0]
        else:  # Polygon
            coords = coords[0]
    
        lons = [point[0] for point in coords]
        lats = [point[1] for point in coords]
    
        return [np.mean(lats), np.mean(lons)]
    
     centroid_lookup = {}
    
     for feature in geojson["features"]:
        county_name = feature["properties"]["NAME_1"].strip()
        centroid_lookup[county_name] = get_centroid(feature)
        
     for _, row in df_year.iterrows():
        county = row["County"]
    
     if county in centroid_lookup:
            folium.Marker(
                location=centroid_lookup[county],
                popup=f"""
                <b>{county}</b><br>
                Income: {row['Household_Income']:,}<br>
                Poverty: {row['Poverty_Rate']:.2f}<br>
                Agriculture: {row['Agricultural_Output']:,}<br>
                Education: {row['Education_Level']:.2f}
                """
            ).add_to(m)
         
     marker_cluster = MarkerCluster().add_to(m)
    
     min_val = df_year[indicator].min()
     max_val = df_year[indicator].max()
    
     def scale_radius(value):
        return 5 + 15 * ((value - min_val) / (max_val - min_val + 1e-6))
    
     for _, row in df_year.iterrows():
        county = row["County"]
        value = row[indicator]
    
        if county in centroid_lookup:
            color = colormap(value)
    
            folium.CircleMarker(
                location=centroid_lookup[county],
                radius=scale_radius(value),
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=f"""
                <b>{county}</b><br>
                {indicator}: {value}
                """
            ).add_to(marker_cluster)
            #colormap.add_to(m)
     folium.LayerControl().add_to(m)
     map_data = st_folium(m, width=900, height=500)
     
     if map_data and map_data.get("last_object_clicked"):
        clicked = map_data["last_object_clicked"].get("properties", {}).get("NAME_1")
    
        if clicked:
            clicked_clean = clicked.strip()
    
            if clicked_clean in df_year["County"].values:
                st.session_state.selected_county = clicked_clean
                st.rerun()
            
     st.info("Darker regions indicate higher values of the selected indicator.")
     st.success("Learning Insight: Spatial disparities highlight regional inequalities.")
    
     # Click interaction feedback
     st.subheader("Selected County Insights")
    
     county_list = df_year["County"].tolist()
    
    # --- 1. HANDLE MAP CLICK FIRST ---
     # --- HANDLE MAP CLICK ---
     if map_data and map_data.get("last_object_clicked"):
        clicked = map_data["last_object_clicked"].get("properties", {}).get("NAME_1")
    
        if clicked:
            clicked_clean = clicked.strip()
    
            if clicked_clean in df_year["County"].values:
                st.session_state.selected_county = clicked_clean
    
    # --- 2. INITIALIZE STATE SAFELY ---
     if "selected_county" not in st.session_state:
        st.session_state.selected_county = county_list[0]
    
    # --- 3. ENSURE VALID VALUE ---
     if st.session_state.selected_county not in county_list:
        st.session_state.selected_county = county_list[0]
    
    # --- 4. DROPDOWN (SYNCED) ---
     selected = st.selectbox(
        "Select County",
        county_list,
        index=county_list.index(st.session_state.selected_county)
     )
    
    # --- 5. SYNC BACK ---
     st.session_state.selected_county = selected
    
    # --- 6. USE SINGLE SOURCE ---
     county_data = df_year[df_year["County"] == st.session_state.selected_county]
    
     st.write(f"### 📊 County Statistics for {st.session_state.selected_county}")
     st.write(county_data)
#------------------------
#Data Analyis
#----------------------------
with tab4:
    st.header("Data Analysis")

    selected = st.session_state.selected_county

    indicator = st.selectbox(
        "Indicator",
        ["Household_Income", "Poverty_Rate", "Agricultural_Output"]
    )

    trend = df[df["County"] == selected]

    st.line_chart(trend.set_index("Year")[indicator])
#-------------------------
# Policy Simulation
#------------------------
with tab5:
    st.header("Policy Simulation")

    df_year = df[df["Year"] == st.session_state.year]

    policy = st.selectbox("Policy", ["Agriculture", "Education", "Jobs"])
    intensity = st.slider("Intensity", 0, 50, 10)

    df_sim = df_year.copy()

    if policy == "Agriculture":
        df_sim["Agricultural_Output"] *= (1 + intensity/100)
    elif policy == "Education":
        df_sim["Education_Level"] *= (1 + intensity/100)
    elif policy == "Jobs":
        df_sim["Unemployment_Rate"] *= (1 - intensity/100)

    st.bar_chart(df_sim.set_index("County")["Poverty_Rate"])
    


import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np
import json
import os
import branca.colormap as cm
from folium.plugins import MarkerCluster

# ✅ ONLY ONCE
st.set_page_config(page_title="GeoStatLab", page_icon="📊", layout="wide")

data = {'time': pd.Timestamp.now()}
# default=str converts the Timestamp object to a string automatically
json_string = json.dumps(data, default=str)

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

# --- PANEL DATA GENERATION ---
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


csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Multi-Year Dataset",
    csv,
    "geostatlab_panel_data.csv",
    "text/csv"
)
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
county_list = sorted(df["County"].unique())

if "selected_county" not in st.session_state:
    st.session_state.selected_county = county_list[0]

if "year" not in st.session_state:
    st.session_state.year = df["Year"].max()
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
# INTERACTIVE MAP
# -------------------------
with tab3:
    #elif module == "🗺️ Interactive Map":
 st.header("Kenya Spatial Analysis")
 
 years = sorted(df["Year"].unique())

 selected_year = st.slider(
    "📅 Select Year",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=int(max(years)),
    step=1
 )
 df_year = df[df["Year"] == selected_year]
    
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
 
 df_year["County"] = df_year["County"].str.strip()
 
 if "selected_county" not in st.session_state:
   st.session_state.selected_county = df_year["County"].iloc[0]
    
 # Create lookup from dataframe
 data_lookup = df_year.set_index("County")[indicator].to_dict()

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
 min_val = df_year[indicator].min()
 max_val = df_year[indicator].max()
 colormap = cm.linear.YlOrRd_09.scale(min_val, max_val)
 colormap.caption = indicator

 m = folium.Map(location=[0.5, 37.8], zoom_start=6)

 folium.Choropleth(
     geo_data=geojson,
     data=df_year,
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
    name="Counties",
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
        sticky=True
    )
 ).add_to(m)

 
 
 #Render the map
 #st_folium(m, width=900, height=500)
 # Add markers with detailed info
 #import numpy as np

 def get_centroid(feature):
    coords = feature["geometry"]["coordinates"]

    # Handle MultiPolygon
    if feature["geometry"]["type"] == "MultiPolygon":
        coords = coords[0][0]
    else:  # Polygon
        coords = coords[0]

    lons = [point[0] for point in coords]
    lats = [point[1] for point in coords]

    return [np.mean(lats), np.mean(lons)]

 centroid_lookup = {}

 for feature in geojson["features"]:
    county_name = feature["properties"]["NAME_1"].strip()
    centroid_lookup[county_name] = get_centroid(feature)
    
 for _, row in df_year.iterrows():
    county = row["County"]

 if county in centroid_lookup:
        folium.Marker(
            location=centroid_lookup[county],
            popup=f"""
            <b>{county}</b><br>
            Income: {row['Household_Income']:,}<br>
            Poverty: {row['Poverty_Rate']:.2f}<br>
            Agriculture: {row['Agricultural_Output']:,}<br>
            Education: {row['Education_Level']:.2f}
            """
        ).add_to(m)
     
 marker_cluster = MarkerCluster().add_to(m)

 min_val = df_year[indicator].min()
 max_val = df_year[indicator].max()

 def scale_radius(value):
    return 5 + 15 * ((value - min_val) / (max_val - min_val + 1e-6))

 for _, row in df_year.iterrows():
    county = row["County"]
    value = row[indicator]

    if county in centroid_lookup:
        color = colormap(value)

        folium.CircleMarker(
            location=centroid_lookup[county],
            radius=scale_radius(value),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"""
            <b>{county}</b><br>
            {indicator}: {value}
            """
        ).add_to(marker_cluster)
        #colormap.add_to(m)
 folium.LayerControl().add_to(m)
 map_data = st_folium(m, width=900, height=500)
 
 if map_data and map_data.get("last_object_clicked"):
    clicked = map_data["last_object_clicked"].get("properties", {}).get("NAME_1")

    if clicked:
        clicked_clean = clicked.strip()

        if clicked_clean in df_year["County"].values:
            st.session_state.selected_county = clicked_clean
            st.rerun()
        
 st.info("Darker regions indicate higher values of the selected indicator.")
 st.success("Learning Insight: Spatial disparities highlight regional inequalities.")

 # Click interaction feedback
 st.subheader("Selected County Insights")

 county_list = df_year["County"].tolist()

# --- 1. HANDLE MAP CLICK FIRST ---
 # --- HANDLE MAP CLICK ---
 if map_data and map_data.get("last_object_clicked"):
    clicked = map_data["last_object_clicked"].get("properties", {}).get("NAME_1")

    if clicked:
        clicked_clean = clicked.strip()

        if clicked_clean in df_year["County"].values:
            st.session_state.selected_county = clicked_clean

# --- 2. INITIALIZE STATE SAFELY ---
 if "selected_county" not in st.session_state:
    st.session_state.selected_county = county_list[0]

# --- 3. ENSURE VALID VALUE ---
 if st.session_state.selected_county not in county_list:
    st.session_state.selected_county = county_list[0]

# --- 4. DROPDOWN (SYNCED) ---
 selected = st.selectbox(
    "Select County",
    county_list,
    index=county_list.index(st.session_state.selected_county)
 )

# --- 5. SYNC BACK ---
 st.session_state.selected_county = selected

# --- 6. USE SINGLE SOURCE ---
 county_data = df_year[df_year["County"] == st.session_state.selected_county]

 st.write(f"### 📊 County Statistics for {st.session_state.selected_county}")
 st.write(county_data)
# -------------------------
# Data Analysis
# -------------------------
with tab4:
    #elif module == "📈 Data Analysis":
  st.header("⚙️ Policy Simulation")

  policy = st.selectbox("Policy", ["Agriculture", "Education", "Jobs"])
  intensity = st.slider("Intensity", 0, 50, 10)

  df_sim = df_year.copy()

  if policy == "Agriculture":
    df_sim["Agricultural_Output"] *= (1 + intensity/100)

  elif policy == "Education":
    df_sim["Education_Level"] *= (1 + intensity/100)

  elif policy == "Jobs":
    df_sim["Unemployment_Rate"] *= (1 - intensity/100)

  st.bar_chart(df_sim.set_index("County")[indicator])
  play = st.checkbox("▶️ Play Time Animation")

  if play:
    import time
    for y in years:
        st.session_state["year"] = y
        time.sleep(0.5)
        st.rerun()
  
  st.bar_chart(df.set_index("County")[indicator])
  
  st.markdown("### Insights")

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

  selected = st.session_state.selected_county

  trend_data = df[df["County"] == selected]

  st.line_chart(
    trend_data.set_index("Year")[indicator]
  )  
  
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
# Policy Simulation
# -------------------------
with tab5:
    #elif module == "🏛️ Policy Simulation":
  st.header("⚙️ Policy Simulation")

  policy = st.selectbox("Policy", ["Agriculture", "Education", "Jobs"])
  intensity = st.slider("Intensity", 0, 50, 10)

  df_sim = df_year.copy()

  if policy == "Agriculture":
    df_sim["Agricultural_Output"] *= (1 + intensity/100)

  elif policy == "Education":
    df_sim["Education_Level"] *= (1 + intensity/100)

  elif policy == "Jobs":
    df_sim["Unemployment_Rate"] *= (1 - intensity/100)

  st.bar_chart(df_sim.set_index("County")[indicator])
  
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
