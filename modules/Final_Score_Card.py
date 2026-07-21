import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


import google.generativeai as genai
import os
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")


from database import get_connection, get_previous_score

    # ------------------------------
    # AI FUNCTION
    # ------------------------------
def generate_ai_insight(prompt):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI insight unavailable: {str(e)}"


    # ------------------------------
    # PDF FUNCTION
    # ------------------------------
def generate_pdf(company_name, overall_score, risk_level, findings, recommendations, ai_output):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        content = []

        content.append(Paragraph("Risk Intelligence Report", styles["Title"]))
        content.append(Spacer(1, 10))

        content.append(Paragraph(f"Company: {company_name}", styles["Normal"]))
        content.append(Paragraph(f"Risk Level: {risk_level}", styles["Normal"]))
        content.append(Paragraph(f"Score: {overall_score:.2f}", styles["Normal"]))
        content.append(Spacer(1, 10))

        content.append(Paragraph("Key Findings:", styles["Heading2"]))
        for f in findings:
            content.append(Paragraph(f"- {f}", styles["Normal"]))

        content.append(Spacer(1, 10))

        content.append(Paragraph("Recommendations:", styles["Heading2"]))
        for level, rec in recommendations:
            content.append(Paragraph(f"- {rec}", styles["Normal"]))

        content.append(Spacer(1, 10))

        content.append(Paragraph("AI Risk Analysis:", styles["Heading2"]))
        content.append(Paragraph(ai_output, styles["Normal"]))

        doc.build(content)
        buffer.seek(0)
        return buffer

def final_score_card():        

    # -----------------------------
    # AUTH CHECK
    # -----------------------------
    user = st.session_state.get("user")

    if not user:
        st.error("Session expired. Please login again.")
        st.stop()

    current_user = user["username"]
    company_name = user["company_name"]
    login_id = user["id"]

    

    # -----------------------------
    # FETCH DATA
    # -----------------------------
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM assessments
        WHERE login_id = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (login_id,))

    row = cursor.fetchone()
    conn.close()

    # -----------------------------
    # SESSION PRIORITY (FIXED)
    # -----------------------------
    if "score" in st.session_state:
        digital_score = st.session_state.get("digital_score", 0)
        human_score = st.session_state.get("human_score", 0)
        financial_score = st.session_state.get("financial_score", 0)
        governance_score = st.session_state.get("governance_score", 0)
        overall_score = st.session_state.get("score", 0)
        risk_level = st.session_state.get("risk_level", "UNKNOWN")

        patch_delay = st.session_state.get("patch_delay", 0)
        training_hours = st.session_state.get("training_hours", 0)
        policy_violations = st.session_state.get("policy_violations", 0)

    else:
        if not row:
            st.warning("No assessment found. Please complete an assessment first.")
            st.stop()

        digital_score = row["digital_score"]
        human_score = row["human_score"]
        financial_score = row["financial_score"]
        governance_score = row["governance_score"]
        overall_score = row["overall_score"]
        risk_level = row["risk_level"]

        patch_delay = row["patch_delay"]
        training_hours = row["training_hours"]
        policy_violations = row["policy_violations"]

    # -----------------------------
    # TREND
    # -----------------------------
    previous_score = get_previous_score(current_user)

    if "score_change" in st.session_state:
        change = st.session_state.score_change
    else:
        change = overall_score - previous_score if previous_score else 0

    # -----------------------------
    # HEADER
    # -----------------------------
    st.markdown("## 🧠 Risk Intelligence Report")
    st.caption(f"Generated on {datetime.now().strftime('%d %B %Y')}")
    st.markdown("---")

    # -----------------------------
    # SUMMARY
    # -----------------------------
    if overall_score > 70:
        summary = "High risk. Immediate intervention required."
    elif overall_score > 40:
        summary = "Moderate risk. Improvements needed in key areas."
    else:
        summary = "Low risk. Maintain current practices."

    st.markdown("### 📌 Executive Summary")
    st.info(f"**Overall Risk Level: {risk_level} ({overall_score:.2f})**\n\n{summary}")

    # -----------------------------
    # KPI
    # -----------------------------
    st.markdown("### 📊 Risk Snapshot")

    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Score", f"{overall_score:.2f}")
    col2.metric("Risk Level", risk_level)

    if previous_score is not None:
        if change > 5:
            col3.metric("Change", f"+{change:.2f}", delta="Increase")
            st.error(f"Risk increased by {change:.2f}")
        elif change < -5:
            col3.metric("Change", f"{change:.2f}", delta="Improved")
            st.success(f"Risk improved by {abs(change):.2f}")
        else:
            col3.metric("Change", f"{change:.2f}", delta="Stable")
            st.info("Risk remains stable")
    else:
        col3.metric("Change", "N/A")

    # -----------------------------
    # WEAKEST PILLAR
    # -----------------------------
    scores = {
        "Digital": digital_score,
        "Human": human_score,
        "Financial": financial_score,
        "Governance": governance_score
    }

    weakest = min(scores, key=scores.get)
    st.error(f"Highest Risk Area: {weakest}")

    # -----------------------------
    # RADAR CHART
    # -----------------------------
    st.markdown("### Risk Dimensions")

    labels = ['Digital', 'Human', 'Financial', 'Governance']
    values = [digital_score, human_score, financial_score, governance_score]

    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4,4), subplot_kw=dict(polar=True))
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.2)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)

    st.pyplot(fig)

    # -----------------------------
    # FINDINGS
    # -----------------------------
    st.markdown("### 🔍 Key Findings")

    findings = []

    if digital_score < 50:
        findings.append("Digital security controls are weak.")

    if human_score < 50:
        findings.append("Employee awareness is insufficient.")

    if financial_score < 50:
        findings.append("Financial resilience is low.")

    if governance_score < 50:
        findings.append("Governance structure is weak.")

    if findings:
        for f in findings:
            st.warning(f)
    else:
        st.success("No major weaknesses detected.")

    # -----------------------------
    # RECOMMENDATIONS
    # -----------------------------
    st.markdown("### Recommendations")

    recommendations = []

    if patch_delay > 7 and training_hours < 10:
        recommendations.append(("high", "Reduce patch delay and increase training"))

    if policy_violations > 5:
        recommendations.append(("high", "Enforce policies strictly"))

    if not recommendations:
        recommendations.append(("low", "Maintain current system"))

    for level, text in recommendations:
        if level == "high":
            st.error(text)
        else:
            st.success(text)

    # -----------------------------
    # AI
    # -----------------------------
    st.markdown("## 🧠 AI Risk Intelligence")

    prompt = f"""
    Digital: {digital_score}
    Human: {human_score}
    Financial: {financial_score}
    Governance: {governance_score}
    Overall: {overall_score}
    Change: {change}
    """

    ai_output = generate_ai_insight(prompt)

    st.markdown("### 🧾 AI Analysis")
    st.markdown(ai_output)

    # -----------------------------
    # PDF
    # -----------------------------
    pdf_file = generate_pdf(
        company_name,
        overall_score,
        risk_level,
        findings,
        recommendations,
        ai_output
    )

    st.download_button("Download Report", pdf_file, "risk_report.pdf")
