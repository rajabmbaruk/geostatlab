import streamlit as st

def generate_insights(df, indicator):
    top = df.loc[df[indicator].idxmax()]
    bottom = df.loc[df[indicator].idxmin()]

    return {
        "summary": f"{top['County']} leads in {indicator}. {bottom['County']} lags behind.",
        "risk": "High inequality detected" if df[indicator].std() > 0.2 else "Stable distribution",
        "policy_hint": "Target bottom counties for intervention"
    }
from core.insights import generate_insights

ins = generate_insights(df, "Household_Income")

st.subheader("🧠 AI Insights Panel")
st.info(ins["summary"])
st.warning(ins["risk"])
st.success(ins["policy_hint"])
