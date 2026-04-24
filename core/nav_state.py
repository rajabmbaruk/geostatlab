import streamlit as st

def get_nav_key():
    return f"main_nav_{st.session_state.get('role','default')}_{st.session_state.get('presentation_mode',False)}"
