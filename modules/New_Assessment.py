import streamlit as st
from database import get_connection
from datetime import datetime

def new_assessment():

    # ===============================
    # SESSION VALIDATION
    # ===============================
    
    user = st.session_state.get("user")

    if not user:
         st.error("Session expired. Please login again.")
         st.stop()


    if not isinstance(user, dict):
        try:
           user = dict(user)
           st.session_state["user"] = user
        except:
           st.error("User session corrupted")
           st.write(user)
           st.stop()

    current_user = user["username"]
    company_name = user["company_name"]
    login_id = user["id"]   
    

    # ===============================
    # INIT SESSION STORAGE
    # ===============================
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # ===============================
    # PAGE CONFIG
    # ===============================

    st.title("Institutional Risk Assessment System")
    st.info(f"Company: {company_name}")

    sector = st.selectbox(
        "Sector",
        ["Technology", "Banking", "Energy", "Healthcare", "Infrastructure"]
    )

    st.markdown("---")

    # ===============================
    # INPUTS
    # ===============================

    # DIGITAL
    st.header("Digital Risk")
    col1, col2, col3 = st.columns(3)

    with col1:
        breaches = st.number_input("Security Breaches", min_value=0, value=st.session_state.answers.get("breaches", 0))
        st.session_state.answers["breaches"] = breaches

    with col2:
        patch_delay = st.number_input("Patch Delay (Days)", min_value=0, value=st.session_state.answers.get("patch_delay", 0))
        st.session_state.answers["patch_delay"] = patch_delay

    with col3:
        firewall_score = st.number_input("Firewall Strength (0-100)", min_value=0, max_value=100,
                                         value=st.session_state.answers.get("firewall_score", 0))
        st.session_state.answers["firewall_score"] = firewall_score

    # HUMAN
    st.header("Human Risk")
    col1, col2, col3 = st.columns(3)

    with col1:
        training_hours = st.number_input("Training Hours", min_value=0,
                                         value=st.session_state.answers.get("training_hours", 0))
        st.session_state.answers["training_hours"] = training_hours

    with col2:
        turnover_rate = st.number_input("Turnover Rate (%)", min_value=0.0, max_value=100.0,
                                        value=st.session_state.answers.get("turnover_rate", 0.0))
        st.session_state.answers["turnover_rate"] = turnover_rate

    with col3:
        policy_violations = st.number_input("Policy Violations", min_value=0,
                                            value=st.session_state.answers.get("policy_violations", 0))
        st.session_state.answers["policy_violations"] = policy_violations

    # FINANCIAL
    st.header("Financial Risk")
    col1, col2, col3 = st.columns(3)

    with col1:
        debt_ratio = st.number_input("Debt Ratio", min_value=0.0, max_value=1.0,
                                     value=st.session_state.answers.get("debt_ratio", 0.0))
        st.session_state.answers["debt_ratio"] = debt_ratio

    with col2:
        revenue_decline = st.number_input("Revenue Decline (%)", min_value=0.0,
                                          value=st.session_state.answers.get("revenue_decline", 0.0))
        st.session_state.answers["revenue_decline"] = revenue_decline

    with col3:
        reserve_months = st.number_input("Reserve Months", min_value=0,
                                         value=st.session_state.answers.get("reserve_months", 0))
        st.session_state.answers["reserve_months"] = reserve_months

    # GOVERNANCE
    st.header("Governance Risk")
    col1, col2, col3 = st.columns(3)

    with col1:
        audit_findings = st.number_input("Audit Findings", min_value=0,
                                         value=st.session_state.answers.get("audit_findings", 0))
        st.session_state.answers["audit_findings"] = audit_findings

    with col2:
        compliance_issues = st.number_input("Compliance Issues", min_value=0,
                                            value=st.session_state.answers.get("compliance_issues", 0))
        st.session_state.answers["compliance_issues"] = compliance_issues

    with col3:
        board_meetings = st.number_input("Board Meetings", min_value=0,
                                         value=st.session_state.answers.get("board_meetings", 0))
        st.session_state.answers["board_meetings"] = board_meetings

    st.markdown("---")

    # ===============================
    # FETCH ADMIN CONFIG (CRITICAL)
    # ===============================
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scoring_config WHERE id = 1")
    config = cursor.fetchone()

    low = config["low_threshold"]
    med = config["medium_threshold"]
    high = config["high_threshold"]

    conn.close()
    
    if all([
        breaches == 0,
        patch_delay == 0,
        firewall_score == 0,
        training_hours == 0,
        turnover_rate == 0,
        policy_violations == 0,
        debt_ratio == 0,
        revenue_decline == 0,
        reserve_months == 0,
        audit_findings == 0,
        compliance_issues == 0,
        board_meetings == 0
    ]):
        st.info("Please fill in the assessment to see risk analysis")
        return
    
    # ===============================
    # SCORE CALCULATION (UNCHANGED LOGIC)
    # ===============================
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

    overall_score = (
    digital_score +
    human_score +
    financial_score +
    governance_score
    ) / 4

    overall_score = max(0, min(overall_score, 100))

    # ===============================
    # TREND
    # ===============================
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT overall_score
        FROM assessments
        WHERE login_id = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (login_id,))

    previous = cursor.fetchone()

    if previous:
        if hasattr(previous, "keys"):
             prev_score = previous["overall_score"]
        else:
             prev_score = previous[0]

        score_change = overall_score - prev_score
    else:
        score_change = 0

    conn.close()

    # ===============================
    # RISK LEVEL (ADMIN CONTROLLED)
    # ===============================
    if overall_score <= low:
        risk_level = "LOW RISK"
    elif overall_score <= med:
        risk_level = "MODERATE RISK"
    elif overall_score <= high:
        risk_level = "HIGH RISK"
    else:
        risk_level = "CRITICAL RISK"

    if score_change >= 20:
        risk_level += " | RAPID DETERIORATION"
    elif score_change <= -20:
        risk_level += " | RAPID IMPROVEMENT"

    # ===============================
    # SESSION STORAGE
    # ===============================
    st.session_state.score = round(overall_score, 2)
    st.session_state.risk_level = risk_level
    st.session_state.digital_score = digital_score
    st.session_state.human_score = human_score
    st.session_state.financial_score = financial_score
    st.session_state.governance_score = governance_score
    st.session_state.patch_delay = patch_delay
    st.session_state.training_hours = training_hours
    st.session_state.policy_violations = policy_violations
    st.session_state.score_change = score_change

    # ===============================
    # DYNAMIC UI (NON-BIASED)
    # ===============================
    st.markdown("## 🟡 Risk Signals")

    if digital_score > 70:
        st.warning("Digital risk rising")
    elif digital_score > 40:
        st.info("Digital risk moderate")
    else:
        st.success("Digital stable")

    if human_score > 70:
        st.warning("Human risk rising")
    elif human_score > 40:
        st.info("Human risk moderate")
    else:
        st.success("Human stable")
    # FINANCIAL
    if financial_score > 70:
        st.warning("Financial risk rising")
    elif financial_score > 40:
        st.info("Financial risk moderate")
    else:
        st.success("Financial stable")

    # GOVERNANCE
    if governance_score > 70:
        st.warning("Governance risk rising")
    elif governance_score > 40:
        st.info("Governance risk moderate")
    else:
        st.success("Governance stable")    

    st.progress(overall_score / 100)

    # ===============================
    # SAVE
    # ===============================
    if st.button("Save Assessment"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO assessments (
                login_id, username, company_name, sector,
                breaches, patch_delay, firewall_score,
                training_hours, turnover_rate, policy_violations,
                debt_ratio, revenue_decline, reserve_months,
                audit_findings, compliance_issues, board_meetings,
                digital_score, human_score, financial_score,
                governance_score, overall_score,
                assessment_date,
                risk_level
            )
            VALUES (?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            login_id, current_user, company_name, sector,
            breaches, patch_delay, firewall_score,
            training_hours, turnover_rate, policy_violations,
            debt_ratio, revenue_decline, reserve_months,
            audit_findings, compliance_issues, board_meetings,
            digital_score, human_score, financial_score,
            governance_score, overall_score,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            risk_level
        ))

        conn.commit()
        conn.close()

        st.session_state.page = "user_dashboard"
        st.session_state.dashboard_page = "home"
        st.rerun()
