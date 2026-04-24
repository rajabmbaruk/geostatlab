import pandas as pd

def validate_dataset(df):
    errors = []

    required_columns = [
        "County",
        "Year",
        "Population",
        "Household_Income",
        "Poverty_Rate",
        "Agricultural_Output",
        "Education_Level",
        "Unemployment_Rate"
    ]

    # -------------------------
    # CHECK COLUMNS
    # -------------------------
    for col in required_columns:
        if col not in df.columns:
            errors.append(f"Missing column: {col}")

    # -------------------------
    # CHECK NULLS
    # -------------------------
    if df.isnull().sum().sum() > 0:
        errors.append("Dataset contains missing values")

    # -------------------------
    # RANGE CHECKS
    # -------------------------
    if (df["Poverty_Rate"] < 0).any() or (df["Poverty_Rate"] > 1).any():
        errors.append("Poverty_Rate out of bounds (0–1)")

    if (df["Education_Level"] < 0).any() or (df["Education_Level"] > 1).any():
        errors.append("Education_Level out of bounds (0–1)")

    if (df["Unemployment_Rate"] < 0).any():
        errors.append("Negative unemployment values")

    # -------------------------
    # DUPLICATES
    # -------------------------
    if df.duplicated(subset=["County", "Year"]).any():
        errors.append("Duplicate County-Year records")

    # -------------------------
    # OUTPUT
    # -------------------------
    if errors:
        return False, errors

    return True, ["Dataset is valid"]
