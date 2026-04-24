import streamlit as st

from core.state import init_state
from ui.sidebar import sidebar_nav
from data.loader import load_data, load_geojson

from ui import home, dataset, maps, analysis, policy, quiz

st.set_page_config("GeoStatLab", layout="wide")

init_state()

df = load_data()
geojson = load_geojson()

page = sidebar_nav()

if page == "Home":
    show_home(df)
elif page == "Dataset":
    show_dataset(df)
elif page == "Survey":
    show_survey(df)
elif page == "Maps":
    show_maps(df)
elif page == "Analysis":
    show_analysis(df)
elif page == "Policy":
    show_policy(df)
elif page == "Quiz":
    show_quiz(df)
