import streamlit as st


def init_quiz_state():
    """Initialize quiz state safely"""
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False


def show_quiz(df=None):
    """
    Quiz module for GeoStatLab
    Clean, stateless-safe, Streamlit-compatible
    """

    init_quiz_state()

    st.header("🧠 Assessment & Knowledge Check")

    st.markdown("""
    Test your understanding of:
    - Sampling methods  
    - Policy impact interpretation  
    - Spatial inequality  
    """)

    # -------------------------
    # QUESTIONS
    # -------------------------
    q1 = st.radio(
        "1. Which sampling method ensures representation across all counties?",
        ["Simple Random", "Stratified", "Cluster", "Systematic"],
        key="q1"
    )

    q2 = st.radio(
        "2. If unemployment decreases after a policy, what does it indicate?",
        ["Worsening economy", "Improved economy", "No change", "Data error"],
        key="q2"
    )

    q3 = st.radio(
        "3. Which visualization best shows regional inequality?",
        ["Pie chart", "Choropleth map", "Scatter plot", "Histogram"],
        key="q3"
    )

    q4 = st.radio(
        "4. In KNBS-style data, what does Household_Income represent?",
        ["Total national GDP", "Average income per household", "Tax revenue", "Exports"],
        key="q4"
    )

    # -------------------------
    # SCORING LOGIC
    # -------------------------
    score = 0

    if q1 == "Stratified":
        score += 1
    if q2 == "Improved economy":
        score += 1
    if q3 == "Choropleth map":
        score += 1
    if q4 == "Average income per household":
        score += 1

    # -------------------------
    # SUBMIT BUTTON
    # -------------------------
    if st.button("📊 Submit Quiz"):

        st.session_state.quiz_submitted = True
        st.session_state.quiz_score = score

        st.success(f"Your Score: {score}/4")

        # Feedback logic
        if score == 4:
            st.balloons()
            st.success("🏆 Excellent! You have mastered the concepts.")
        elif score == 3:
            st.info("👍 Good job! You are close to mastery.")
        elif score == 2:
            st.warning("⚠️ Fair understanding. Review policy simulation.")
        else:
            st.error("❌ Needs improvement. Revisit dataset & maps modules.")

    # -------------------------
    # EDUCATIONAL FEEDBACK PANEL
    # -------------------------
    st.markdown("---")
    st.subheader("📘 Learning Insights")

    st.info("""
    ✔ Stratified sampling improves representativeness  
    ✔ Choropleth maps reveal spatial inequality  
    ✔ Policy impact is measured through before/after comparison  
    """)

    # -------------------------
    # RESET OPTION
    # -------------------------
    if st.session_state.quiz_submitted:
        if st.button("🔄 Retake Quiz"):
            st.session_state.quiz_score = 0
            st.session_state.quiz_submitted = False
            st.rerun()




