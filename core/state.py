import streamlit as st
defaults = {
        "active_tab": "Home",
        "year": 2024,
        "presentation_mode": False,
        "slide_index": 0,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def init_state():
    """Safe idempotent initializer (NO arguments)."""
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value            

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Home"
        
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


import streamlit as st

def init_state(years):
    default_year = max(years)

    defaults = {
        "year": default_year,
        "playing": False,
        "active_tab": 0,
        "role": "Analyst",
        "show_onboarding": True,
        "onboarding_step": 0,
        "presentation_mode": False,
        "slide_index": 0,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value




