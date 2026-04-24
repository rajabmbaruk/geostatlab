import pandas as pd
import os
import json
import streamlit as st

def load_data():
    path = os.path.join(os.path.dirname(__file__), "geostatlab_data.csv")
    return pd.read_csv(path)

def load_geojson():
    path = os.path.join(os.path.dirname(__file__), "kenya_counties.geojson")

    if not os.path.exists(path):
        st.error("Missing GeoJSON file")
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
        
