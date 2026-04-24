import pandas as pd

REQUIRED_COLUMNS = [
    "County", "Year", "Population",
    "Household_Income", "Poverty_Rate",
    "Unemployment_Rate", "Education_Level",
    "Agricultural_Output"
]


def validate_dataset(df: pd.DataFrame):
    """
    Runs validation ONLY when called (NOT on import)
    """

    df.columns = df.columns.str.strip()

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]

    if missing:
        raise ValueError(
            f"""
❌ DATA VALIDATION FAILED

Missing columns: {missing}

Available columns:
{list(df.columns)}
"""
        )

    if df[["County", "Year"]].duplicated().any():
        raise ValueError("Duplicate County-Year records detected")

    return True
