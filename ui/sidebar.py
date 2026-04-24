# ui/sidebar.py
import streamlit as st

def sidebar_nav():
    st.sidebar.title("🌍 GeoStatLab")

    return st.sidebar.radio(
        "Navigation",
        ["Home", "Dataset", "Survey", "Maps", "Analysis", "Policy", "Quiz"],
        key="nav_main"
    )
