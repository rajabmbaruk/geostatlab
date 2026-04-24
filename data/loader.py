import pandas as pd
import json
import os

import os
import json
import streamlit as st

def load_geojson():
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, "kenya_counties.geojson")

    if not os.path.exists(path):
        st.error("GeoJSON file missing. Check deployment assets.")
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
        
