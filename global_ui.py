import streamlit as st


def apply_global_ui(
    logo_path=None,
    show_top_buttons=False,
    show_hero=False
):

    # ===============================
    # GLOBAL THEME (ALL PAGES)
    # ===============================
    st.markdown("""
    <style>
    body {
        background-color: #020617;
    }

    /* Global buttons (clean + glow) */
    div[data-testid="stButton"] button {
        border-radius: 10px;
        border: 1px solid #2a2a2a;
        background-color: #0e1117;
        color: white;
        font-weight: 500;
        transition: 0.2s ease;
    }

    div[data-testid="stButton"] button:hover {
        border-color: #4a90e2;
        box-shadow: 0 0 10px rgba(74,144,226,0.4);
        transform: translateY(-1px);
    }

       
    </style>
    """, unsafe_allow_html=True)

    current_page = st.session_state.get("page", "home")

    show_back = current_page != "home"
    # ===============================
    # SIDEBAR (CONTROLLED)
    # ===============================
    if logo_path:
        with st.sidebar:
            st.image(logo_path, width=140)
            st.markdown("---")
                        # 🔙 GLOBAL BACK BUTTON
        if show_back:

            if st.button("⬅ Back", key="global_back_btn"):

                    public_pages = [
                        "about",
                        "features",
                        "how_it_works",
                        "why_iris",
                        "contact"
                    ]

                    auth_pages = [
                        "login_user",
                        "register_user",
                        "login_admin",
                        "register_admin"
                    ]

                    dashboard_pages = [
                        "user_dashboard",
                        "admin_dashboard"
                    ]

                    if current_page in public_pages:
                        st.session_state.page = "home"

                    elif current_page in auth_pages:
                        st.session_state.page = "home"

                    elif current_page in dashboard_pages:

                        if st.session_state.get("role") == "admin":
                            st.session_state.page = "login_admin"

                        else:
                           st.session_state.page = "login_user"

                    st.rerun()

            
            # 👉 ONLY HOME SHOWS NAV
            if show_top_buttons:

                if st.button("🏠 Home"):
                    st.session_state.page = "home"
                    st.rerun()

                if st.button("🛡️ About IRIS"):
                    st.session_state.page = "about"
                    st.rerun()

                if st.button("⚙️ Key Features"):
                    st.session_state.page = "features"
                    st.rerun()

                if st.button("🔄 How It Works"):
                    st.session_state.page = "how_it_works"
                    st.rerun()

                if st.button("⭐ Why IRIS"):
                    st.session_state.page = "why_iris"
                    st.rerun()

                if st.button("✉️ Contact Us"):
                    st.session_state.page = "contact"
                    st.rerun()        

    # ===============================
    # HOME ONLY (HEADER + TOP BUTTONS)
    # ===============================
    if show_hero or show_top_buttons:

        left, right = st.columns([4, 2])

        # ---- LEFT: TITLE ----
        with left:
            if show_hero:
                st.markdown("## IRIS")
                st.markdown("### Intelligent Risk & Resilience System")

        # ---- RIGHT: ACTION BUTTONS (HOME ONLY) ----
        with right:
            if show_top_buttons:

                b1, b2, b3 = st.columns(3)

                with b1:
                    if st.button("User"):
                        st.session_state.page = "login_user"
                        st.rerun()

                with b2:
                    if st.button("Register"):
                        st.session_state.page = "register_user"
                        st.rerun()

                with b3:
                    if st.button("Admin"):
                        st.session_state.page = "login_admin"
                        st.rerun()

        st.markdown("---")

    # ===============================
    # HOME BODY ONLY
    # ===============================
    if show_hero:

        st.write("""
        IRIS helps organizations analyze cybersecurity risks, detect vulnerabilities,
        and improve resilience through intelligent assessment and scoring.
        """)

        st.markdown("###")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.info("🔍 Risk Analysis")

        with c2:
            st.info("🛡️ Security Insights")

        with c3:
            st.info("📊 Smart Scoring")
