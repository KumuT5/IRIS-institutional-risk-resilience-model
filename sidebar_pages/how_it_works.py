import streamlit as st

def show_how_it_works():
    st.title("How IRIS Works")

    st.write("IRIS follows a structured 4-step workflow:")

    st.markdown("""
    1. **Data Input** – Organization submits system/security data  
    2. **Risk Evaluation** – System analyzes based on predefined parameters  
    3. **Scoring Engine** – Generates risk scorecard  
    4. **Insights & Recommendations** – Actionable outputs for improvement  
    """)

    st.success("Simple workflow. Powerful outcomes.")
