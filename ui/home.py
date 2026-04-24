def show_home():
    import streamlit as st
    st.title("Home")
    
import streamlit as st

def show_home(df):
    st.title("🌍 GeoStatLab Home")

    st.write("Dataset overview:")
    st.dataframe(df.head())
