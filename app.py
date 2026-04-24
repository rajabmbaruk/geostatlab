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
    home.show(df)

elif page == "Dataset":
    dataset.show(df)

elif page == "Maps":
    maps.show(df, geojson)

elif page == "Analysis":
    analysis.show(df)

elif page == "Policy":
    policy.show(df)

elif page == "Quiz":
    quiz.show(df)
