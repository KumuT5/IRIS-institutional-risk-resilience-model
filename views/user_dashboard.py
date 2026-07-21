import streamlit as st
from database import get_user_history
from modules.New_Assessment import new_assessment
from modules.Final_Score_Card import final_score_card
from modules.Assessment_history import assessment_history


def user_dashboard():

    # ---------------- MAIN PAGE (DO NOT TOUCH THIS SYSTEM) ----------------
    if "page" not in st.session_state:
        st.session_state.page = "user_dashboard"

    # ---------------- DASHBOARD INTERNAL PAGE ----------------
    if "dashboard_page" not in st.session_state:
        st.session_state.dashboard_page = "home"

    user = st.session_state.get("user")

    # ---------------- SAFETY ----------------
    if not user:
        st.error("Login required")
        st.stop()

    # convert sqlite row → dict
    if not isinstance(user, dict):
        try:
            user = dict(user)
            st.session_state["user"] = user
        except:
            st.error("User session corrupted")
            st.write(user)
            st.stop()

    
    # ---------------- TOP BAR ----------------
    col1, col2 = st.columns([8, 1])

    with col1:
        st.markdown(
            f'<div class="username">👤 {user["username"]} | 🏢 {user["company_name"]}</div>',
            unsafe_allow_html=True
        )

    with col2:
        if st.button("Logout", key="logout_btn"):
            st.session_state.clear()
            st.rerun()

    # ---------------- BACK BUTTON ----------------
    if st.session_state.dashboard_page != "home":
        if st.button("⬅ Back", key="back_btn"):
            st.session_state.dashboard_page = "home"
            st.rerun()

    # ============================================================
    # 🏠 HOME DASHBOARD
    # ============================================================
    if st.session_state.dashboard_page == "home":

        st.markdown("## Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🧪 Start Assessment", key="start_btn"):
                st.session_state.dashboard_page = "assessment"
                st.rerun()

        with col2:
            if st.button("📊 View Scorecard", key="score_btn"):
                st.session_state.dashboard_page = "scorecard"
                st.rerun()

        with col3:
            if st.button("🕘 Insights", key="history_btn"):
                st.session_state.dashboard_page = "history"
                st.rerun()

    # ============================================================
    # 🧪 ASSESSMENT
    # ============================================================
    elif st.session_state.dashboard_page == "assessment":
        new_assessment()

    # ============================================================
    # 📊 SCORECARD
    # ============================================================
    elif st.session_state.dashboard_page == "scorecard":
        final_score_card()

    # ============================================================
    # 🕘 HISTORY
    # ============================================================
    elif st.session_state.dashboard_page == "history":
        assessment_history()

    else:
        st.error(f"Invalid dashboard state: {st.session_state.dashboard_page}")
