import pandas as pd


def generate_ai_insights(df: pd.DataFrame, indicator: str = None):
    """
    AI-style narrative insights engine (KNBS-style analytics)
    """

    if df is None or df.empty:
        return ["No data available for analysis."]

    insights = []

    # -------------------------
    # BASIC STATISTICAL INSIGHTS
    # -------------------------
    if indicator and indicator in df.columns:
        top = df.loc[df[indicator].idxmax()]
        bottom = df.loc[df[indicator].idxmin()]

        insights.append(
            f"{top['County']} leads in {indicator}, indicating strong socio-economic performance."
        )

        insights.append(
            f"{bottom['County']} shows lowest {indicator}, suggesting need for targeted intervention."
        )

    # -------------------------
    # MACRO PATTERNS
    # -------------------------
    if "Poverty_Rate" in df.columns:
        if df["Poverty_Rate"].mean() > 0.3:
            insights.append("High poverty levels persist across regions.")

    if "Education_Level" in df.columns:
        if df["Education_Level"].mean() > 0.6:
            insights.append("Education levels are improving nationally.")

    if "Unemployment_Rate" in df.columns:
        if df["Unemployment_Rate"].mean() > 0.1:
            insights.append("Unemployment remains a structural challenge.")

    # -------------------------
    # DISPARITY CHECK
    # -------------------------
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:
        variance = df[numeric_cols].std().mean()

        if variance > 0.2:
            insights.append("High regional disparity detected across indicators.")
        else:
            insights.append("Indicators show moderate regional balance.")

    return insights
