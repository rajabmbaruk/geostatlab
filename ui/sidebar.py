import streamlit as st

NAV_ITEMS = ["Home", "Dataset", "Survey", "Maps", "Analysis", "Policy", "Quiz"]

def sidebar_nav():
    st.sidebar.title("🧭 GeoStatLab")

    selected = st.sidebar.radio(
        "Navigate",
        NAV_ITEMS,
        key="nav_main"   # single global key
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("KNBS-style Analytics Engine")

    return selected
