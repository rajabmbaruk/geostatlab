def init_state():
    import streamlit as st

    defaults = {
        "year": 2024,
        "playing": False,
        "presentation_mode": False,
        "slide_index": 0,
        "role": "Analyst"
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
