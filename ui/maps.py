import streamlit as st
import folium
from streamlit_folium import st_folium


def show_maps(df, geojson=None):
    """
    GeoStatLab Map Module
    Choropleth + policy comparison
    """

    st.header("🗺️ Spatial Analysis Dashboard")

    # -------------------------
    # VALIDATION
    # -------------------------
    if df is None or df.empty:
        st.error("Dataset not loaded.")
        return

    required = ["County", "Year"]
    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    # -------------------------
    # YEAR FILTER
    # -------------------------
    year = st.slider(
        "Select Year",
        int(df["Year"].min()),
        int(df["Year"].max()),
        int(df["Year"].max()),
        key="maps_year"
    )

    df_year = df[df["Year"] == year]

    # -------------------------
    # INDICATOR SELECTION
    # -------------------------
    indicator = st.selectbox(
        "Select Indicator",
        [
            "Household_Income",
            "Poverty_Rate",
            "Agricultural_Output",
            "Education_Level",
            "Unemployment_Rate"
        ],
        key="maps_indicator"
    )

    # -------------------------
    # MAP BUILDER
    # -------------------------
    def build_map(data, column):
        m = folium.Map(location=[0.5, 37.8], zoom_start=6)

        if geojson is None:
            st.warning("GeoJSON missing — map borders disabled.")
            return m

        folium.Choropleth(
            geo_data=geojson,
            data=data,
            columns=["County", column],
            key_on="feature.properties.NAME_1",
            fill_color="YlOrRd",
            legend_name=column
        ).add_to(m)

        return m

    # -------------------------
    # POLICY SIMULATION
    # -------------------------
    st.subheader("⚙️ Policy Simulation")

    policy = st.selectbox(
        "Policy Type",
        ["None", "Agriculture Boost", "Education Investment", "Jobs Program"],
        key="maps_policy"
    )

    intensity = st.slider(
        "Intensity (%)",
        0, 50, 10,
        key="maps_intensity"
    )

    df_policy = df_year.copy()

    if policy == "Agriculture Boost":
        df_policy["Agricultural_Output"] *= (1 + intensity / 100)

    elif policy == "Education Investment":
        df_policy["Education_Level"] *= (1 + intensity / 100)

    elif policy == "Jobs Program":
        df_policy["Unemployment_Rate"] *= (1 - intensity / 100)

    # -------------------------
    # MAP DISPLAY
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Baseline")
        st_folium(build_map(df_year, indicator), height=400)

    with col2:
        st.subheader("📍 Policy Impact")
        st_folium(build_map(df_policy, indicator), height=400)

    # -------------------------
    # IMPACT ANALYSIS
    # -------------------------
    st.subheader("📊 Impact Summary")

    diff = df_policy[indicator] - df_year[indicator]

    summary = df_year.copy()
    summary["Change"] = diff

    col1, col2 = st.columns(2)

    with col1:
        st.success("Top Improvements")
        st.dataframe(summary.sort_values("Change", ascending=False).head(5))

    with col2:
        st.error("Largest Declines")
        st.dataframe(summary.sort_values("Change").head(5))
