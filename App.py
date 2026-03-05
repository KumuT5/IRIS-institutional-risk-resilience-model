import streamlit as st
from database import create_tables

st.set_page_config(
    page_title="IRIS",
    page_icon="🛡️",
    layout="wide"
)

create_tables()
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ================== STYLING ==================
st.markdown("""
<style>

/* ================= Main Container ================= */
.block-container {
    padding-top: 2rem;
    padding-left: 4rem;
    padding-right: 4rem;
}

/* ================= Section Divider ================= */
.section-line {
    height: 1px;
    background-color: #E5E7EB;
    margin-top: 40px;
    margin-bottom: 40px;
}

/* ================= Sidebar Brand ================= */
.sidebar-brand {
    background-color: #F3F4F6;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 20px;
}

.sidebar-brand-title {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
}

.sidebar-brand-sub {
    font-size: 13px;
    color: #6B7280;
    margin-top: 5px;
}

/* ================= Sidebar Info ================= */
.sidebar-info {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 14px;
    font-size: 13px;
    line-height: 1.6;
    color: #374151;
    border: 1px solid #E5E7EB;
}

/* ================= Main Title ================= */
.main-title {
    font-size: 30px;
    font-weight: 700;
    margin-top: 10px;
    color: #111827;
}

.full-form {
    font-size: 15px;
    color: #6B7280;
    margin-bottom: 20px;
}

/* ================= Executive Dark Cards ================= */
.dark-card {
    background-color: #111827;
    padding: 25px;
    border-radius: 18px;
    margin-top: 20px;
    border: 1px solid #1F2937;
    transition: all 0.3s ease;
    min-height: 160px;
}

.dark-card:hover {
    transform: translateY(-5px);
    border: 1px solid #2563EB;
}

.card-title {
    color: #FFFFFF;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 12px;
}

.card-text {
    color: #9CA3AF;
    font-size: 14px;
    line-height: 1.6;
}

/* ================= Status Box ================= */
.status-box {
    background-color: #F9FAFB;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #E5E7EB;
    font-size: 14px;
    line-height: 1.7;
    margin-top: 20px;
}

/* ================= Optional Executive Header ================= */
.section-header {
    font-size: 22px;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 10px;
    color: #111827;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:

    # Section 2 — IRIS Brand Block
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">IRIS</div>
        <div class="sidebar-brand-sub">
            Institutional Risk Intelligence System
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Section Divider
    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Navigation")

    

    # Section 3 — Relevant Elegant Content
    st.markdown("""
    <div class="sidebar-info">
    <b>Risk Intelligence Framework</b><br><br>
    Structured domain evaluation.<br>
    Weighted institutional modeling.<br>
    Longitudinal risk visibility.
    </div>
    """, unsafe_allow_html=True)

# ================= MAIN SECTION =================
#LOGO
  
st.markdown('<div class="main-title">🛡 IRIS</div>', unsafe_allow_html=True)
# Full Form
st.markdown(
    '<div class="full-form">Institutional Risk Intelligence System</div>',
    unsafe_allow_html=True
)

# Section Divider
st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

# Body
st.markdown("""
### Strategic Risk Visibility for Modern Institutions

IRIS transforms institutional metrics into executive-grade insight.

By integrating digital, human, financial, and governance risk domains,
the system enables proactive risk identification, structured evaluation,
and long-term stability monitoring.

Designed for clarity. Built for intelligence.
""")

# ================== Executive Insight Cards ==================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="dark-card">
        <div class="card-title">Risk Mapping</div>
        <div class="card-text">
            Cross-domain identification of digital, human,
            financial, and governance exposure layers.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="dark-card">
        <div class="card-title">Weighted Scoring</div>
        <div class="card-text">
            Dynamic likelihood-impact modeling with
            structured executive-grade risk prioritization.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="dark-card">
        <div class="card-title">Longitudinal Monitoring</div>
        <div class="card-text">
            Institutional stability tracking across time
            with adaptive intelligence calibration.
        </div>
    </div>
    """, unsafe_allow_html=True)

# System Status Section
st.markdown("""
<div class="status-box">
<b>System Status</b><br><br>
🟢 Application Running<br>
🟢 SQLite Database Active<br>
🟢 Risk Engine Initialized
</div>
""", unsafe_allow_html=True)