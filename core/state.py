import streamlit as st

def init_state(years):
    defaults = {
        "year": max(years),
        "active_tab": 0,
        "playing": False,
        "selected_county": None,
        "show_onboarding": True,
        "onboarding_step": 0,
        "presentation_mode": False,
        "slide_index": 0,
        "global_indicator": "Household_Income",
        "role": "Analyst"
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


