# ADS_app.py — A05.2 (iOS buttons, enhanced validation, animations, WhatsApp, stable)

import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from PIL import Image
import io

try:
    import qrcode
except ImportError:
    qrcode = None

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="AARA Dance Studio",
    page_icon="💃",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# DATA PATHS
# ---------------------------------------------------------
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
REG_FILE = os.path.join(DATA_DIR, "registrations.csv")
VISIT_FILE = os.path.join(DATA_DIR, "site_visits.csv")
LOGO_PATH = "logo.png"

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False
if "theme" not in st.session_state:
    st.session_state.theme = "light"

params = st.query_params
if "page" in params:
    st.session_state.page = params["page"]

page = st.session_state.page
theme = st.session_state.theme

# ---------------------------------------------------------
# THEME COLORS
# ---------------------------------------------------------
if theme == "light":
    PRIMARY = "#b8860b"
    PRIMARY_HOVER = "#a0750a"
    ACCENT = "#111827"
    MUTED = "#f7f7fa"
    CARD = "#ffffff"
    BORDER = "#e6e6e8"
    TEXT = "#111827"
else:
    PRIMARY = "#facc6b"
    PRIMARY_HOVER = "#e0b45f"
    ACCENT = "#f9fafb"
    MUTED = "#020617"
    CARD = "#020617"
    BORDER = "#1f2937"
    TEXT = "#f9fafb"

# ---------------------------------------------------------
# CSS (A05.2)
# ---------------------------------------------------------
CSS = f"""
<style>

:root {{
    color-scheme: light dark;
}}

html, body, [data-testid="stAppViewContainer"] {{
    background-color: {MUTED} !important;
    color: {TEXT} !important;
    transition: background-color 0.3s ease, color 0.3s ease;
}}

[data-testid="stSidebar"] {{
    background-color: {CARD} !important;
}}

* {{
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui;
}}

.block-container {{
  padding-top: 1rem;
  max-width: 900px;
  animation: fadeIn 0.4s ease;
}}

@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(6px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

.header {{
  display:flex; align-items:center; gap:14px;
  padding:10px 14px; background:{CARD};
  border-radius:14px; border:1px solid {BORDER};
  box-shadow:0 6px 18px rgba(17,24,39,0.12);
  margin-bottom:14px;
}}

.logo-wrap {{
  width:72px; height:72px; display:flex;
  align-items:center; justify-content:center;
  overflow:hidden; border-radius:14px;
}}

.brand-title {{
  font-weight:700; color:{TEXT}; font-size:1.1rem;
}}
.brand-sub {{
  font-size:0.8rem; color:#9ca3af;
}}

.nav-top {{
  margin-left:auto; display:flex; gap:8px;
}}
.nav-top a {{
  padding:8px 12px; border-radius:999px;
  text-decoration:none; color:{TEXT};
  font-size:0.9rem;
}}
.nav-top a.active {{
  background:{PRIMARY}; color:white;
}}

.section {{
  background:{CARD}; padding:14px;
  border-radius:12px; border:1px solid {BORDER};
  margin-bottom:12px;
}}

.title {{
  font-size:1.25rem; font-weight:700; color:{TEXT};
}}
.subtitle {{
  font-size:0.9rem; color:#9ca3af; margin-bottom:10px;
}}

.class-card {{
  padding:10px; border-radius:10px;
  background:rgba(15,23,42,0.03); border:1px solid {BORDER};
  margin-bottom:8px;
}}

.btn-primary {{
  display:inline-block;
  padding:10px 20px;
  background:{PRIMARY};
  color:white !important;
  border-radius:999px;
  text-decoration:none;
  font-weight:600;
  transition: background 0.2s ease;
}}
.btn-primary:hover {{
  background:{PRIMARY_HOVER};
}}

.btn-secondary {{
  display:inline-block;
  padding:10px 20px;
  background:white;
  color:{TEXT} !important;
  border-radius:999px;
  border:1px solid #d1d5db;
  text-decoration:none;
  font-weight:500;
  transition: background 0.2s ease;
}}
.btn-secondary:hover {{
  background:#f2f2f7;
}}

.required-label::after {{
    content: " *";
    color: #e11d48;
    font-weight: 700;
}}

.error-field input,
.error-field textarea,
.error-field select {{
    border-color: #e11d48 !important;
    box-shadow: 0 0 0 1px rgba(225,29,72,0.4);
}}

@keyframes shake {{
  10%, 90% {{ transform: translateX(-1px); }}
  20%, 80% {{ transform: translateX(2px); }}
  30%, 50%, 70% {{ transform: translateX(-4px); }}
  40%, 60% {{ transform: translateX(4px); }}
}}

.shake {{
  animation: shake 0.3s ease-in-out;
}}

.footer {{
  text-align:center; color:#9ca3af;
  font-size:0.8rem; margin-top:40px; margin-bottom:60px;
}}

.bottom-nav {{
  position:fixed; bottom:0; left:0; right:0;
  background:{CARD}; border-top:1px solid {BORDER};
  display:flex; justify-content:space-around;
  padding:8px 0; z-index:999;
}}
.bottom-nav a {{
  text-decoration:none; font-size:0.8rem;
  color:{TEXT}; text-align:center;
}}
.bottom-nav a span {{
  display:block; font-size:1.1rem;
}}
.bottom-nav a.active {{
  color:{PRIMARY};
}}

.whatsapp-btn {{
  position:fixed;
  bottom:80px;
  right:20px;
  background:#25D366;
  color:white;
  padding:14px 16px;
  border-radius:50%;
  font-size:22px;
  text-decoration:none;
  box-shadow:0 4px 12px rgba(0,0,0,0.2);
}}

</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------
def log_visit():
    df = pd.DataFrame([{"timestamp": datetime.now().isoformat()}])
    if os.path.exists(VISIT_FILE):
        df.to_csv(VISIT_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(VISIT_FILE, index=False)

def save_registration(record):
    df = pd.DataFrame([record])
    if os.path.exists(REG_FILE):
        df.to_csv(REG_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(REG_FILE, index=False)

def read_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

log_visit()

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
def render_header():
    cols = st.columns([0.15, 0.65, 0.2])

    with cols[0]:
        st.markdown('<div class="header">', unsafe_allow_html=True)
        st.markdown('<div class="logo-wrap">', unsafe_allow_html=True)
        if os.path.exists(LOGO_PATH):
            try:
                img = Image.open(LOGO_PATH)
                st.image(img, width=72)
            except:
                st.write("")
        st.markdown('</div>', unsafe_allow_html=True)

    with cols[1]:
        st.markdown(
            f"""
            <div class="brand-title">AARA Dance Studio</div>
            <div class="brand-sub">Fate · Rockwall · Dallas, TX</div>
            """,
            unsafe_allow_html=True,
        )

    with cols[2]:
        home = "active" if page == "Home" else ""
        classes = "active" if page == "Classes" else ""
        reg = "active" if page == "Register" else ""
        admin = "active" if page == "Admin" else ""

        st.markdown(
            f"""
            <div class="nav-top">
              <a class="{home}" href="/?page=Home">Home</a>
              <a class="{classes}" href="/?page=Classes">Classes</a>
              <a class="{reg}" href="/?page=Register">Register</a>
              <a class="{admin}" href="/?page=Admin">Admin</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    toggle_label = "🌙 Dark mode" if theme == "light" else "☀️ Light mode"
    if st.button(toggle_label, key="theme_toggle"):
        st.session_state.theme = "dark" if theme == "light" else "light"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

