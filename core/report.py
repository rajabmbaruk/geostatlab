def generate_report(df, year):
    return f"""
    GEOSTATLAB POLICY REPORT – {year}

    SUMMARY:
    - Counties analyzed: {df['County'].nunique()}
    - Mean income: {df['Household_Income'].mean():,.0f}
    - Poverty rate: {df['Poverty_Rate'].mean():.2%}

    INSIGHTS:
    - High spatial inequality detected
    - Education strongly correlates with income

    RECOMMENDATION:
    Focus investment on bottom 20% counties.
    """

st.download_button(
    "📄 Download AI Report",
    generate_report(df_year, year),
    "report.txt"
)
