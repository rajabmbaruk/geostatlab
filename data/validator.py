import pandas as pd

REQUIRED_COLUMNS = [
    "County", "Year", "Population",
    "Household_Income", "Poverty_Rate",
    "Unemployment_Rate", "Education_Level",
    "Agricultural_Output"
]


def validate_dataset(df):
    required = ["County", "Year"]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # FIX: safe duplication check
    if df.duplicated(subset=required).any():
        raise ValueError("Duplicate County-Year records found")

    # ensure types
    if not df["Year"].dtype.kind in "i":
        df["Year"] = df["Year"].astype(int)

    return True



