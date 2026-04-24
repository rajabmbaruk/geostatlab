def generate_report(df, year):
    return f"""
    GeoStatLab Analytical Report - {year}

    - Total Counties: {df['County'].nunique()}
    - Avg Income: {df['Household_Income'].mean():,.2f}
    - Avg Poverty: {df['Poverty_Rate'].mean():.2%}

    Key Insight:
    Spatial inequality remains a key development challenge.
    """
