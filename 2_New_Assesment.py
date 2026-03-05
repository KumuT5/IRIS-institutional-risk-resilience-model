import streamlit as st
from database import get_connection
from datetime import datetime
# =========================================
# SESSION VALIDATION
# =========================================

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please login first.")
    st.stop()

if "username" not in st.session_state:
    st.error("Please login first.")
    st.stop()

current_user = st.session_state["username"]
company_name = st.session_state.get("company_name", "")

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(page_title="New Assessment", layout="wide")
st.title("Institutional Risk Assessment System")

st.info(f"Company: {company_name}")

sector = st.selectbox(
    "Sector",
    ["Technology", "Banking", "Energy", "Healthcare", "Infrastructure"]
)

st.markdown("---")

# =========================================
# DIGITAL RISK
# =========================================

st.header("Digital Risk")

col1, col2, col3 = st.columns(3)

with col1:
    breaches = st.number_input("Security Breaches", min_value=0)

with col2:
    patch_delay = st.number_input("Patch Delay (Days)", min_value=0)

with col3:
    firewall_score = st.number_input("Firewall Strength (0-100)", min_value=0, max_value=100)

# =========================================
# HUMAN RISK
# =========================================

st.header("Human Risk")

col1, col2, col3 = st.columns(3)

with col1:
    training_hours = st.number_input("Training Hours per Employee", min_value=0)

with col2:
    turnover_rate = st.number_input("Turnover Rate (%)", min_value=0.0, max_value=100.0)

with col3:
    policy_violations = st.number_input("Policy Violations", min_value=0)

# =========================================
# FINANCIAL RISK
# =========================================

st.header("Financial Risk")

col1, col2, col3 = st.columns(3)

with col1:
    debt_ratio = st.number_input("Debt Ratio (0-1)", min_value=0.0, max_value=1.0)

with col2:
    revenue_decline = st.number_input("Revenue Decline (%)", min_value=0.0)

with col3:
    reserve_months = st.number_input("Reserve Months Available", min_value=0)

# =========================================
# GOVERNANCE RISK
# =========================================

st.header("Governance Risk")

col1, col2, col3 = st.columns(3)

with col1:
    audit_findings = st.number_input("Audit Findings", min_value=0)

with col2:
    compliance_issues = st.number_input("Compliance Issues", min_value=0)

with col3:
    board_meetings = st.number_input("Board Meetings per Year", min_value=0)

st.markdown("---")

# =========================================
# CALCULATION & STORAGE
# =========================================

if st.button("Calculate & Store Assessment"):

    # ---------- SCORE CALCULATION ----------
    digital_score = (
        min(breaches * 15, 100) * 0.4 +
        min(patch_delay * 3, 100) * 0.3 +
        (100 - firewall_score) * 0.3
    )

    human_score = (
        (100 - min(training_hours * 2, 100)) * 0.3 +
        min(turnover_rate * 2, 100) * 0.4 +
        min(policy_violations * 10, 100) * 0.3
    )

    financial_score = (
        (debt_ratio * 100) * 0.4 +
        min(revenue_decline * 2, 100) * 0.3 +
        (100 - min(reserve_months * 10, 100)) * 0.3
    )

    governance_score = (
        min(audit_findings * 10, 100) * 0.4 +
        min(compliance_issues * 10, 100) * 0.4 +
        (100 - min(board_meetings * 10, 100)) * 0.2
    )

    # Clamp
    digital_score = max(0, min(digital_score, 100))
    human_score = max(0, min(human_score, 100))
    financial_score = max(0, min(financial_score, 100))
    governance_score = max(0, min(governance_score, 100))

    # ---------- OVERALL ----------
    overall_score = (
        digital_score * 0.30 +
        human_score * 0.25 +
        financial_score * 0.30 +
        governance_score * 0.15
    )

    # ---------- TREND DETECTION ----------
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT overall_score
        FROM assessments
        WHERE company_name = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (company_name,))

    previous = cursor.fetchone()
    score_change = overall_score - previous[0] if previous else 0

    # ---------- CLASSIFICATION ----------
    if overall_score <= 30:
        risk_level = "LOW RISK"
    elif overall_score <= 55:
        risk_level = "MODERATE RISK"
    elif overall_score <= 75:
        risk_level = "HIGH RISK"
    else:
        risk_level = "CRITICAL RISK"

    dominant_pillar = max(digital_score, human_score, financial_score, governance_score)

    if dominant_pillar > 85:
        risk_level += " | CRITICAL PILLAR ALERT"

    high_pillars = sum(score > 75 for score in 
        [digital_score, human_score, financial_score, governance_score]
    )

    if high_pillars >= 2:
        risk_level += " | MULTI-PILLAR PRESSURE"

    if score_change >= 20:
        risk_level += " | RAPID DETERIORATION"
    elif score_change <= -20:
        risk_level += " | RAPID IMPROVEMENT"

    # ---------- RECOMMENDATIONS ----------
    strategic_recs = []
    operational_recs = []
    immediate_recs = []

    if overall_score <= 30:
        strategic_recs.append("Maintain enterprise risk framework.")
    elif overall_score <= 55:
        strategic_recs.append("Initiate targeted mitigation strategy.")
    elif overall_score <= 75:
        strategic_recs.append("Escalate to executive supervision.")
    else:
        strategic_recs.append("Activate board-level intervention.")

    if digital_score > 70:
        operational_recs.append("Enhance cybersecurity controls.")
    if human_score > 70:
        operational_recs.append("Strengthen workforce governance.")
    if financial_score > 70:
        operational_recs.append("Rebalance capital structure.")
    if governance_score > 70:
        operational_recs.append("Increase audit rigor.")

    if dominant_pillar > 85:
        immediate_recs.append("Initiate urgent corrective action.")
    if score_change >= 20:
        immediate_recs.append("Investigate rapid deterioration.")

    # ---------- STORE ----------
    cursor.execute("""
        INSERT INTO assessments (
            username, company_name, sector,
            breaches, patch_delay, firewall_score,
            training_hours, turnover_rate, policy_violations,
            debt_ratio, revenue_decline, reserve_months,
            audit_findings, compliance_issues, board_meetings,
            digital_score, human_score, financial_score,
            governance_score, overall_score,
            assessment_date,
            risk_level
        )
        VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        current_user, company_name, sector,
        breaches, patch_delay, firewall_score,
        training_hours, turnover_rate, policy_violations,
        debt_ratio, revenue_decline, reserve_months,
        audit_findings, compliance_issues, board_meetings,
        digital_score, human_score, financial_score,
        governance_score, overall_score,
        datetime.now().strftime("%Y-%m-%d"), 
        risk_level
    ))

    conn.commit()
    conn.close()

    # ---------- OUTPUT ----------
    st.success("Assessment Stored Successfully")

    st.subheader("Risk Summary")
    st.write(f"Overall Score: {round(overall_score, 2)}")
    st.error(f"Risk Level: {risk_level}")

    st.subheader("Strategic Recommendations")
    for rec in strategic_recs:
        st.write("• " + rec)

    st.subheader("Operational Recommendations")
    for rec in operational_recs:
        st.write("• " + rec)

    st.subheader("Immediate Actions")

    if immediate_recs:
         for rec in immediate_recs:
                        st.write("- " + rec)
    else:
        st.success("No immediate action required. Risk levels within acceptable tolerance.")