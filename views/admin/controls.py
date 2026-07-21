import streamlit as st
import sqlite3

def admin_controls():

    # 🔐 PROTECTION
    if st.session_state.get("role") != "admin":
        st.error("Unauthorized")
        st.stop()

    st.title("Admin Controls")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # 🔥 SYSTEM CONTROL
    st.subheader("System Control")

    if st.button("⚠️ Trigger System Alert", key="alert_btn"):
        st.warning("System Alert Triggered")

    # 📊 COMPANY VIEW (PRIVACY SAFE)
    st.subheader("Company Insights")

    cursor.execute("""
    SELECT 
        u.id,
        u.username,
        COUNT(m.id),
        GROUP_CONCAT(m.message, ' | ')
    FROM users u
    LEFT JOIN messages m ON u.id = m.user_id
    GROUP BY u.id
    """)

    data = cursor.fetchall()

    if not data:
        st.info("No company data available")
    else:
        for row in data:
            company_id = row[0]
            company_name = row[1]
            frequency = row[2]
            reviews = row[3] if row[3] else "-"

            st.markdown(f"""
            ---
            **Company ID:** {company_id}  
            **Name:** {company_name}  
            **Visit Frequency:** {frequency}  
            **Reviews:** {reviews}
            """)

    conn.close()
