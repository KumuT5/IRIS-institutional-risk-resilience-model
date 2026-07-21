import streamlit as st
import sqlite3
import pandas as pd
from database import get_all_company_stats
from database import load_risk_config
from database import get_connection, update_thresholds
from database import save_risk_config

def risk_settings():

    st.subheader("Risk Threshold Settings")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scoring_config WHERE id = 1")
    config = cursor.fetchone()
    conn.close()

    low = st.number_input("Low Risk Limit", value=config["low_threshold"])
    med = st.number_input("Medium Risk Limit", value=config["medium_threshold"])
    high = st.number_input("High Risk Limit", value=config["high_threshold"])

    if st.button("Save"):
        if not (low < med < high):
            st.error("Low < Medium < High required")
        else:
            update_thresholds(low, med, high)
            st.success("Updated Successfully")


def admin_dashboard():

    # 🔐 AUTH CHECK
    if st.session_state.get("role") != "admin":
        st.error("Unauthorized")
        st.stop()

    # ---------------- STYLE ----------------
    st.markdown("""
    <style>
    .stApp { background: #020617; color: white; }
    .topbar {
        display:flex; justify-content:space-between;
        padding:15px; border:1px solid #00f7ff;
        border-radius:10px; margin-bottom:20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- TOP BAR ----------------
    st.markdown(f"""
    <div class="topbar">
        <div><b>IRIS SYSTEM</b></div>
        <div>
            ID: {st.session_state.get("admin_id")} |
            {st.session_state.get("admin_name")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- NAV ----------------
    col1, col2, col3 = st.columns(3)

    if col1.button("📂 Database", key="nav_db"):
        st.session_state["view"] = "db"

    if col2.button("📊 Analytics", key="nav_analytics"):
        st.session_state["view"] = "analytics"

    if col3.button("⚙️ Config", key="nav_config"):
        st.session_state["view"] = "config"

    view = st.session_state.get("view", "db")

    # 🔁 FETCH DATA ONCE
    data = get_all_company_stats()

    # ---------------- DATABASE ----------------
    if view == "db":

        st.subheader("Company Data")

        if not data:
            st.info("No company data available")
        else:
            df_db = pd.DataFrame(data)

            df_db.columns = [
                "Company ID",
                "Company Name",
                "Visits",
                "Reviews"
            ]

            st.dataframe(
                 df_db,
                 use_container_width=True,
            hide_index=True
        )

    # ---------------- ANALYTICS ----------------
    elif view == "analytics":

        if not data:
            st.info("No analytics data available")
        else:
            total = sum([d["usage_count"] for d in data])

            col1, col2 = st.columns(2)
            col1.metric("Total Visits", total)
            col2.metric("Companies", len(data))

        pos_words, neg_words = load_risk_config()

        positive = 0
        negative = 0
        neutral = 0

        for d in data:
            review = (d.get("message") or "").lower()

            if any(word in review for word in pos_words):
                positive += 1
            elif any(word in review for word in neg_words):
                negative += 1
            else:
                neutral += 1

        st.subheader("Review Insights")

        st.write(f"Positive: {positive}")
        st.write(f"Negative: {negative}")
        st.write(f"Needs Improvement: {neutral}")       

    

        df = pd.DataFrame(data)

        st.bar_chart(
        df.set_index("company_name")["usage_count"]
        )


    # ---------------- CONFIG ----------------
    elif view == "config":
        
        st.subheader("Config")

        risk_settings()
        
        # 🔐 Change Password
        new_pass = st.text_input("New Password", type="password", key="new_pass")

        if st.button("Update Password", key="update_pass"):
            if not new_pass:
                st.error("Password cannot be empty")
            else:
                conn = sqlite3.connect("risk_management.db")
                cursor = conn.cursor()

                cursor.execute(
                    "UPDATE admin SET password=? WHERE id=?",
                    (new_pass, st.session_state["admin_id"])
                )

                conn.commit()
                conn.close()

                st.success("Password updated")

        # ➕ Add New Admin
        st.subheader("Add Admin")

        u = st.text_input("Username", key="new_admin_user")
        p = st.text_input("Password", type="password", key="new_admin_pass")

        if st.button("Create Admin", key="create_admin"):
            if not u or not p:
                st.error("All fields required")
            else:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()

                try:
                    cursor.execute(
                        "INSERT INTO admin (username, password) VALUES (?, ?)",
                        (u, p)
                    )
                    conn.commit()
                    st.success("Admin created")
                except:
                    st.error("Admin already exists")

                conn.close()

            st.subheader("Risk Configuration")

            positive_words = st.text_input(
                "Positive Keywords (comma separated)",
                value="good,great,excellent",
                key="pos_words"
            )

            negative_words = st.text_input(
                "Negative Keywords (comma separated)",
                value="bad,error,poor",
                key="neg_words"
            )

            if st.button("Save Risk Settings", key="save_risk"):
                save_risk_config(positive_words, negative_words)
                st.success("Risk configuration saved")      

    # ---------------- LOGOUT ----------------
    if st.button("Logout", key="logout_btn"):
        st.session_state.clear()
        st.rerun()
