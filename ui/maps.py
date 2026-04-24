import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from ui.maps import show_analytics_panel

show_analytics_panel(df)
# -----------------------------
# SAFE STATE ACCESS
# -----------------------------
def get_state(key, default=None):
    return st.session_state.get(key, default)


# -----------------------------
# CORE MAP ENGINE
# -----------------------------
def build_map(df: pd.DataFrame, column: str, geojson: dict):
    """
    Creates a choropleth map (KNBS-style spatial visualization)
    """

    if geojson is None:
        raise ValueError("GeoJSON data is required for map rendering.")

    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in dataset.")

    m = folium.Map(location=[0.5, 37.8], zoom_start=6, tiles="cartodbpositron")

    folium.Choropleth(
        geo_data=geojson,
        data=df,
        columns=["County", column],
        key_on="feature.properties.NAME_1",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=column,
        highlight=True
    ).add_to(m)

    return m


# -----------------------------
# MAIN UI FUNCTION
# -----------------------------
def show_maps(df: pd.DataFrame, geojson: dict, year: int, indicator: str):
    """
    Main maps dashboard (baseline vs policy simulation)
    """

    st.header("🗺️ Spatial Analysis Dashboard")

    # -----------------------------
    # VALIDATION
    # -----------------------------
    if df is None or df.empty:
        st.error("Dataset is empty.")
        return

    if "Year" not in df.columns:
        st.error("Missing required column: Year")
        return

    if "County" not in df.columns:
        st.error("Missing required column: County")
        return

    # -----------------------------
    # FILTER DATA
    # -----------------------------
    df_year = df[df["Year"] == year].copy()

    if df_year.empty:
        st.warning(f"No data available for year {year}")
        return

    # -----------------------------
    # LAYOUT
    # -----------------------------
    col1, col2 = st.columns(2)

    # -----------------------------
    # BASELINE MAP
    # -----------------------------
    with col1:
        st.subheader("📍 Baseline Scenario")

        try:
            map_base = build_map(df_year, indicator, geojson)
            st_folium(
                map_base,
                key=f"base_{year}_{indicator}"
            )
        except Exception as e:
            st.error(f"Map error: {str(e)}")

    # -----------------------------
    # POLICY SIMULATION MAP
    # -----------------------------
    with col2:
        st.subheader("📈 Policy Scenario")

        df_policy = df_year.copy()

        # simple simulation (placeholder logic)
        if indicator in df_policy.columns and pd.api.types.is_numeric_dtype(df_policy[indicator]):
            df_policy[indicator] = df_policy[indicator] * 1.1

        try:
            map_policy = build_map(df_policy, indicator, geojson)
            st_folium(
                map_policy,
                key=f"policy_{year}_{indicator}"
            )
        except Exception as e:
            st.error(f"Policy map error: {str(e)}")

    # -----------------------------
    # INSIGHT PANEL
    # -----------------------------
    st.subheader("🧠 Spatial Insights")

    if indicator in df_year.columns:
        base_mean = df_year[indicator].mean()
        policy_mean = df_policy[indicator].mean()

        col1, col2 = st.columns(2)

        col1.metric("Baseline Avg", f"{base_mean:.2f}")
        col2.metric("Policy Avg", f"{policy_mean:.2f}", delta=f"{policy_mean - base_mean:.2f}")

    else:
        st.info("Select a valid numeric indicator for analysis.")
