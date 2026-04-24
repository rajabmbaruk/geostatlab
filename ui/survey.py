import streamlit as st
import pandas as pd
import numpy as np


def show_survey(df):
    """
    Survey Simulation Module (GeoStatLab)
    KNBS-style sampling demonstration
    """

    st.header("🧪 Survey Simulation Lab")

    st.markdown("""
    Explore how sampling affects statistical accuracy in national datasets.
    """)

    # -------------------------
    # VALIDATION
    # -------------------------
    if df is None or len(df) == 0:
        st.error("Dataset not loaded properly.")
        return

    required_cols = ["County", "Year"]
    for col in required_cols:
        if col not in df.columns:
            st.error(f"Missing required column: {col}")
            return

    # -------------------------
    # CONTROLS
    # -------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        sample_size = st.slider(
            "Sample Size",
            min_value=5,
            max_value=len(df),
            value=20,
            key="survey_sample_size"
        )

    with col2:
        method = st.selectbox(
            "Sampling Method",
            ["Simple Random", "Stratified", "Cluster", "Systematic"],
            key="survey_method"
        )

    with col3:
        indicator = st.selectbox(
            "Indicator",
            ["Household_Income", "Poverty_Rate", "Agricultural_Output",
             "Education_Level", "Unemployment_Rate"],
            key="survey_indicator"
        )

    # -------------------------
    # SAMPLING LOGIC
    # -------------------------
    size = min(sample_size, len(df))

    if method == "Simple Random":
        sample = df.sample(n=size, random_state=42)

    elif method == "Stratified":
        sample = df.groupby("County", group_keys=False).apply(
            lambda x: x.sample(max(1, size // df["County"].nunique()), random_state=42)
        )

    elif method == "Cluster":
        clusters = np.random.choice(
            df["County"].unique(),
            size=min(3, df["County"].nunique()),
            replace=False
        )
        sample = df[df["County"].isin(clusters)]

    elif method == "Systematic":
        k = max(1, len(df) // size)
        sample = df.iloc[::k].head(size)

    # -------------------------
    # DISPLAY SAMPLE
    # -------------------------
    st.subheader("📋 Sample Data")
    st.dataframe(sample)

    # -------------------------
    # STATISTICS
    # -------------------------
    pop_mean = df[indicator].mean()
    sample_mean = sample[indicator].mean()

    st.subheader("📊 Population vs Sample")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Population Mean", f"{pop_mean:,.2f}")

    with col2:
        st.metric(
            "Sample Mean",
            f"{sample_mean:,.2f}",
            delta=f"{sample_mean - pop_mean:,.2f}"
        )

    # -------------------------
    # VISUAL COMPARISON
    # -------------------------
    chart_df = pd.DataFrame({
        "Type": ["Population", "Sample"],
        "Mean": [pop_mean, sample_mean]
    })

    st.bar_chart(chart_df.set_index("Type"))

    # -------------------------
    # BIAS CHECK
    # -------------------------
    st.subheader("💡 Sampling Quality")

    diff = abs(sample_mean - pop_mean)

    if diff < 0.05 * pop_mean:
        st.success("✅ High representativeness")
    elif diff < 0.15 * pop_mean:
        st.warning("⚠️ Moderate sampling bias")
    else:
        st.error("❌ High sampling bias")

    # -------------------------
    # EXPLANATION
    # -------------------------
    with st.expander("📘 Method Explanation"):
        if method == "Simple Random":
            st.write("Each unit has equal chance of selection.")
        elif method == "Stratified":
            st.write("Ensures representation across counties.")
        elif method == "Cluster":
            st.write("Selects entire counties as clusters.")
        elif method == "Systematic":
            st.write("Selects every k-th record from dataset.")

    # -------------------------
    # DOWNLOAD
    # -------------------------
    csv = sample.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Sample",
        csv,
        "survey_sample.csv",
        "text/csv"
    )