render_header()

# ---------------------------------------------------------
# QR CODE
# ---------------------------------------------------------
def render_qr_section():
    if qrcode is None:
        return
    st.markdown("#### Quick Registration QR")
    base = st.request.url.split("?")[0] if hasattr(st, "request") else ""
    reg_url = base + "?page=Register"
    qr_img = qrcode.make(reg_url)
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)
    st.image(buf, caption="Scan to open registration page", width=140)

# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------
if page == "Home":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Welcome to AARA Dance Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Where passion meets performance.</div>', unsafe_allow_html=True)
    st.write("Choreography by **Mrs. Rekha Mahendran & Mahendran Ramachandran**")
    st.write("📍 **315 Spirehaven Dr, Rockwall, TX 75087**")
    st.markdown('<a class="btn-secondary" href="/?page=Classes">View Classes</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    render_qr_section()

# ---------------------------------------------------------
# CLASSES PAGE
# ---------------------------------------------------------
elif page == "Classes":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Programs & Fees</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="class-card"><b>Tiny Stars (Ages 5–8)</b><br>'
        'Beginner / Intermediate<br>'
        'Wed & Fri · 6:30–7:30 PM<br>'
        '4 classes: $60 · 8 classes: $100</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="class-card"><b>Shining Stars (Ages 9+)</b><br>'
        'Beginner / Intermediate<br>'
        'Tue · 7–8 PM<br>'
        '4 classes: $60 · 8 classes: $100</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="class-card"><b>Dream Chasers (Ladies 18+)</b><br>'
        'Beginner / Intermediate<br>'
        'Thu 6:30–7:30 PM · Sat 10:30–11:30 AM<br>'
        '4 classes: $50 · 8 classes: $80</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<a class="btn-primary" href="/?page=Register">Register Now</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# REGISTRATION PAGE (A05.2 Enhanced Validation)
# ---------------------------------------------------------
elif page == "Register":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Student Registration</div>', unsafe_allow_html=True)

    error_fields = set()

    with st.form("reg_form", clear_on_submit=False):

        st.subheader("Student Info")

        student_name = st.text_input("Student Name", key="student_name")
        st.markdown('<label class="required-label">Student Name</label>', unsafe_allow_html=True)

        dob = st.text_input("Date of Birth (Age)", key="dob", placeholder="e.g., Jan 2015 (9 yrs)")
        st.markdown('<label class="required-label">Date of Birth (Age)</label>', unsafe_allow_html=True)

        gender = st.selectbox("Gender", ["", "Female", "Male", "Other", "Prefer not to say"], key="gender")
        st.markdown('<label class="required-label">Gender</label>', unsafe_allow_html=True)

        school = st.text_input("School Name (optional)", key="school")

        st.subheader("Parent / Guardian")
        parent = st.text_input("Parent/Guardian Name", key="parent")
        phone = st.text_input("Phone Number", key="phone")
        email = st.text_input("Email Address", key="email")
        address = st.text_area("Address", key="address")

        st.subheader("Class Details")

        st.markdown('<label class="required-label">Enrollment Type</label>', unsafe_allow_html=True)
        enrollment = st.selectbox(
            "Enrollment Type",
            ["", "Regular ($50/month)", "Drop-in ($15/session)"],
            key="enroll"
        )

        st.markdown('<label class="required-label">Mode</label>', unsafe_allow_html=True)
        mode = st.radio("Mode", ["In-Person", "Online"], key="mode")

        workshops = st.multiselect(
            "Workshops",
            ["Ladies Kuthu Workshop", "Couple Dance Fitness Workshop"],
            key="workshops"
        )

        st.markdown('<label class="required-label">Level</label>', unsafe_allow_html=True)
        level = st.selectbox("Level", ["", "Beginner", "Intermediate", "Advanced"], key="level")

        st.markdown('<label class="required-label">Preferred Days/Time</label>', unsafe_allow_html=True)
        pref_time = st.text_input("Preferred Days/Time", key="pref_time")

        experience = st.text_area("Previous Experience", key="experience")

        st.subheader("Emergency Contact")
        em_name = st.text_input("Emergency Contact Name", key="em_name")
        em_rel = st.text_input("Relationship", key="em_rel")
        em_phone = st.text_input("Emergency Phone", key="em_phone")

        st.subheader("Medical Info")
        medical = st.text_area("Allergies / Injuries / Conditions", key="medical")

        st.subheader("Media Consent")
        st.markdown('<label class="required-label">Media Consent</label>', unsafe_allow_html=True)
        consent = st.radio("Allow photo/video for promotions?", ["Yes", "No"], key="consent")

        st.subheader("Parent Consent")
        st.markdown('<label class="required-label">Parent/Guardian Signature</label>', unsafe_allow_html=True)
        signature = st.text_input("Parent/Guardian Signature", key="signature")

        st.markdown('<label class="required-label">Date</label>', unsafe_allow_html=True)
        sig_date = st.date_input("Date", value=date.today(), key="sig_date")

        submitted = st.form_submit_button("Submit Registration")

    if submitted:
        missing = []

        # Required fields
        if not student_name.strip():
            missing.append("Student Name")
            error_fields.add("student_name")
        if not dob.strip():
            missing.append("Date of Birth / Age")
            error_fields.add("dob")
        if not gender.strip():
            missing.append("Gender")
            error_fields.add("gender")
        if not enrollment.strip():
            missing.append("Enrollment Type")
            error_fields.add("enroll")
        if not mode:
            missing.append("Mode")
            error_fields.add("mode")
        if not level.strip():
            missing.append("Level")
            error_fields.add("level")
        if not pref_time.strip():
            missing.append("Preferred Days/Time")
            error_fields.add("pref_time")
        if not consent:
            missing.append("Media Consent")
            error_fields.add("consent")
        if not signature.strip():
            missing.append("Parent/Guardian Signature")
            error_fields.add("signature")
        if not sig_date:
            missing.append("Date")
            error_fields.add("sig_date")

        if missing:
            st.error("Please fill the required fields: " + ", ".join(missing))

            # Shake animation
            st.markdown(
                """
                <script>
                const sections = window.parent.document.querySelectorAll('.section');
                if (sections.length > 0) {
                    const last = sections[sections.length - 1];
                    last.class
