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


# -------------------------
# PANEL DATA
# -------------------------
years = list(range(2018, 2025))
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

df = pd.DataFrame(panel).sort_values(["County", "Year"])


