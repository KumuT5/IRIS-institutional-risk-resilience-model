import streamlit as st
from database import admin_exists

def show_home():

    # ---------- GLOBAL STYLE ----------
    st.markdown("""
    <style>

    /* ---- MAIN APP ---- */
    .stApp {
        background: linear-gradient(180deg, #020617, #020617);
        color: #e2e8f0;
    }

    /* ---- REMOVE EXTRA SPACE ---- */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* ---- SIDEBAR ---- */
    [data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid rgba(56,189,248,0.2);
    }

    /* ---- SIDEBAR BUTTONS ---- */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border: 1px solid #38bdf8;
        color: #38bdf8;
        background: transparent;
        border-radius: 8px;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #38bdf8;
        color: black;
    }

    /* ---- MAIN BUTTONS ---- */
    div.stButton > button {
        border: 1px solid #38bdf8;
        background: transparent;
        color: #38bdf8;
        border-radius: 8px;
    }

    div.stButton > button:hover {
        background: #38bdf8;
        color: black;
    }

    /* ---- TITLE ---- */
    .title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        color: #38bdf8;
    }

    .subtitle {
        text-align: center;
        color: #94a3b8;
        margin-bottom: 25px;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------- HEADER ----------
    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.markdown('<div class="title">IRIS</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Intelligent Risk & Resilience System</div>', unsafe_allow_html=True)

    # ---------- NAV BUTTONS ----------
    colA, colB, colC, colD = st.columns(4)

    with colA:
        if st.button("👤 User"):
            st.session_state.page = "register_user"
            st.rerun()

    with colB:
        if st.button("🔐 Admin"):
            st.session_state.page = "login_admin"
            st.rerun()

    with colC:
        if st.button("📝 Register"):
            st.session_state.page = "register_user"
            st.rerun()

    with colD:
        if not admin_exists():
            if st.button("⚙ Setup"):
                st.session_state.page = "register_admin"
                st.rerun()

    st.divider()

    # ---------- WHAT IS IRIS ----------
    st.markdown("## What is IRIS?")
    st.write(
        "IRIS is an intelligent system designed to assess, monitor, and improve "
        "cybersecurity resilience across institutions in real time."
    )

    # ---------- FEATURES ----------
    st.markdown("## Key Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.container(border=True)
        st.markdown("**AI Risk Analysis**")
        st.write("Detect threats using intelligent scoring models.")

    with col2:
        st.container(border=True)
        st.markdown("**Real-Time Monitoring**")
        st.write("Continuously track vulnerabilities and system health.")

    with col3:
        st.container(border=True)
        st.markdown("**Secure Data Handling**")
        st.write("Ensure encrypted and protected data pipelines.")

    # ---------- STATS ----------
    st.markdown("## Impact")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Institutions", "250+")

    with c2:
        st.metric("Accuracy", "95%")

    with c3:
        st.metric("Monitoring", "24/7")

    # ---------- CONTACT ----------
    st.markdown("## Quick Feedback")

    email = st.text_input("Email")
    message = st.text_area("Message")

    if st.button("Submit"):
        if not message:
            st.error("Message required")
        else:
            st.success("Submitted successfully")
