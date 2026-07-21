import streamlit as st

def render_public_sidebar():

    if "page" not in st.session_state:
        st.session_state.page = "home"

    menu = [
        ("🏠 Home", "home"),
        ("🛡️ About IRIS", "about"),
        ("⚙️ Key Features", "features"),
        ("🔄 How It Works", "how_it_works"),
        ("⭐ Why IRIS?", "why_iris"),
        
        ("✉️ Contact Us", "contact"),
    ]

    for label, key in menu:
        if st.sidebar.button(label, key=f"nav_{key}"):
            st.session_state.page = key
            st.rerun()

    return st.session_state.page
