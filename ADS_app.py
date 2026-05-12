# ADS_app.py — A06.1
# Gradient background, centered logo, no dark mode, WhatsApp top-right,
# About page, slideshow, enhanced validation

import streamlit as st
import pandas as pd
import os
import json
import glob
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

params = st.query_params
if "page" in params:
    st.session_state.page = params["page"]

page = st.session_state.page

# ---------------------------------------------------------
# THEME COLORS (light only)
# ---------------------------------------------------------
PRIMARY = "#b8860b"
PRIMARY_HOVER = "#a0750a"
ACCENT = "#111827"
MUTED = "#f7f7fa"
CARD = "#ffffff"
BORDER = "#e6e6e8"
TEXT = "#111827"

# ---------------------------------------------------------
# CSS — gradient, iOS buttons, validation, WhatsApp top-right
# ---------------------------------------------------------
CSS = f"""
<style>

:root {{
    color-scheme: light;
}}

html, body, [data-testid="stAppViewContainer"] {{
    background: linear-gradient(
        135deg,
        #fff7c2 0%,
        #ffe27a 25%,
        #f5f5f5 100%
    ) !important;
    background-attachment: fixed !important;
    color: {TEXT} !important;
    transition: background 0.4s ease;
}}

[data-testid="stSidebar"] {{
    background-color: {CARD} !important;
}}

* {{
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui;
}}

.block-container {{
  padding-top: 0.5rem;
  max-width: 900px;
  animation: fadeIn 0.4s ease;
}}

@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(6px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

.section {{
  background:{CARD};
  padding:14px;
  border-radius:12px;
  border:1px solid {BORDER};
  margin-bottom:12px;
}}

.title {{
  font-size:1.25rem;
  font-weight:700;
  color:{TEXT};
}}
.subtitle {{
  font-size:0.9rem;
  color:#6b7280;
  margin-bottom:10px;
}}

.class-card {{
  padding:10px;
  border-radius:10px;
  background:rgba(15,23,42,0.03);
  border:1px solid {BORDER};
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
    box-shadow: 0 0 0 1px rgba(225,29,72,0.12);
}}

@keyframes shake {{
  10%, 90% {{ transform: translateX(-1px); }}
  20%, 80% {{ transform: translateX(2px); }}
  30%, 50%, 70% {{ transform: translateX(-4px); }}
  40%, 60% {{ transform: translateX(4px); }}
}}

.shake {{
  animation: shake 0.35s ease-in-out;
}}

.footer {{
  text-align:center;
  color:#9ca3af;
  font-size:0.8rem;
  margin-top:40px;
  margin-bottom:60px;
}}

.bottom-nav {{
  position:fixed;
  bottom:0;
  left:0;
  right:0;
  background:{CARD};
  border-top:1px solid {BORDER};
  display:flex;
  justify-content:space-around;
  padding:8px 0;
  z-index:999;
}}
.bottom-nav a {{
  text-decoration:none;
  font-size:0.8rem;
  color:{TEXT};
  text-align:center;
}}
.bottom-nav a span {{
  display:block;
  font-size:1.1rem;
}}
.bottom-nav a.active {{
  color:{PRIMARY};
}}

.whatsapp-btn {{
  position:fixed;
  top:20px;
  right:20px;
  background:#25D366;
  color:white;
  padding:14px 16px;
  border-radius:50%;
  font-size:22px;
  text-decoration:none;
  box-shadow:0 4px 12px rgba(0,0,0,0.2);
  z-index:9999;
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
# HEADER — centered logo
# ---------------------------------------------------------
def render_header():
    if os.path.exists(LOGO_PATH):
        logo_html = f'<img src="{LOGO_PATH}" width="110" style="border-radius:16px;" />'
    else:
        logo_html = ""

    st.markdown(
        f"""
        <div style="text-align:center; padding:20px 0 10px 0;">
            {logo_html}
            <div style="font-size:1.4rem; font-weight:700; margin-top:8px; color:{TEXT};">
                AARA Dance Studio
            </div>
            <div style="font-size:0.9rem; color:#6b7280;">
                Fate · Rockwall · Dallas, TX
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
# PAGES
# ---------------------------------------------------------
if page == "Home":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Welcome to AARA Dance Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Where passion meets performance.</div>', unsafe_allow_html=True)
    st.write("Dance Instructor: **Mrs. Rekha Mahendran & Mahendran Ramachandran**")
    st.write("📍 **315 Spirehaven Dr, Rockwall, TX 75087**")

    st.markdown("### Studio Moments")
    images = sorted(glob.glob("slide*.jpg"))
    if images:
        st.image(images, width=600)
    else:
        st.info("Upload slide1.jpg, slide2.jpg, slide3.jpg in the root directory for slideshow.")

    st.markdown('<a class="btn-secondary" href="/?page=Classes">View Classes</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    render_qr_section()

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

elif page == "About":
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align:center; font-size:1.6rem; font-weight:700; margin-bottom:10px;">
            Find your Groove!
        </div>
        """,
        unsafe_allow_html=True,
    )

    if os.path.exists("instructor.jpg"):
        st.image("instructor.jpg", width=260)
    else:
        st.info("Instructor photo placeholder (upload instructor.jpg in root directory).")

    st.markdown(
        """
        <ul style="font-size:1rem; line-height:1.6;">
            <li><b>Bollywood</b> – A fun and energetic dance style inspired by Hindi movie songs and Indian cinema.</li>
            <li><b>Kollywood</b> – A vibrant dance form based on Tamil movie music, known for expressive moves and powerful energy.</li>
            <li><b>Tollywood</b> – A lively dance style inspired by Telugu film songs, featuring fast beats and dynamic choreography.</li>
            <li><b>Semi-Classical</b> – A graceful blend of classical Indian dance techniques with modern expressions and music.</li>
            <li><b>Freestyle</b> – A creative dance form that allows dancers to move freely and express themselves without fixed rules.</li>
            <li><b>Hip Hop</b> – A trendy and energetic street dance style with sharp movements, rhythm, and attitude.</li>
            <li><b>Kuthu</b> – A high-energy South Indian folk-inspired dance style known for its fun beats and energetic moves.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Register":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Student Registration</div>', unsafe_allow_html=True)

    required_placeholders = {
        "student_name": "__req_student_name",
        "dob": "__req_dob",
        "pref_time": "__req_pref_time",
        "signature": "__req_signature"
    }

    with st.form("reg_form", clear_on_submit=False):
        st.subheader("Student Info")

        student_name = st.text_input("Student Name", key="student_name",
                                     placeholder=required_placeholders["student_name"])

        dob = st.text_input("Date of Birth (Age)", key="dob",
                            placeholder=required_placeholders["dob"])

        gender = st.selectbox("Gender", ["", "Female", "Male", "Other", "Prefer not to say"], key="gender")

        school = st.text_input("School Name (optional)", key="school")

        st.subheader("Parent / Guardian")
        parent = st.text_input("Parent/Guardian Name", key="parent")
        phone = st.text_input("Phone Number", key="phone")
        email = st.text_input("Email Address", key="email")
        address = st.text_area("Address", key="address")

        st.subheader("Class Details")
        enrollment = st.selectbox(
            "Enrollment Type",
            ["", "Regular ($50/month)", "Drop-in ($15/session)"],
            key="enroll"
        )

        mode = st.radio("Mode", ["In-Person", "Online"], key="mode")

        workshops = st.multiselect(
            "Workshops",
            ["Ladies Kuthu Workshop", "Couple Dance Fitness Workshop"],
            key="workshops"
        )

        level = st.selectbox("Level", ["", "Beginner", "Intermediate", "Advanced"], key="level")

        pref_time = st.text_input("Preferred Days/Time", key="pref_time",
                                  placeholder=required_placeholders["pref_time"])

        experience = st.text_area("Previous Experience", key="experience")

        st.subheader("Emergency Contact")
        em_name = st.text_input("Emergency Contact Name", key="em_name")
        em_rel = st.text_input("Relationship", key="em_rel")
        em_phone = st.text_input("Emergency Phone", key="em_phone")

        st.subheader("Medical Info")
        medical = st.text_area("Allergies / Injuries / Conditions", key="medical")

        st.subheader("Media Consent")
        consent = st.radio("Allow photo/video for promotions?", ["", "Yes", "No"], key="consent")

        st.subheader("Parent Consent")
        signature = st.text_input("Parent/Guardian Signature", key="signature",
                                  placeholder=required_placeholders["signature"])

        sig_date = st.date_input("Date", value=date.today(), key="sig_date")

        submitted = st.form_submit_button("Submit Registration")

    if submitted:
        missing = []
        missing_placeholders = []

        if not student_name or not student_name.strip():
            missing.append("Student Name")
            missing_placeholders.append(required_placeholders["student_name"])
        if not dob or not dob.strip():
            missing.append("Date of Birth / Age")
            missing_placeholders.append(required_placeholders["dob"])
        if not gender or not gender.strip():
            missing.append("Gender")
        if not enrollment or not enrollment.strip():
            missing.append("Enrollment Type")
        if not mode:
            missing.append("Mode")
        if not level or not level.strip():
            missing.append("Level")
        if not pref_time or not pref_time.strip():
            missing.append("Preferred Days/Time")
            missing_placeholders.append(required_placeholders["pref_time"])
        if not consent or not consent.strip():
            missing.append("Media Consent")
        if not signature or not signature.strip():
            missing.append("Parent/Guardian Signature")
            missing_placeholders.append(required_placeholders["signature"])
        if not sig_date:
            missing.append("Date")

        if missing:
            st.error("Please fill the required fields: " + ", ".join(missing))

            js = f"""
            <script>
            (function() {{
                try {{
                    const missing = {json.dumps(missing_placeholders)};
                    missing.forEach(p => {{
                        const el = document.querySelector('[placeholder="'+p+'"]');
                        if (el) {{
                            el.style.borderColor = '#e11d48';
                            el.style.boxShadow = '0 0 0 1px rgba(225,29,72,0.12)';
                        }}
                    }});
                    const sections = window.parent.document.querySelectorAll('.section');
                    if (sections.length > 0) {{
                        const last = sections[sections.length - 1];
                        last.classList.add('shake');
                        setTimeout(() => last.classList.remove('shake'), 400);
                    }}
                }} catch(e) {{
                    console.log('validation script error', e);
                }}
            }})();
            </script>
            """
            st.markdown(js, unsafe_allow_html=True)
        else:
            record = {
                "timestamp": datetime.now().isoformat(),
                "student_name": student_name,
                "dob": dob,
                "gender": gender,
                "school": school,
                "parent": parent,
                "phone": phone,
                "email": email,
                "address": address,
                "enrollment": enrollment,
                "mode": mode,
                "workshops": "; ".join(workshops),
                "level": level,
                "style": "",
                "pref_time": pref_time,
                "experience": experience,
                "em_name": em_name,
                "em_rel": em_rel,
                "em_phone": em_phone,
                "medical": medical,
                "consent": consent,
                "signature": signature,
                "sig_date": sig_date.isoformat()
            }
            save_registration(record)
            st.success("Registration submitted successfully!")

elif page == "Admin":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Admin Dashboard</div>', unsafe_allow_html=True)

    ADMIN_PASS = os.environ.get("ADMIN_PASS", "aara-admin-2026")

    if not st.session_state.admin_authenticated:
        pwd = st.text_input("Enter admin password", type="password")
        if st.button("Login"):
            if pwd == ADMIN_PASS:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    else:
        st.success("Admin authenticated.")

        regs = read_csv(REG_FILE)
        visits = read_csv(VISIT_FILE)

        st.subheader("Overview")
        st.write(f"Total registrations: **{len(regs)}**")
        st.write(f"Total site visits: **{len(visits)}**")

        st.subheader("Registrations")
        if regs.empty:
            st.info("No registrations yet.")
        else:
            st.dataframe(regs)
            st.download_button("Download Registrations CSV", regs.to_csv(index=False), "registrations.csv")

        st.subheader("Site Visits")
        if visits.empty:
            st.info("No visits yet.")
        else:
            st.dataframe(visits)
            st.download_button("Download Visits CSV", visits.to_csv(index=False), "site_visits.csv")

        st.markdown("---")
        if st.button("Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# WHATSAPP BUTTON (top-right)
# ---------------------------------------------------------
st.markdown(
    """
    <a class="whatsapp-btn" href="https://wa.me/14692222222" target="_blank">💬</a>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# BOTTOM NAV
# ---------------------------------------------------------
home = "active" if page == "Home" else ""
classes = "active" if page == "Classes" else ""
reg = "active" if page == "Register" else ""
about = "active" if page == "About" else ""
admin = "active" if page == "Admin" else ""

st.markdown(
    f"""
    <div class="bottom-nav">
      <a class="{home}" href="/?page=Home"><span>🏠</span>Home</a>
      <a class="{classes}" href="/?page=Classes"><span>📚</span>Classes</a>
      <a class="{reg}" href="/?page=Register"><span>📝</span>Register</a>
      <a class="{about}" href="/?page=About"><span>ℹ️</span>About</a>
      <a class="{admin}" href="/?page=Admin"><span>🔐</span>Admin</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    '<div class="footer">© AARA Dance Studio · Fate · Rockwall · Dallas, TX</div>',
    unsafe_allow_html=True,
)
