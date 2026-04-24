import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def load_data():
    path = os.path.join(BASE_DIR, "data", "geostatlab_data.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing dataset: {path}")
    return pd.read_csv(path)

def load_geojson():
    path = os.path.join(BASE_DIR, "data", "kenya_counties.geojson")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing geojson: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
        
