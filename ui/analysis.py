from core.ai_insights import generate_ai_insights

def show_ai_panel(df, year, indicator):

    st.subheader("🧠 AI Insights Engine")

    insights = generate_ai_insights(df, year, indicator)

    for i in insights:
        st.info(i)

from core.ai_insights import generate_ai_insights
from core.report_generator import generate_report

def show_analysis(df):

    year = st.session_state.year

    indicator = st.selectbox(
        "Select Indicator",
        ["Household_Income", "Poverty_Rate", "Unemployment_Rate"]
    )

    # AI INSIGHTS
    st.subheader("🧠 AI Insights Panel")

    insights = generate_ai_insights(df, year, indicator)

    for i in insights:
        st.info(i)

    # REPORT GENERATION
    st.subheader("📄 Export Policy Report")

    if st.button("Generate PDF Report"):

        file = generate_report(df, year, indicator, insights)

        with open(file, "rb") as f:
            st.download_button(
                "⬇ Download Report",
                f,
                file_name=file,
                mime="application/pdf"
            )