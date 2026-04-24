import streamlit as st


# -------------------------
# SAFE STATE INIT
# -------------------------
def init_home_state():
    defaults = {
        "role": "Analyst",
        "page": "🏠 Home",
        "first_visit": True,
        "show_onboarding": True,
        "onboarding_step": 0
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# -------------------------
# ROLE SYSTEM
# -------------------------
def role_selector():
    with st.sidebar:
        st.markdown("## 👤 User Role")

        st.session_state.role = st.radio(
            "Select Role",
            ["Analyst", "Policy Maker"],
            index=0 if st.session_state.role == "Analyst" else 1,
            key="role_selector"
        )


# -------------------------
# ONBOARDING SYSTEM
# -------------------------
def onboarding():
    steps = [
        ("👋 Welcome", "Explore statistics, maps, and policy simulation."),
        ("🗺️ Maps", "Compare baseline vs policy maps."),
        ("📊 Analysis", "Track rankings and disparities."),
        ("⚙️ Policy", "Simulate interventions and impacts."),
        ("🎯 Ready", "Start exploring GeoStatLab.")
    ]

    if not st.session_state.show_onboarding:
        return

    step = st.session_state.onboarding_step
    title, content = steps[step]

    st.markdown(f"## {title}")
    st.info(content)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅ Back", disabled=step == 0):
            st.session_state.onboarding_step -= 1

    with col2:
        if st.button("Next ➡"):
            if step < len(steps) - 1:
                st.session_state.onboarding_step += 1
            else:
                st.session_state.show_onboarding = False

    with col3:
        if st.button("⏭ Skip"):
            st.session_state.show_onboarding = False


# -------------------------
# ROLE DASHBOARD
# -------------------------
def role_dashboard():
    st.markdown("---")

    if st.session_state.role == "Analyst":
        st.subheader("📊 Analyst View")

        st.markdown("""
        - Data exploration  
        - Statistical analysis  
        - Trend evaluation  
        """)

        st.success("Use Analysis module for insights")

    else:
        st.subheader("🏛️ Policy Maker View")

        st.markdown("""
        - Policy simulation  
        - Impact comparison  
        - Decision support  
        """)

        st.warning("Use Policy module for simulations")


# -------------------------
# QUICK ACTIONS
# -------------------------
def quick_actions():
    st.markdown("---")
    st.markdown("## 🚀 Quick Start")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🗺️ Maps"):
            st.session_state.page = "🗺️ Maps"

    with col2:
        if st.button("📈 Analysis"):
            st.session_state.page = "📈 Analysis"

    with col3:
        if st.button("⚙️ Policy"):
            st.session_state.page = "⚙️ Policy"


# -------------------------
# HOME PAGE
# -------------------------
def show_home(df=None):
    init_home_state()

    st.title("🌍 GeoStatLab – Policy Intelligence Dashboard")

   onboarding()

    st.markdown("Interactive Spatial Statistics & Policy Simulation Platform")

    # KPI HEADER
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Counties", "47")
    col2.metric("📅 Years", "2018–2024")
    col3.metric("🧠 Modules", "5 + Quiz")

    

    st.markdown("---")
    st.caption("GeoStatLab | KNBS-style Policy Intelligence Dashboard")



