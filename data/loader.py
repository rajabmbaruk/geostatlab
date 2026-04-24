import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

GEO_PATH = BASE / "assets" / "kenya_counties.geojson"



def load_data():
    path = BASE / "assets" / "geostatlab_data.csv"

    if not path.exists():
        raise FileNotFoundError(f"Dataset missing at {path}")

    return pd.read_csv(path)

def load_geojson():
    if not GEO_PATH.exists():
        raise FileNotFoundError(f"Missing geojson: {GEO_PATH}")
    return GEO_PATH.read_text()
