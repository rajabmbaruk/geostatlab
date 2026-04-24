import streamlit as st

def sidebar_nav():

    st.sidebar.title("🌍 GeoStatLab")

    page = st.sidebar.radio(
        "Navigate",
        ["Home", "Dataset", "Survey", "Maps", "Analysis", "Policy", "Quiz"],
        key="main_navigation"
    )

    st.sidebar.markdown("---")
    st.sidebar.info("KNBS-style Policy Intelligence System")

    return page

st.sidebar.markdown("## 🎤 Demo Mode")

if st.sidebar.button("▶ Enter Presentation Mode"):
    toggle_presentation()

if st.session_state.get("presentation_mode", False):
    st.sidebar.success("Presentation Mode ON")
