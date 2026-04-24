import pandas as pd

REQUIRED_COLUMNS = [
    "County", "Year", "Population",
    "Household_Income", "Poverty_Rate",
    "Unemployment_Rate", "Education_Level",
    "Agricultural_Output"
]


def validate_dataset(df: pd.DataFrame):
    errors = []

    # 1. Schema check
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")

    # 2. Missing values
    if df.isnull().sum().sum() > 0:
        errors.append("Dataset contains missing values")

    # 3. Range validation (KNBS realism rules)
    if (df["Poverty_Rate"] < 0).any() or (df["Poverty_Rate"] > 1).any():
        errors.append("Poverty_Rate out of range (0–1)")

    if (df["Unemployment_Rate"] < 0).any() or (df["Unemployment_Rate"] > 1).any():
        errors.append("Unemployment_Rate out of range (0–1)")

    if (df["Education_Level"] < 0).any() or (df["Education_Level"] > 1).any():
        errors.append("Education_Level out of range (0–1)")

    # 4. Duplicate check
    if df.duplicated(subset=["County", "Year"]).any():
        errors.append("Duplicate County-Year records detected")

    # 5. Year sanity check
    if df["Year"].min() < 2010 or df["Year"].max() > 2030:
        errors.append("Year range unrealistic")

    if errors:
        raise ValueError("DATA VALIDATION FAILED:\n" + "\n".join(errors))

    return True


