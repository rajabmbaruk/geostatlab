import streamlit as st

from data.loader import load_data, load_geojson
from data.processor import build_panel
from state import init_state
from ui.sidebar import sidebar_nav


if st.session_state.presentation_mode:

    story = get_story(df, st.session_state.year)
    step = st.session_state.slide_index

    slide = story[step]

    st.markdown(
        f"""
        <div style="
            height: 80vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        ">
            <h1 style="font-size:42px;">{slide['title']}</h1>
            <p style="font-size:22px; width:70%;">{slide['content']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅ Previous"):
            st.session_state.slide_index = max(0, step - 1)

    with col2:
        if st.button("Exit Demo Mode"):
            st.session_state.presentation_mode = False

    with col3:
        if st.button("Next ➡"):
            st.session_state.slide_index = min(len(story) - 1, step + 1)

    st.stop()  # 🚨 IMPORTANT: freezes normal UI


# INIT
years = list(range(2018, 2025))
init_state(years)

st.set_page_config(page_title="GeoStatLab", layout="wide")

# LOAD DATA
df_base = load_data()
geojson = load_geojson()
df = build_panel(df_base, years)

# NAVIGATION (ONLY SIDEBAR)
page = sidebar_nav()

# ROUTING
if page == "Home":
    from ui.home import show_home
    show_home(df)

elif page == "Dataset":
    from ui.dataset import show_dataset
    show_dataset(df)

elif page == "Survey":
    from ui.survey import show_survey
    show_survey(df)

elif page == "Maps":
    from ui.maps import show_maps
    show_maps(df, geojson)

elif page == "Analysis":
    from ui.analysis import show_analysis
    show_analysis(df)

elif page == "Policy":
    from ui.policy import show_policy
    show_policy(df)

elif page == "Quiz":
    from ui.quiz import show_quiz
    show_quiz()

from core.presentation_mode import init_presentation, toggle_presentation
import time
from core.storyboard import get_story

story = get_story(df, st.session_state.year)
step = st.session_state.slide_index

slide = story[step]

st.markdown(
    f"""
    <div style="
        height: 80vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    ">
        <h1 style="font-size:42px;">{slide['title']}</h1>
        <p style="font-size:22px; width:70%;">{slide['content']}</p>
    </div>
    """,
    unsafe_allow_html=True
)

if st.session_state.auto_play:

    time.sleep(4)  # slide duration (adjust for pacing)

    if st.session_state.slide_index < len(story) - 1:
        st.session_state.slide_index += 1
        st.rerun()
    else:
        st.session_state.auto_play = False

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ Auto Play"):
        st.session_state.auto_play = True

with col2:
    if st.button("⏸ Pause"):
        st.session_state.auto_play = False

with col3:
    if st.button("🔄 Restart"):
        st.session_state.slide_index = 0
        

init_presentation()