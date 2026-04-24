import pandas as pd
import os
from data.knbs_generator import generate_knbs_dataset
from data.validator import validate_dataset

DATA_PATH = "data/geostatlab_data.csv"


def load_data():

    # If file missing → generate fresh dataset
    if not os.path.exists(DATA_PATH):
        df = generate_knbs_dataset()
        os.makedirs("data", exist_ok=True)
        df.to_csv(DATA_PATH, index=False)
    else:
        df = pd.read_csv(DATA_PATH)

    # Normalize column names (CRITICAL FIX)
    df.columns = df.columns.str.strip()

    # Ensure KNBS schema consistency
    df.columns = [
        c.replace(" ", "_").title()
        for c in df.columns
    ]

    required_cols = [
        "County", "Year", "Population",
        "Household_Income", "Poverty_Rate",
        "Unemployment_Rate",
        "Education_Level",
        "Agricultural_Output"
    ]

    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        raise ValueError(
            f"""
❌ SCHEMA MISMATCH DETECTED

Missing columns: {missing}

Actual columns:
{list(df.columns)}

👉 FIX: delete dataset OR regenerate from generator
"""
        )

    validate_dataset(df)
    return df


def load_geojson():
    path = "data/kenya_counties.geojson"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing geojson: {path}")

    import json
    with open(path, "r") as f:
        return json.load(f)



