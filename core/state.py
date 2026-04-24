import streamlit as st

def init_state():
    defaults = {
        "year": 2024,
        "active_tab": "Home",
        "playing": False,
        "show_onboarding": True,
        "onboarding_step": 0,
        "presentation_mode": False,
        "slide_index": 0,
        "global_indicator": "Household_Income",
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
