import pandas as pd
import numpy as np
import os

def generate_knbs_data():
    counties = ["Nairobi", "Kiambu", "Mombasa", "Kisumu", "Machakos"]
    years = list(range(2018, 2025))

    rows = []

    for county in counties:
        base_income = np.random.randint(40000, 120000)
        base_pop = np.random.randint(500000, 3000000)

        for year in years:
            row = {
                "County": county,
                "Year": year,
                "Household_Income": float(base_income * (1 + 0.04 * (year - 2018))),
                "Poverty_Rate": float(np.random.uniform(0.15, 0.45)),
                "Agricultural_Output": float(np.random.uniform(50, 200)),
                "Education_Level": float(np.random.uniform(0.3, 0.8)),
                "Unemployment_Rate": float(np.random.uniform(0.05, 0.25)),
                "Population": int(base_pop)
            }
            rows.append(row)

    return pd.DataFrame(rows)


def load_data(path=None):
    try:
        if path and os.path.exists(path):
            df = pd.read_csv(path)
        else:
            df = generate_knbs_data()

        # enforce schema safety
        required = [
            "County", "Year", "Household_Income",
            "Poverty_Rate", "Agricultural_Output",
            "Education_Level", "Unemployment_Rate",
            "Population"
        ]

        missing = [c for c in required if c not in df.columns]

        if missing:
            raise ValueError(f"Missing columns: {missing}")

        return df

    except Exception as e:
        raise RuntimeError(f"Data loading failed: {str(e)}")
        
def load_geojson():
    path = "data/kenya_counties.geojson"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing geojson: {path}")

    import json
    with open(path, "r") as f:
        return json.load(f)



