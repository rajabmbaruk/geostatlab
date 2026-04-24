import streamlit as st

def sidebar_nav():
    with st.sidebar:
        st.title("GeoStatLab")

        nav_key = f"main_nav_{st.session_state.get('presentation_mode', False)}"

        page = st.radio(
            "Navigate",
            ["Home", "Dataset", "Survey", "Maps", "Analysis", "Policy", "Quiz"],
            key=get_nav_key()
        )

    return page

st.sidebar.markdown("## 🎤 Demo Mode")

if st.sidebar.button("▶ Enter Presentation Mode"):
    toggle_presentation()

if st.session_state.get("presentation_mode", False):
    st.sidebar.success("Presentation Mode ON")
