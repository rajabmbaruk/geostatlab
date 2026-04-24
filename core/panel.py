import pandas as pd
import numpy as np

def generate_panel(df_base, start=2018, end=2024, seed=42):
    np.random.seed(seed)

    years = list(range(start, end + 1))
    panel = []

    for _, row in df_base.iterrows():
        for i, year in enumerate(years):
            r = row.copy()

            # Add time
            r["Year"] = year

            # Controlled growth models (realistic)
            r["Household_Income"] *= (1 + 0.04 * i)  # steady growth
            r["Poverty_Rate"] *= (1 - 0.015 * i)     # gradual reduction

            # Agriculture fluctuates
            r["Agricultural_Output"] *= (
                1 + np.random.normal(0.02, 0.05)
            )

            # Education improves slowly (bounded)
            r["Education_Level"] = min(
                1.0,
                r["Education_Level"] * (1 + 0.01 * i)
            )

            # Unemployment noisy
            r["Unemployment_Rate"] *= (
                1 + np.random.normal(0, 0.03)
            )

            panel.append(r)

    df = pd.DataFrame(panel)

    return df.sort_values(["County", "Year"])
