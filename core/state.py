import streamlit as st

DEFAULT_STATE = {
    "year": 2024,
    "active_page": "Home",
    "role": "Analyst",
    "presentation_mode": False,
    "slide_index": 0
}

def init_state():
    for key, value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_page(page: str):
    st.session_state.active_page = page

