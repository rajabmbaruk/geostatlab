import streamlit as st

from core.state import init_state
from data.loader import load_data, load_geojson
from ui.sidebar import sidebar_nav
from ui.dataset import show_dataset

# INIT FIRST (CRITICAL)
init_state()

df = load_data()
geojson = load_geojson()

# LOAD DATA
df = load_data()

# NAVIGATION
page = sidebar_nav()

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
    from data.loader import load_geojson
        
    geojson = load_geojson()
        
        show_maps(
            df=df,
            geojson=geojson,
            year=st.session_state.year
        )

elif page == "Analysis":
    from ui.analysis import show_analysis
    show_analysis(df)

elif page == "Policy":
    from ui.policy import show_policy
    show_policy(df)

elif page == "Quiz":
    from ui.quiz import show_quiz
    show_quiz(df)
