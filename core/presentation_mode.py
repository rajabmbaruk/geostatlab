import streamlit as st
from services.speech import speak

SLIDES = [
    {"title": "Welcome", "content": "GeoStatLab overview"},
    {"title": "Maps", "content": "Spatial analysis tools"},
]

def get_slide():
    idx = st.session_state.slide_index
    return SLIDES[idx]

def next_slide():
    st.session_state.slide_index += 1
    if st.session_state.slide_index >= len(SLIDES):
        st.session_state.slide_index = 0

def play_voice_slide():
    slide = get_slide()
    if st.session_state.presentation_mode:
        speak(f"{slide['title']}. {slide['content']}")
