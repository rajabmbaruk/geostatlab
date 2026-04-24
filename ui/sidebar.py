import streamlit as st
from core.state import set_page

def sidebar_nav():

    with st.sidebar:
        st.title("🌍 GeoStatLab")

        page = st.radio(
            "Navigate",
            ["Home", "Dataset", "Survey", "Maps", "Analysis", "Policy", "Quiz"],
            key="nav_radio"
        )

        role = st.selectbox(
            "Role",
            ["Analyst", "Policy Maker"],
            key="role_select"
        )

    st.session_state.role = role
    set_page(page)

    return page



