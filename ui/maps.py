import streamlit as st
import folium
from streamlit_folium import st_folium


def build_map(df, column, geojson):
    m = folium.Map(location=[0.5, 37.8], zoom_start=6)

    folium.Choropleth(
        geo_data=geojson,
        data=df,
        columns=["County", column],
        key_on="feature.properties.NAME_1",
        fill_color="YlOrRd",
        legend_name=column
    ).add_to(m)

    return m


def show_maps(df, geojson, year, indicator):
    st.header("🗺️ Maps")

    df_year = df[df["Year"] == year]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Baseline")
        m1 = build_map(df_year, "Household_Income", geojson)
        st_folium(m1, key=f"base_{year}")

    with col2:
        st.subheader("Policy")
        df_policy = df_year.copy()
        df_policy["Household_Income"] *= 1.1

        m2 = build_map(df_policy, "Household_Income", geojson)
        st_folium(m2, key=f"policy_{year}")
        

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
        st_folium(
            build_map(df_year, indicator),
            height=400,
            key=f"baseline_map_{year}_{indicator}"
        )

    with col2:
        st.subheader("📍 Policy Impact")
        st_folium(
            build_map(df_policy, indicator),
            height=400,
            key=f"policy_map_{year}_{indicator}"
        )

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
