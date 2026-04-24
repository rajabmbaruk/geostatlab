def generate_ai_insights(df, indicator):
    top = df.loc[df[indicator].idxmax()]
    bottom = df.loc[df[indicator].idxmin()]

    return {
        "summary": f"{top['County']} leads in {indicator}, while {bottom['County']} lags.",
        "policy_signal": (
            "High inequality detected → targeted intervention recommended"
            if df[indicator].std() > df[indicator].mean()*0.3
            else "Moderate disparity levels"
        ),
        "trend_signal": (
            "Volatile system detected"
            if df[indicator].max() - df[indicator].min() > df[indicator].mean()
            else "Stable distribution"
        )
    }
st.subheader("🧠 AI Insights Panel")
st.info(ins["summary"])
st.warning(ins["risk"])
st.success(ins["policy_hint"])
