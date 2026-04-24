import streamlit as st

def init_state(years):
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