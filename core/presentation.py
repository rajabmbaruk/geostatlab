import streamlit as st

SLIDES = [
    ("GeoStatLab", "Policy intelligence using KNBS-style data"),
    ("Problem", "Data is fragmented and not spatially visualized"),
    ("Solution", "Interactive geospatial analytics dashboard"),
    ("Impact", "Supports evidence-based policymaking"),
]

def next_slide():
    st.session_state.slide_index = (st.session_state.slide_index + 1) % len(SLIDES)

def current_slide():
    return SLIDES[st.session_state.slide_index]
