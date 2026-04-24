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

if st.session_state.get("voice_mode", True):

    speak(slide["title"] + ". " + slide["content"])