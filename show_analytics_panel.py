import streamlit as st
import pandas as pd


def show_analytics_panel(df: pd.DataFrame):
    """
    Advanced KNBS-style analytics panel (filters + KPIs + trends)
    """

    st.subheader("📊 Interactive Analytics Dashboard")

    # -------------------------
    # VALIDATION
    # -------------------------
    required_cols = ["Year", "County"]
    for col in required_cols:
        if col not in df.columns:
            st.error(f"Missing required column: {col}")
            return

    # -------------------------
    # FILTERS (TOP BAR)
    # -------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_year = st.selectbox(
            "📅 Select Year",
            sorted(df["Year"].dropna().unique()),
            key="analytics_year"
        )

    with col2:
        counties = sorted(df["County"].dropna().unique())
        selected_counties = st.multiselect(
            "🏞️ Select Counties",
            counties,
            default=counties[:5],
            key="analytics_counties"
        )

    with col3:
        numeric_cols = df.select_dtypes("number").columns.tolist()

        default_indicator = "Household_Income" if "Household_Income" in numeric_cols else numeric_cols[0]

        indicator = st.selectbox(
            "📌 Focus Indicator",
            numeric_cols,
            index=numeric_cols.index(default_indicator) if default_indicator in numeric_cols else 0,
            key="analytics_indicator"
        )

    # -------------------------
    # FILTER DATA
    # -------------------------
    df_filtered = df[
        (df["Year"] == selected_year) &
        (df["County"].isin(selected_counties))
    ]

    if df_filtered.empty:
        st.warning("No data available for selected filters.")
        return

    st.markdown("---")

    # -------------------------
    # KPI CARDS
    # -------------------------
    st.subheader("📌 Key Indicators")

    col1, col2, col3, col4 = st.columns(4)

    def safe_mean(col):
        return df_filtered[col].mean() if col in df_filtered.columns else 0

    col1.metric("👥 Population", f"{int(safe_mean('Population')):,}" if "Population" in df_filtered.columns else "N/A")

    col2.metric("💰 Avg Income", f"KES {int(safe_mean('Household_Income')):,}" if "Household_Income" in df_filtered.columns else "N/A")

    col3.metric("📉 Poverty Rate", f"{safe_mean('Poverty_Rate')*100:.1f}%" if "Poverty_Rate" in df_filtered.columns else "N/A")

    col4.metric("📊 Unemployment", f"{safe_mean('Unemployment_Rate')*100:.1f}%" if "Unemployment_Rate" in df_filtered.columns else "N/A")

    st.markdown("---")

    # -------------------------
    # DISTRIBUTION ANALYSIS
    # -------------------------
    st.subheader("📊 Indicator Distribution")

    if indicator in df_filtered.columns:
        st.bar_chart(df_filtered.set_index("County")[indicator])
    else:
        st.info("Selected indicator not available in dataset.")

    st.markdown("---")

    # -------------------------
    # TOP & BOTTOM COUNTIES
    # -------------------------
    st.subheader("🏆 Top & Bottom Performers")

    if indicator in df_filtered.columns:

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🔝 Top Counties")
            st.dataframe(
                df_filtered.sort_values(indicator, ascending=False).head(5)
            )

        with col2:
            st.markdown("### 🔻 Bottom Counties")
            st.dataframe(
                df_filtered.sort_values(indicator, ascending=True).head(5)
            )

    st.markdown("---")

    # -------------------------
    # TREND ANALYSIS
    # -------------------------
    st.subheader("📈 Trends Over Time")

    if indicator in df.columns:
        trend_df = df[df["County"].isin(selected_counties)]

        st.line_chart(
            trend_df.groupby("Year")[indicator].mean()
        )
    else:
        st.info("Trend analysis unavailable for selected indicator.")

    st.markdown("---")

    # -------------------------
    # DATA EXPORT
    # -------------------------
    with st.expander("📂 Export Dataset"):
        st.dataframe(df_filtered)

        csv = df_filtered.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download CSV",
            csv,
            f"dataset_{selected_year}.csv",
            "text/csv",
            key="download_filtered"
        )

    # -------------------------
    # INSIGHTS PANEL
    # -------------------------
    st.subheader("💡 Key Insights")

    if indicator in df_filtered.columns and not df_filtered.empty:
        top_row = df_filtered.sort_values(indicator, ascending=False).iloc[0]
        bottom_row = df_filtered.sort_values(indicator, ascending=True).iloc[0]

        st.success(f"Highest {indicator}: {top_row['County']}")
        st.warning(f"Lowest {indicator}: {bottom_row['County']}")

    st.info("Use Maps tab to visualize spatial disparities.")

