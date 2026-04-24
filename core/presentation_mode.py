import streamlit as st
import time

def init_presentation():
    if "presentation_mode" not in st.session_state:
        st.session_state.presentation_mode = False

    if "slide_index" not in st.session_state:
        st.session_state.slide_index = 0

    if "auto_play" not in st.session_state:
        st.session_state.auto_play = False

def toggle_auto_play():
    st.session_state.auto_play = not st.session_state.auto_play

from core.voice import speak

import streamlit as st

slides = [
    {"title": "Welcome", "content": "GeoStatLab overview"},
    {"title": "Maps", "content": "Explore spatial patterns"},
]

def speak(text):
    # placeholder for TTS (optional)
    print(text)

def init_presentation():
    if "slide_index" not in st.session_state:
        st.session_state.slide_index = 0

def get_current_slide():
    idx = st.session_state.get("slide_index", 0)
    return slides[idx]

def next_slide():
    st.session_state.slide_index = min(
        st.session_state.slide_index + 1,
        len(slides) - 1
    )

def toggle_presentation():
    st.session_state.presentation_mode = not st.session_state.get("presentation_mode", False)

def speak_current_slide():
    slide = get_current_slide()
    speak(slide["title"] + ". " + slide["content"])


