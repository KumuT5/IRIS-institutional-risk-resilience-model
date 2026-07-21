import streamlit as st
from modules.admin_auth import handle_admin_login

def admin_login_page():

    st.title("Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", key="admin_login_btn"):

        # ✅ Validation
        if not username or not password:
            st.error("All fields required")
            return

        admin = handle_admin_login(username, password)

        if admin:
            # 🔐 Set session
            st.session_state["admin_id"] = admin[0]
            st.session_state["admin_name"] = admin[1]
            st.session_state["logged_in"] = True
            st.session_state["role"] = "admin"

            # 🔁 Route to dashboard
            st.session_state["page"] = "admin_dashboard"
            st.write("DEBUG SESSION:", st.session_state)


            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")
