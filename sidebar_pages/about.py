import streamlit as st

def show_about():
    st.title("About IRIS")

    st.write("""
    IRIS (Intelligent Risk & Resilience System) is designed to help organizations
    assess, monitor, and improve their cybersecurity posture.

    It combines structured risk evaluation with intelligent insights to provide
    actionable recommendations for resilience.
    """)

    st.subheader("Core Objective")
    st.write("To provide a centralized system for institutional risk assessment and decision support.")
