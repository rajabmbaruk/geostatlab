import pandas as pd
import numpy as np
import os

REQUIRED_COLUMNS = [
    "County", "Year",
    "Household_Income",
    "Poverty_Rate",
    "Agricultural_Output",
    "Education_Level",
    "Unemployment_Rate",
    "Population"
]

def generate_knbs_like_data():
    counties = [
        "Nairobi", "Kiambu", "Mombasa", "Kisumu",
        "Machakos", "Uasin Gishu", "Narok", "Meru"
    ]

    years = list(range(2018, 2025))

    rows = []
    for c in counties:
        base_income = np.random.randint(40000, 120000)
        base_pop = np.random.randint(500000, 4000000)

        for y in years:
            rows.append({
                "County": c,
                "Year": y,
                "Household_Income": base_income * (1 + 0.04 * (y - 2018)),
                "Poverty_Rate": max(0.05, np.random.uniform(0.15, 0.45)),
                "Agricultural_Output": np.random.uniform(50, 200),
                "Education_Level": np.clip(np.random.uniform(0.3, 0.8), 0, 1),
                "Unemployment_Rate": np.random.uniform(0.05, 0.25),
                "Population": base_pop
            })

    return pd.DataFrame(rows)


def validate_dataset(df: pd.DataFrame):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    if df.duplicated(subset=["County", "Year"]).any():
        raise ValueError("Duplicate County-Year pairs detected")

    return True


def load_data(path=None):
    try:
        if path and os.path.exists(path):
            df = pd.read_csv(path)
        else:
            df = generate_knbs_like_data()

        validate_dataset(df)
        return df

    except Exception as e:
        raise RuntimeError(f"Dataset loading failed: {e}")
def load_geojson():
    path = "data/kenya_counties.geojson"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing geojson: {path}")

    import json
    with open(path, "r") as f:
        return json.load(f)



