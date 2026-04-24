import streamlit as st
import config

DEFAULT_YEAR = config.DEFAULT_YEAR

def init_state():
    if "year" not in st.session_state:
        st.session_state.year = DEFAULT_YEAR

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = 0
        
    if "year" not in st.session_state:
        st.session_state.year = max(years)

    if "role" not in st.session_state:
        st.session_state.role = "Analyst"

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Home"

def get_year():
    return st.session_state.year

def set_year(year):
    st.session_state.year = year


def init_state():
    defaults = {
        "presentation_mode": False,
        "year": 2024,
        "active_tab": 0,
        "playing": False,
        "show_onboarding": False,
        "onboarding_step": 0,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

