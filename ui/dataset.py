import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd

def show_dataset(df):

    st.header("📊 Dataset Explorer")

    if df is None or df.empty:
        st.error("Dataset is empty or not loaded properly.")
        return

    # SAFETY CHECK (fix your crash)
    if "Year" not in df.columns:
        st.error("Column 'Year' missing. Check dataset schema.")
        st.write(df.columns)
        return

    col1, col2 = st.columns(2)

    with col1:
        year = st.selectbox("Year", sorted(df["Year"].unique()))

    with col2:
        county = st.multiselect(
            "County",
            sorted(df["County"].unique())
        )

    filtered = df[df["Year"] == year]

    if county:
        filtered = filtered[filtered["County"].isin(county)]

    st.dataframe(filtered, use_container_width=True)

    st.download_button(
        "Download Data",
        filtered.to_csv(index=False),
        "dataset.csv",
        "text/csv"
    )
    
def show_dataset1(df):
    st.title("📊 Dataset Explorer")

    # -------------------------
    # SAFETY CHECK
    # -------------------------
    if df is None or df.empty:
        st.error("Dataset is empty or failed to load.")
        return

    # -------------------------
    # YEAR FILTER
    # -------------------------
    years = sorted(df["Year"].unique())

    selected_year = st.selectbox(
        "📅 Select Year",
        years,
        index=len(years) - 1
    )

    # -------------------------
    # COUNTY FILTER
    # -------------------------
    counties = sorted(df["County"].unique())

    selected_counties = st.multiselect(
        "🏞️ Select Counties",
        counties,
        default=counties[:5]
    )

    # -------------------------
    # INDICATOR SELECTION
    # -------------------------
    indicator = st.selectbox(
        "📌 Select Indicator",
        [
            "Household_Income",
            "Poverty_Rate",
            "Agricultural_Output",
            "Education_Level",
            "Unemployment_Rate"
        ]
    )

    # -------------------------
    # FILTER DATA
    # -------------------------
    df_filtered = df[
        (df["Year"] == selected_year) &
        (df["County"].isin(selected_counties))
    ]

    st.markdown("---")

    # -------------------------
    # KPI METRICS
    # -------------------------
    st.subheader("📌 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Population",
        f"{int(df_filtered['Population'].mean()):,}"
    )

    col2.metric(
        "💰 Avg Income",
        f"KES {int(df_filtered['Household_Income'].mean()):,}"
    )

    col3.metric(
        "📉 Poverty Rate",
        f"{df_filtered['Poverty_Rate'].mean()*100:.1f}%"
    )

    col4.metric(
        "📊 Unemployment",
        f"{df_filtered['Unemployment_Rate'].mean()*100:.1f}%"
    )

    st.markdown("---")

    # -------------------------
    # BAR CHART
    # -------------------------
    st.subheader("📊 Indicator Distribution")

    st.bar_chart(
        df_filtered.set_index("County")[indicator]
    )

    # -------------------------
    # TOP / BOTTOM
    # -------------------------
    st.subheader("🏆 Top & Bottom Counties")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔝 Top 5")
        st.dataframe(
            df_filtered.sort_values(indicator, ascending=False).head(5)
        )

    with col2:
        st.markdown("### 🔻 Bottom 5")
        st.dataframe(
            df_filtered.sort_values(indicator, ascending=True).head(5)
        )

    st.markdown("---")

    # -------------------------
    # TRENDS
    # -------------------------
    st.subheader("📈 Trend Over Time")

    trend_df = df[df["County"].isin(selected_counties)]

    st.line_chart(
        trend_df.groupby("Year")[indicator].mean()
    )

    st.markdown("---")

    # -------------------------
    # DATA TABLE
    # -------------------------
    with st.expander("📂 View Data Table"):
        st.dataframe(df_filtered)

        csv = df_filtered.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download CSV",
            csv,
            f"dataset_{selected_year}.csv",
            "text/csv"
        )

    # -------------------------
    # AI INSIGHTS
    # -------------------------
    st.subheader("💡 Insights")

    try:
        top = df_filtered.sort_values(indicator, ascending=False).iloc[0]["County"]
        bottom = df_filtered.sort_values(indicator, ascending=True).iloc[0]["County"]

        st.success(f"Top performer: {top}")
        st.warning(f"Lowest performer: {bottom}")

        spread = df_filtered[indicator].max() - df_filtered[indicator].min()

        if spread > df_filtered[indicator].mean():
            st.info("High disparity detected across counties.")
        else:
            st.info("Moderate variation across counties.")

    except:
        st.info("Not enough data for insights.")
