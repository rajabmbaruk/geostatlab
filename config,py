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
