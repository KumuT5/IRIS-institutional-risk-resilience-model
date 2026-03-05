import streamlit as st
import sqlite3
import pandas as pd

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please login first.")
    st.stop()

if "username" not in st.session_state:
    st.error("Please login first.")
    st.stop()

current_user = st.session_state["username"]

st.set_page_config(page_title="Final Risk Score Card", layout="wide")

st.title("📊 Final Institutional Risk Score Card")

# ------------------------------
# DATABASE CONNECTION
# ------------------------------
conn = sqlite3.connect("risk_management.db", check_same_thread=False)

df = pd.read_sql_query(
    "SELECT * FROM assessments WHERE username = ? AND company_name = ?",
    conn,
    params=(current_user, st.session_state["company_name"])
)

if df.empty:
    st.warning("No assessment records available.")
    st.stop()

# ------------------------------
# COMPANY SELECTION
# ------------------------------
col1, col2 = st.columns(2)

with col1:
    company_list = df["company_name"].unique()
    selected_company = st.selectbox("Select Company", company_list)

company_data = df[df["company_name"] == selected_company]

with col2:
    selected_date = st.selectbox(
        "Select Assessment Date",
        company_data["assessment_date"].sort_values(ascending=False)
    )

record = company_data[company_data["assessment_date"] == selected_date].iloc[0]

digital_score = record["digital_score"]
human_score = record["human_score"]
financial_score = record["financial_score"]
governance_score = record["governance_score"]
overall_score = record["overall_score"]
risk_level = record["risk_level"]

st.markdown("---")

# ------------------------------
# BIG SCORE DISPLAY
# ------------------------------
st.markdown(f"""
<div style='padding:40px;
            border-radius:18px;
            background: linear-gradient(135deg,#111827,#1f2937);
            text-align:center'>
    <h2 style='color:white;'>Overall Risk Score</h2>
    <h1 style='color:#f87171;font-size:72px;'>{round(overall_score,2)}</h1>
    <h3 style='color:#facc15;'>Classification: {risk_level}</h3>
    <p style='color:#9ca3af;'>Assessment Date: {selected_date}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# ------------------------------
# DOMAIN CARDS
# ------------------------------
st.subheader("📌 Domain Risk Breakdown")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Digital", round(digital_score,2))
col2.metric("Human", round(human_score,2))
col3.metric("Financial", round(financial_score,2))
col4.metric("Governance", round(governance_score,2))

# ------------------------------
# BAR CHART
# ------------------------------
chart_data = pd.DataFrame({
    "Domain": ["Digital", "Human", "Financial", "Governance"],
    "Score": [digital_score, human_score, financial_score, governance_score]
})

st.subheader("📈 Risk Distribution")
st.bar_chart(chart_data.set_index("Domain"))

# ------------------------------
# TREND GRAPH
# ------------------------------
st.subheader("📉 Risk Trend Over Time")

trend = company_data.sort_values("assessment_date")
st.line_chart(trend.set_index("assessment_date")["overall_score"])

# ------------------------------
# RECOMMENDATION ENGINE
# ------------------------------
st.subheader("🛡 System Recommendations")

if digital_score > 60:
    st.write("• Improve cybersecurity posture and reduce patch delays.")

if financial_score > 70:
    st.write("• Strengthen liquidity and reduce debt exposure.")

if governance_score > 60:
    st.write("• Increase audit frequency and compliance monitoring.")

if human_score > 60:
    st.write("• Improve workforce training and retention strategy.")

if overall_score <= 30:
    st.success("Overall risk is within acceptable tolerance.")

elif overall_score <= 60:
    st.warning("Moderate exposure detected. Preventive actions advised.")

elif overall_score <= 80:
    st.error("High exposure. Strategic intervention required.")

else:
    st.error("Critical exposure. Immediate executive action necessary.")

st.markdown("---")

# ------------------------------
# REFRESH BUTTON
# ------------------------------
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()