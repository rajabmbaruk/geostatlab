import streamlit as st
import pandas as pd


def show_policy(df, year, geojson=None):
    """
    Policy Simulation Module (KNBS-style)
    """

    st.header("⚙️ Policy Simulation Dashboard")

    if df is None or df.empty:
        st.error("Dataset not available.")
        return

    # -------------------------
    # FILTER YEAR
    # -------------------------
    df_year = df[df["Year"] == year]

    # -------------------------
    # POLICY CONTROLS
    # -------------------------
    policy = st.selectbox(
        "Select Policy",
        ["Agriculture Boost", "Education Investment", "Employment Program"]
    )

    intensity = st.slider("Policy Intensity (%)", 0, 50, 10)

    # -------------------------
    # APPLY POLICY EFFECTS
    # -------------------------
    df_policy = df_year.copy()

    if policy == "Agriculture Boost":
        if "Agricultural_Output" in df_policy.columns:
            df_policy["Agricultural_Output"] *= (1 + intensity / 100)

    elif policy == "Education Investment":
        if "Education_Level" in df_policy.columns:
            df_policy["Education_Level"] *= (1 + intensity / 100)

    elif policy == "Employment Program":
        if "Unemployment_Rate" in df_policy.columns:
            df_policy["Unemployment_Rate"] *= (1 - intensity / 100)

    # -------------------------
    # KPI COMPARISON
    # -------------------------
    st.subheader("📊 Policy Impact Summary")

    col1, col2 = st.columns(2)

    numeric_cols = df_year.select_dtypes("number").columns

    if len(numeric_cols) > 0:
        metric = numeric_cols[0]

        before = df_year[metric].mean()
        after = df_policy[metric].mean()

        col1.metric("Before Policy", f"{before:.2f}")
        col2.metric("After Policy", f"{after:.2f}", delta=f"{after - before:.2f}")

    # -------------------------
    # TOP IMPACT COUNTIES
    # -------------------------
    st.subheader("🏆 Impact Analysis")

    if len(numeric_cols) > 0:
        metric = numeric_cols[0]

        df_policy["Change"] = df_policy[metric] - df_year[metric]

        st.write("Top Improvements")
        st.dataframe(df_policy.sort_values("Change", ascending=False).head(5))

        st.write("Top Declines")
        st.dataframe(df_policy.sort_values("Change").head(5))
