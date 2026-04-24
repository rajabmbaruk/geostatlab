import pandas as pd
import os
from data.validator import validate_dataset

DATA_PATH = "data/geostatlab_data.csv"

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Missing dataset file at: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    # normalize columns (CRITICAL FIX)
    df.columns = df.columns.str.strip()

    required_cols = [
        "County", "Year",
        "Household_Income",
        "Poverty_Rate",
        "Agricultural_Output",
        "Education_Level",
        "Unemployment_Rate"
    ]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    validate_dataset(df)
    return df


def load_geojson():
    path = "data/kenya_counties.geojson"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing geojson: {path}")

    import json
    with open(path, "r") as f:
        return json.load(f)



