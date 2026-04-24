import pandas as pd

REQUIRED_COLUMNS = [
    "County", "Year", "Population",
    "Household_Income", "Poverty_Rate",
    "Unemployment_Rate", "Education_Level",
    "Agricultural_Output"
]


def validate_dataset(df: pd.DataFrame):
    errors = []

    # -------------------------
    # 1. Normalize columns (CRITICAL FIX)
    # -------------------------
    df.columns = df.columns.str.strip()

    # -------------------------
    # 2. Schema check
    # -------------------------
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_cols:
        raise ValueError(
            f"""
❌ DATA VALIDATION FAILED
Missing columns: {missing_cols}

👉 Actual columns found:
{list(df.columns)}
"""
        )

    # -------------------------
    # 3. Safe duplicated check
    # -------------------------
    try:
        if df[["County", "Year"]].duplicated().any():
            errors.append("Duplicate County-Year records detected")
    except KeyError as e:
        raise ValueError(
            f"""
❌ DUPLICATE CHECK FAILED

Reason: {e}

👉 Columns available:
{list(df.columns)}
"""
        )

    # -------------------------
    # 4. Missing values
    # -------------------------
    if df.isnull().sum().sum() > 0:
        errors.append("Dataset contains missing values")

    # -------------------------
    # 5. Range validation
    # -------------------------
    if "Poverty_Rate" in df.columns:
        if ((df["Poverty_Rate"] < 0) | (df["Poverty_Rate"] > 1)).any():
            errors.append("Poverty_Rate out of range (0–1)")

    if "Unemployment_Rate" in df.columns:
        if ((df["Unemployment_Rate"] < 0) | (df["Unemployment_Rate"] > 1)).any():
            errors.append("Unemployment_Rate out of range (0–1)")

    if "Education_Level" in df.columns:
        if ((df["Education_Level"] < 0) | (df["Education_Level"] > 1)).any():
            errors.append("Education_Level out of range (0–1)")

    # -------------------------
    # FINAL RESULT
    # -------------------------
    if errors:
        raise ValueError("DATA VALIDATION FAILED:\n" + "\n".join(errors))

    return True





