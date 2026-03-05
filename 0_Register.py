import streamlit as st
from database import get_connection

st.title("User Registration")

company_name = st.text_input("Company Name")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if company_name.strip() == "" or username.strip() == "" or password.strip() == "":
        st.warning("All fields are required.")
    else:
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO LOGINS (username, password, company_name)
                VALUES (?, ?, ?)
            """, (username, password, company_name))

            conn.commit()
            st.success("Registration successful. Please login.")
            

        except Exception as e:
            st.error("Username already exists.")

        conn.close()