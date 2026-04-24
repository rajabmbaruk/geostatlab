from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def generate_report(df, year, indicator, insights, filename="GeoStatLab_Report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    story = []

    # TITLE
    story.append(Paragraph("GeoStatLab Policy Intelligence Report", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Year: {year}", styles["Normal"]))
    story.append(Paragraph(f"Indicator: {indicator}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # SUMMARY STATS
    df_year = df[df["Year"] == year]

    story.append(Paragraph("Key Insights:", styles["Heading2"]))
    for i in insights:
        story.append(Paragraph(f"• {i}", styles["Normal"]))

    story.append(Spacer(1, 12))

    # SUMMARY METRICS
    story.append(Paragraph("Statistical Summary:", styles["Heading2"]))
    story.append(
        Paragraph(
            f"Mean: {df_year[indicator].mean():.2f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Std Dev: {df_year[indicator].std():.2f}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["Italic"]
        )
    )

    doc.build(story)

    return filename