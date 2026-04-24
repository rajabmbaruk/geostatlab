import pandas as pd
import json
import os

def load_data():
    return pd.read_csv("geostatlab_data.csv")

def load_geojson():
    path = os.path.join("assets", "kenya_counties.geojson")
    with open(path) as f:
        return json.load(f)