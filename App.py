import streamlit as st
from global_ui import apply_global_ui

st.set_page_config(layout="wide")            

from sidebar_public import render_public_sidebar

from database import create_tables   
create_tables()

# -------------------------------
# SESSION INIT
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

page = st.session_state.page

home_pages = [
    "home",
    "about",
    "features",
    "how_it_works",
    "why_iris",
    "contact"
]

apply_global_ui(
    r"assets/IRIS LOGO.jfif",

    show_top_buttons=(page == "home"),

    show_hero=(page == "home")
)


# -------------------------------
# AUTH PROTECTION
# -------------------------------

if page == "user_dashboard":

    if (
        not st.session_state.get("logged_in")
        or st.session_state.get("role") != "user"
    ):
        st.session_state.page = "login_user"
        st.rerun()

elif page == "admin_dashboard":

    if (
        not st.session_state.get("logged_in")
        or st.session_state.get("role") != "admin"
    ):
        st.session_state.page = "login_admin"
        st.rerun()
# -------------------------------
# PUBLIC PAGES LIST (MATCHES sidebar_pages/)
# -------------------------------
public_pages = [
    "home",
    "about",
    "features",
    "how_it_works",
    "why_iris",
    "contact"
]

# -------------------------------
# SIDEBAR CONTROL
# -------------------------------
if st.session_state.page in public_pages:
    render_public_sidebar()
# -------------------------------
# ROUTING SYSTEM
# -------------------------------

# -------- PUBLIC --------
if page == "home":
    from sidebar_pages.home import show_home
    show_home()

elif page == "about":
    from sidebar_pages.about import show_about
    show_about()

elif page == "features":
    from sidebar_pages.features import show_features
    show_features()

elif page == "how_it_works":
    from sidebar_pages.how_it_works import show_how_it_works
    show_how_it_works()

elif page == "why_iris":
    from sidebar_pages.why_iris import show_why_iris
    show_why_iris()

elif page == "contact":
    from sidebar_pages.contact import show_contact
    show_contact()

# -------- AUTH --------
elif page == "login_user":
    from views.login_user import login_user_page
    login_user_page()

elif page == "register_user":
    from views.register_user import register_user_page
    register_user_page()

elif page == "login_admin":
    from views.admin.login_admin import admin_login_page
    admin_login_page()
    
elif page == "register_admin":
    from views.admin.register_admin import register_admin_page
    register_admin_page()
    
# -------- DASHBOARDS --------
elif page == "user_dashboard":
    from views.user_dashboard import user_dashboard
    user_dashboard()

elif page == "admin_dashboard":
    from views.admin.admin_dashboard import admin_dashboard
    admin_dashboard()
