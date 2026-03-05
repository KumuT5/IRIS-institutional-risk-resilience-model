import streamlit as st
import sqlite3
from database import get_connection

st.title("User Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username.strip() == "" or password.strip() == "":
        st.warning("All fields required.")
    else:
        conn = get_connection()
        cursor = conn.cursor()

        user = cursor.execute(
            "SELECT username, company_name FROM LOGINS WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:
            st.session_state["logged_in"] = True 
            st.session_state["username"] = user[0]
            st.session_state["company_name"] = user[1]
            st.success("Login successful.")
            
        else:
            st.error("Invalid credentials.")