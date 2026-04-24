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
        ("👋 Welcome", "Explore statistics, maps, analysis, and policy simulation."),
        ("🗺️ Maps", "Compare county-level baseline and policy maps."),
        ("📊 Analysis", "Track rankings, disparities, and trends."),
        ("⚙️ Policy", "Simulate interventions and compare outcomes."),
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
        if st.button("⬅ Back", disabled=step == 0, key="onboard_back"):
            st.session_state.onboarding_step -= 1

    with col2:
        if st.button("Next ➡", key="onboard_next"):
            if step < len(steps) - 1:
                st.session_state.onboarding_step += 1
            else:
                st.session_state.show_onboarding = False

    with col3:
        if st.button("⏭ Skip", key="onboard_skip"):
            st.session_state.show_onboarding = False


# -------------------------
# ROLE DASHBOARD
# -------------------------
def role_dashboard():
    st.markdown("---")

    if st.session_state.role == "Analyst":
        st.subheader("📊 Analyst View")
        st.markdown("""
        - Explore county disparities  
        - Analyze statistical trends  
        - Compare baseline vs policy maps  
        """)
        st.success("Start with Analysis or Policy Maps")

    else:
        st.subheader("🏛️ Policy Maker View")
        st.markdown("""
        - Simulate interventions  
        - Compare policy scenarios  
        - Review spatial policy impact  
        """)
        st.warning("Start with Policy or Policy Maps")


# -------------------------
# QUICK ACTIONS
# -------------------------
def quick_actions():
    st.markdown("---")
    st.markdown("## 🚀 Quick Start")

    def go(page: str, role: str | None = None):
        st.session_state.page = page
        if role:
            st.session_state.role = role
        st.rerun()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🗺️ Maps", key="home_maps", use_container_width=True):
            go("🗺️ Maps")

    with col2:
        if st.button("📈 Analysis", key="home_analysis", use_container_width=True):
            go("📈 Analysis")

    with col3:
        if st.button("⚙️ Policy", key="home_policy", use_container_width=True):
            go("⚙️ Policy", role="Policy Maker")

    with col4:
        if st.button("🧭 Policy Maps", key="home_policy_maps", use_container_width=True):
            go("🗺️ Maps", role="Policy Maker")
            
# -------------------------
# POLICY MAPS PREVIEW
# -------------------------
def policy_maps_preview():
    st.markdown("---")
    st.subheader("🧭 Policy Maps Preview")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "Baseline Maps\n\n"
            "- View county disparities\n"
            "- Explore current indicator distribution\n"
            "- Identify regional hotspots"
        )

    with col2:
        st.success(
            "Policy Maps\n\n"
            "- Compare intervention scenarios\n"
            "- Simulate county-level impact\n"
            "- Evaluate policy effectiveness"
        )

    if st.button("Open Policy Maps", key="open_policy_maps"):
        st.session_state.page = "🗺️ Maps"
        st.session_state.role = "Policy Maker"


# -------------------------
# HOME PAGE
# -------------------------
def show_home(df=None):
    init_home_state()

    st.title("🌍 GeoStatLab – Policy Intelligence Dashboard")
    role_selector()

    st.markdown("Interactive Spatial Statistics, Policy Simulation & Policy Maps")

    # KPI HEADER
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Counties", "47")
    col2.metric("📅 Years", "2018–2024")
    col3.metric("🧠 Modules", "5 + Quiz")
    col4.metric("🗺️ Policy Maps", "Enabled")

    # ONBOARDING
    onboarding()

    # ROLE CONTENT
    role_dashboard()

    # POLICY MAPS PREVIEW
    policy_maps_preview()

    # QUICK ACTIONS
    quick_actions()

    st.markdown("---")
    st.caption("GeoStatLab | KNBS-style Policy Intelligence Dashboard")



