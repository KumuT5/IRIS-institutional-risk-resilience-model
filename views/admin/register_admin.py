import streamlit as st
from database import admin_exists
from modules.admin_auth import handle_admin_register

def register_admin_page():

    # 🔒 Allow only if NO admin exists
    if admin_exists():
        st.error("Admin already exists. Registration disabled.")
        st.stop()

    st.title("Initial Admin Setup")

    username = st.text_input("Admin Username")
    password = st.text_input("Password", type="password")

    if st.button("Create Admin", key="create_admin_btn"):

        # ✅ Basic validation
        if not username or not password:
            st.error("All fields required")
            return

        result = handle_admin_register(username, password)

        if result == "Admin created":
            st.success("Admin created successfully")

            # 🔁 Redirect to login
            st.session_state["page"] = "admin_login"
            st.rerun()
        else:
            st.error("Admin already exists or error occurred")
