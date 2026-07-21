import streamlit as st
from modules.user_auth import handle_user_login

def login_user_page():
    st.title("User Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user, message = handle_user_login(username,  password)

        if user:
            st.session_state["user"] = dict(user)
            st.session_state["role"] = "user"
            st.session_state["logged_in"] = True

            st.session_state["page"] = "user_dashboard"
            st.success("Login successful")
            st.write(user)
            st.rerun()
        else:
            st.error(message)

        
