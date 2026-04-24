# data/loader.py
import pandas as pd
import os
from data.knbs_generator import generate_knbs_dataset
from data.validator import validate_dataset

DATA_PATH = "data/geostatlab_data.csv"


def load_data():
    """
    Loads dataset if available.
    Otherwise generates KNBS-style synthetic panel data.
    """

    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        df = generate_knbs_dataset()
        os.makedirs("data", exist_ok=True)
        df.to_csv(DATA_PATH, index=False)

    # Validate before returning
    validate_dataset(df)

    return df

    df.columns = df.columns.str.strip()
    
    # normalize naming (CRITICAL FIX)
    df.columns = [
        c.strip().title().replace(" ", "_")
        for c in df.columns
    ]


def load_geojson():
    path = "data/kenya_counties.geojson"

    if not os.path.exists(path):
        raise FileNotFoundError(
            "Missing geojson file: kenya_counties.geojson"
        )

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
