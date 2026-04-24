import streamlit as st
st.sidebar.toggle("🎤 Presentation Mode", key="presentation_mode")
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

if st.session_state.presentation_mode:
    import time
    time.sleep(3)
    st.session_state.slide_index += 1
    st.rerun()
