def smart_insights(df):
    insights = []

    if df["Education_Level"].mean() > 0.6:
        insights.append("Higher education improves outcomes.")

    if df["Poverty_Rate"].mean() > 0.3:
        insights.append("Poverty remains high → intervention needed.")

    if df["Unemployment_Rate"].mean() < 0.1:
        insights.append("Employment programs are effective.")

    return insights


def generate_insights(df, indicator):
    top = df.sort_values(indicator, ascending=False).iloc[0]
    bottom = df.sort_values(indicator, ascending=True).iloc[0]

    return f"""
🔍 AI Insights

• {top['County']} leads in {indicator}.  
• {bottom['County']} is lowest → needs intervention.  
• Strong regional inequality persists.
"""