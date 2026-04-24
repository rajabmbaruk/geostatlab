import numpy as np
import pandas as pd

def generate_knbs_dataset():
    np.random.seed(42)

    counties = [
        "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Kiambu",
        "Machakos", "Uasin Gishu", "Kakamega", "Meru", "Turkana"
    ]

    years = list(range(2018, 2025))

    rows = []

    for county in counties:
        base_income = np.random.randint(30000, 120000)
        base_poverty = np.random.uniform(0.2, 0.6)
        base_unemployment = np.random.uniform(0.1, 0.3)
        base_edu = np.random.uniform(0.4, 0.8)
        base_agri = np.random.randint(50, 200)

        for i, year in enumerate(years):
            rows.append({
                "County": county,
                "Year": year,

                # KNBS-style indicators
                "Population": int(np.random.randint(500000, 5000000)),
                "Household_Income": base_income * (1 + 0.05 * i) + np.random.randint(-2000, 2000),
                "Poverty_Rate": max(0, base_poverty - 0.02 * i + np.random.uniform(-0.02, 0.02)),
                "Unemployment_Rate": max(0, base_unemployment - 0.01 * i + np.random.uniform(-0.01, 0.01)),
                "Education_Level": min(1, base_edu + 0.015 * i + np.random.uniform(-0.02, 0.02)),
                "Agricultural_Output": base_agri * (1 + np.random.uniform(-0.1, 0.1)),
            })

    df = pd.DataFrame(rows)

    # enforce types
    df["Year"] = df["Year"].astype(int)

    return df
