import pandas as pd
import numpy as np

def build_panel(df_base, years):
    panel = []

    for _, row in df_base.iterrows():
        for i, year in enumerate(years):
            r = row.copy()
            r["Year"] = year

            r["Household_Income"] *= (1 + 0.05 * i)
            r["Poverty_Rate"] *= (1 - 0.02 * i)
            r["Agricultural_Output"] *= (1 + np.random.uniform(-0.1, 0.1))
            r["Education_Level"] = min(1, r["Education_Level"] * (1 + 0.015 * i))
            r["Unemployment_Rate"] *= (1 + np.random.uniform(-0.05, 0.05))

            panel.append(r)

    return pd.DataFrame(panel)