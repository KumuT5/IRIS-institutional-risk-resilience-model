import streamlit as st

# Safe import (prevents app crash if DB breaks)
try:
    from database import save_contact_message
except:
    save_contact_message = None


def show_contact():

    # ---------------- WRAPPER ----------------
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    # ---------------- TITLE ----------------
    st.title("Contact Us")
    st.caption("We’d love to hear from you")

    st.markdown("---")

    # ---------------- FORM ----------------
    with st.form("contact_form"):

        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        company = st.text_input("Organization (optional)")
        message = st.text_area("Your Message")

        submit = st.form_submit_button("Send Message")

    # ---------------- VALIDATION + ACTION ----------------
    if submit:

        # REQUIRED FIELDS
        if not name:
            st.error("Name is required")
            return

        if not email:
            st.error("Email is required")
            return

        if not message:
            st.error("Message cannot be empty")
            return

        # DEFAULT VALUE
        if not company:
            company = "Individual User"

        # SAVE TO DB (safe)
        if save_contact_message:
            save_contact_message(
            company_name=company,
            message=message,
            msg_type="review"
            )
        else:
            st.warning("Database not connected. Message not saved.")

        # SUCCESS UI
        st.success("✅ Message sent successfully!")
        st.info("Our team will get back to you soon.")

        # OPTIONAL RESET (clean UX)
        
        st.rerun()

    # ---------------- WRAPPER CLOSE ----------------
    st.markdown('</div>', unsafe_allow_html=True)
