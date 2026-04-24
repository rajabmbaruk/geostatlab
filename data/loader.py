import pandas as pd
import os
import json
import streamlit as st

def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # go one level up from /data/
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))

    path = os.path.join(root_dir, "geostatlab_data.csv")

    if not os.path.exists(path):
        st.error(f"Dataset not found at: {path}")
        return pd.DataFrame()

    return pd.read_csv(path)

def load_geojson():
    path = os.path.join(os.path.dirname(__file__), "kenya_counties.geojson")

    if not os.path.exists(path):
        st.error("Missing GeoJSON file")
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
        
