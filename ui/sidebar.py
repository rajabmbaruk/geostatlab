import streamlit as st

PAGES = ["Home", "Dataset", "Survey", "Maps", "Analysis", "Policy", "Quiz"]

def sidebar_nav():
    st.sidebar.title("🧭 Navigation")

    # safe default
    current = st.session_state.get("active_page", "Home")

    # IMPORTANT: NEVER reuse radio across reruns without stable key logic
    selected = st.sidebar.radio(
        "Go to",
        PAGES,
        index=PAGES.index(current),
        key="__nav_radio__"   # 🔥 SINGLE GLOBAL UNIQUE KEY
    )

    st.session_state.active_page = selected

    return selected

st.sidebar.markdown("## 🎤 Demo Mode")

if st.sidebar.button("▶ Enter Presentation Mode"):
    toggle_presentation()

if st.session_state.get("presentation_mode", False):
    st.sidebar.success("Presentation Mode ON")
