import streamlit as st

def generate_insights(df, indicator):
    top = df.loc[df[indicator].idxmax()]
    bottom = df.loc[df[indicator].idxmin()]

    return {
        "summary": f"{top['County']} leads in {indicator}. {bottom['County']} lags behind.",
        "risk": "High inequality detected" if df[indicator].std() > 0.2 else "Stable distribution",
        "policy_hint": "Target bottom counties for intervention"
    }
