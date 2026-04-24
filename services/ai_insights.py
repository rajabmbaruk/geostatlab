import streamlit as st

def generate_ai_insights(df, indicator):
    top = df.loc[df[indicator].idxmax()]
    bottom = df.loc[df[indicator].idxmin()]

    return f"""
### 🧠 AI INSIGHTS

- {top['County']} leads in {indicator}
- {bottom['County']} is lowest performing

📊 Pattern detected:
Regional inequality persists across counties.

📌 Recommendation:
Target bottom counties with sector-specific investment.
"""
    
def generate_ai_insights(df, year, indicator):

    df_year = df[df["Year"] == year]

    top = df_year.sort_values(indicator, ascending=False).iloc[0]
    bottom = df_year.sort_values(indicator, ascending=True).iloc[0]

    mean_val = df_year[indicator].mean()
    std_val = df_year[indicator].std()

    insights = []

    # 1. Leadership insight
    insights.append(
        f"🏆 {top['County']} leads in {indicator}, indicating strong structural advantage."
    )

    # 2. Weakest region insight
    insights.append(
        f"⚠️ {bottom['County']} shows lowest performance, suggesting targeted intervention is needed."
    )

    # 3. inequality signal
    if std_val > mean_val * 0.3:
        insights.append(
            "📊 High regional inequality detected across counties."
        )
    else:
        insights.append(
            "📊 Moderate equality observed across regions."
        )

    # 4. policy hint
    if indicator == "Unemployment_Rate":
        insights.append("💼 Job creation policies would have highest impact here.")
    elif indicator == "Poverty_Rate":
        insights.append("🎯 Social protection programs recommended.")
    elif indicator == "Education_Level":
        insights.append("🎓 Education investment will yield long-term gains.")

    return insights
