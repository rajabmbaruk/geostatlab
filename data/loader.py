import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_PATH = BASE / "assets" / "geostatlab_data.csv"
GEO_PATH = BASE / "assets" / "kenya_counties.geojson"

def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing dataset: {DATA_PATH}")
    return pd.read_csv(DATA_PATH)

def load_geojson():
    if not GEO_PATH.exists():
        raise FileNotFoundError(f"Missing geojson: {GEO_PATH}")
    return GEO_PATH.read_text()
