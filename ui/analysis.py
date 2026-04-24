import streamlit as st
import pandas as pd
import numpy as np


# -----------------------------
# SAFE STATE ACCESS
# -----------------------------
def get_state(key, default=None):
    return st.session_state.get(key, default)


# -----------------------------
# CORE ANALYTICS ENGINE
# -----------------------------
def compute_summary(df: pd.DataFrame, year: int):
    df_year = df[df["Year"] == year].copy()

    numeric_cols = df_year.select_dtypes(include=np.number).columns.tolist()

    if not numeric_cols:
        return None, None

    summary = df_year[numeric_cols].describe().T
    summary["missing"] = df_year[numeric_cols].isna().sum()

    return df_year, summary


# -----------------------------
# MAIN UI FUNCTION
# -----------------------------
def show_analysis(df: pd.DataFrame):
    st.header("📊 Data Analysis Dashboard")

    # SAFE STATE
    year = get_state("year", 2024)
    indicator = get_state("global_indicator", None)

    if df is None or df.empty:
        st.error("Dataset is empty or missing.")
        return

    if "Year" not in df.columns:
        st.error("Missing Year column")
        return

    # FILTER DATA
    df_year, summary = compute_summary(df, year)

    if df_year is None:
        st.warning("No numeric columns found for analysis.")
        return

    # -----------------------------
    # KPI SECTION
    # -----------------------------
    st.subheader(f"📅 Year: {year}")

    col1, col2, col3 = st.columns(3)

    col1.metric("Records", len(df_year))
    col2.metric("Columns", len(df_year.columns))
    col3.metric("Numeric Features", len(summary))

    st.divider()

    # -----------------------------
    # SUMMARY STATISTICS
    # -----------------------------
    st.subheader("📈 Statistical Summary")

    st.dataframe(summary, use_container_width=True)

    # -----------------------------
    # INDICATOR ANALYSIS
    # -----------------------------
    st.subheader("🎯 Indicator Insights")

    if indicator and indicator in df_year.columns:
        col1, col2 = st.columns(2)

        mean_val = df_year[indicator].mean()
        std_val = df_year[indicator].std()

        col1.metric("Mean", f"{mean_val:.2f}")
        col2.metric("Std Dev", f"{std_val:.2f}")

        st.line_chart(df_year[indicator])

    else:
        st.info("Select a valid indicator to view trend analysis.")

    # -----------------------------
    # OUTLIER DETECTION (LIGHTWEIGHT)
    # -----------------------------
    st.subheader("🚨 Outlier Detection")

    if indicator and indicator in df_year.columns:
        q1 = df_year[indicator].quantile(0.25)
        q3 = df_year[indicator].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df_year[
            (df_year[indicator] < lower) |
            (df_year[indicator] > upper)
        ]

        st.write(f"Detected {len(outliers)} outliers")
        st.dataframe(outliers)

    # -----------------------------
    # AI INSIGHT HOOK (FUTURE READY)
    # -----------------------------
    st.subheader("🧠 AI Insights (Preview Hook)")

    st.info(
        "AI module placeholder: integrate core.ai_insights.generate_ai_insights(df)"
    )
    
