import streamlit as st
from database import get_connection

# -----------------------------
# PAGE CONFIG MUST BE FIRST
# -----------------------------
st.set_page_config(layout="wide")

# -----------------------------
# AUTH CHECK
# -----------------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please login first.")
    st.stop()

if "username" not in st.session_state:
    st.error("Please login first.")
    st.stop()

current_user = st.session_state["username"]
company_name = st.session_state["company_name"]

st.markdown("## Assessment History")
st.caption("Review historical institutional risk evaluations.")
st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------
# DATABASE QUERY (USER ISOLATED)
# -----------------------------
conn = get_connection()
cursor = conn.cursor()

data = cursor.execute("""
    SELECT created_at,
           digital_score,
           human_score,
           financial_score,
           governance_score,
           overall_score,
           risk_level
    FROM assessments
    WHERE username = ? AND company_name = ?
    ORDER BY created_at DESC
""", (current_user, company_name)).fetchall()

conn.close()

# -----------------------------
# DISPLAY
# -----------------------------
if not data:
    st.info("No assessments found. Please create one first.")
else:

    st.markdown("### Historical Records")
    st.dataframe(data, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Overall Risk Trend")

    scores = [row[5] for row in data][::-1]
    st.line_chart(scores)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Latest Assessment Snapshot")

    latest = data[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Digital", f"{latest[1]:.0f}")
    col2.metric("Human", f"{latest[2]:.0f}")
    col3.metric("Financial", f"{latest[3]:.0f}")
    col4.metric("Governance", f"{latest[4]:.0f}")

    st.metric("Overall Risk Score", f"{latest[5]:.2f}")

    if "LOW" in latest[6]:
        st.success(latest[6])
    elif "MODERATE" in latest[6]:
        st.warning(latest[6])
    else:
        st.error(latest[6])