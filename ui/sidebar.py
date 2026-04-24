import streamlit as st

PAGES = ["Home", "Dataset", "Survey", "Maps", "Analysis", "Policy", "Quiz"]

def sidebar_nav():
    st.sidebar.title("🧭 Navigation")

    # IMPORTANT: single source of truth
    if "active_page" not in st.session_state:
        st.session_state.active_page = "Home"

    selected = st.sidebar.radio(
        "Go to",
        PAGES,
        index=PAGES.index(st.session_state.active_page),
        key="main_nav_radio"   # 🔥 MUST be unique
    )

    st.session_state.active_page = selected
    return selected

st.sidebar.markdown("## 🎤 Demo Mode")

if st.sidebar.button("▶ Enter Presentation Mode"):
    toggle_presentation()

if st.session_state.get("presentation_mode", False):
    st.sidebar.success("Presentation Mode ON")
