import streamlit as st
from modules import user_auth
import re

def register_user_page():
    st.title("User Registration")

    with st.form("register_form"):
        company_name = st.text_input("Company Name")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submit = st.form_submit_button("Register")

    if submit:
        if not re.match("^[A-Za-z0-9]+$", username):
           st.error("Username must be alphanumeric only")

        result = user_auth.handle_user_register(company_name,username, email, password)

        if result == "success":
            st.success("Registration successful! Please login.")
            st.session_state.page = "login_user"
            st.rerun()
        else:
            st.error(result)
