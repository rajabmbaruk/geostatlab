from gtts import gTTS
import streamlit as st
import base64

def speak(text):

    tts = gTTS(text=text, lang="en")
    file = "speech.mp3"
    tts.save(file)

    audio_file = open(file, "rb")
    audio_bytes = audio_file.read()

    st.audio(audio_bytes, format="audio/mp3")