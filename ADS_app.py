# ADS_app.py — A03 Version (Logo Fixed, Admin Improved, Streamlit 1.32+ Compatible)

import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from PIL import Image

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
# THEME COLORS
# ---------------------------------------------------------
PRIMARY = "#b8860b"      # gold
ACCENT = "#111827"       # charcoal
MUTED = "#f7f7fa"        # soft background
CARD = "#ffffff"
BORDER = "#e6e6e8"

# ---------------------------------------------------------
# FILE PATHS
# ---------------------------------------------------------
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

REG_FILE = os.path.join(DATA_DIR, "registrations.csv")
VISIT_FILE = os.path.join(DATA_DIR, "site_visits.csv")

LOGO_PATH = "logo.png"   # must be in same folder as ADS_app.py

# ---------------------------------------------------------
# CSS (iOS Minimalist)
# ---------------------------------------------------------
CSS = f"""
<style>
* {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui; }}
html, body {{ background: {MUTED}; }}
.block-container {{ padding-top: 1rem; max-width: 900px; }}

.header {{
  display:flex; align-items:center; gap:14px;
  padding:10px 14px; background:white;
  border-radius:14px; border:1px solid {BORDER};
  box-shadow:0 6px 18px rgba(17,24,39,0.04);
  margin-bottom:14px;
}}

.logo-wrap {{
  width:72px; height:72px; display:flex;
  align-items:center; justify-content:center;
  overflow:hidden; border-radius:14px;
}}

.brand-title {{
  font-weight:700; color:{ACCENT}; font-size:1.1rem;
}}
.brand-sub {{
  font-size:0.8rem; color:#6b7280;
}}

.nav {{
  margin-left:auto; display:flex; gap:8px;
}}
.nav a {{
  padding:8px 12px; border-radius:999px;
  text-decoration:none; color:{ACCENT};
  font-size:0.9rem;
}}
.nav a.active {{
  background:{PRIMARY}; color:white;
}}

.section {{
  background:{CARD}; padding:14px;
  border-radius:12px; border:1px solid {BORDER};
  margin-bottom:12px;
}}

.title {{
  font-size:1.25rem; font-weight:700; color:{ACCENT};
}}
.subtitle {{
  font-size:0.9rem; color:#6b7280; margin-bottom:10px;
}}

.class-card {{
  padding:10px; border-radius:10px;
  background:#fbfbfb; border:1px solid {BORDER};
  margin-bottom:8px;
}}

.btn {{
  padding:8px 14px; border-radius:999px;
  background:{ACCENT}; color:white;
  text-decoration:none; font-weight:600;
}}

.footer {{
  text-align:center; color:#9ca3af;
  font-size:0.8rem; margin-top:20px;
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
# NAVIGATION STATE
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
# HEADER
# ---------------------------------------------------------
def render_header():
    cols = st.columns([0.15, 0.65, 0.2])

    # Logo
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

    # Brand
    with cols[1]:
        st.markdown(
            f"""
            <div class="brand-title">AARA Dance Studio</div>
            <div class="brand-sub">Fate · Rockwall · Dallas, TX</div>
            """,
            unsafe_allow_html=True,
        )

    # Navigation
    with cols[2]:
        home = "active" if page == "Home" else ""
        classes = "active" if page == "Classes" else ""
        reg = "active" if page == "Register" else ""
        admin = "active" if page == "Admin" else ""

        st.markdown(
            f"""
            <div class="nav">
              <a class="{home}" href="/?page=Home">Home</a>
              <a class="{classes}" href="/?page=Classes">Classes</a>
              <a class="{reg}" href="/?page=Register">Register</a>
              <a class="{admin}" href="/?page=Admin">Admin</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

render_header()

# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------
if page == "Home":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Welcome to AARA Dance Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Where passion meets performance.</div>', unsafe_allow_html=True)
    st.write("Choreography by **Mrs. Rekha Mahendran & Mahendran Ramachandran**")
    st.write("📍 **315 Spirehaven Dr, Rockwall, TX 75087**")
    st.markdown('<a class="btn" href="/?page=Classes">View Classes</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# CLASSES PAGE
# ---------------------------------------------------------
elif page == "Classes":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Programs & Fees</div>', unsafe_allow_html=True)

    st.markdown('<div class="class-card"><b>Tiny Stars (Ages 5–8)</b><br>Wed & Fri · 6:30–7:30 PM<br>4 classes: $60 · 8 classes: $100</div>', unsafe_allow_html=True)
    st.markdown('<div class="class-card"><b>Shining Stars (Ages 9+)</b><br>Tue · 7–8 PM<br>4 classes: $60 · 8 classes: $100</div>', unsafe_allow_html=True)
    st.markdown('<div class="class-card"><b>Dream Chasers (Ladies 18+)</b><br>Thu 6:30–7:30 PM · Sat 10:30–11:30 AM<br>4 classes: $50 · 8 classes: $80</div>', unsafe_allow_html=True)

    st.markdown('<a class="btn" href="/?page=Register">Register Now</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# REGISTRATION PAGE
# ---------------------------------------------------------
elif page == "Register":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Student Registration</div>', unsafe_allow_html=True)

    with st.form("reg_form", clear_on_submit=True):
        st.subheader("Student Info")
        student_name = st.text_input("Student Name")
        dob = st.text_input("Date of Birth (Age)")
        gender = st.selectbox("Gender", ["Female", "Male", "Other", "Prefer not to say"])
        school = st.text_input("School Name (optional)")

        st.subheader("Parent / Guardian")
        parent = st.text_input("Parent/Guardian Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        address = st.text_area("Address")

        st.subheader("Class Details")
        enrollment = st.selectbox("Enrollment Type", ["Regular ($50/month)", "Drop-in ($15/session)"])
        mode = st.radio("Mode", ["In-Person", "Online"])
        workshops = st.multiselect("Workshops", ["Ladies Kuthu Workshop", "Couple Dance Fitness Workshop"])
        level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
        style = st.text_input("Dance Style")
        pref_time = st.text_input("Preferred Days/Time")
        experience = st.text_area("Previous Experience")

        st.subheader("Emergency Contact")
        em_name = st.text_input("Emergency Contact Name")
        em_rel = st.text_input("Relationship")
        em_phone = st.text_input("Emergency Phone")

        st.subheader("Medical Info")
        medical = st.text_area("Allergies / Injuries / Conditions")

        st.subheader("Media Consent")
        consent = st.radio("Allow photo/video for promotions?", ["Yes", "No"])

        st.subheader("Parent Consent")
        signature = st.text_input("Parent/Guardian Signature")
        sig_date = st.date_input("Date", value=date.today())

        submitted = st.form_submit_button("Submit Registration")

    if submitted:
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
            "style": style,
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

# ---------------------------------------------------------
# ADMIN PAGE (PASSWORD PROTECTED)
# ---------------------------------------------------------
elif page == "Admin":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Admin Dashboard</div>', unsafe_allow_html=True)

    ADMIN_PASS = os.environ.get("ADMIN_PASS", "aara-admin-2026")

    if not st.session_state.admin_authenticated:
        pwd = st.text_input("Enter admin password", type="password")
        if st.button("Login"):
            if pwd == ADMIN_PASS:
                st.session_state.admin_authenticated = True
                st.experimental_rerun()
            else:
                st.error("Incorrect password.")
    else:
        st.success("Admin authenticated.")

        st.subheader("Registrations")
        regs = read_csv(REG_FILE)
        if regs.empty:
            st.info("No registrations yet.")
        else:
            st.dataframe(regs)
            st.download_button("Download Registrations CSV", regs.to_csv(index=False), "registrations.csv")

        st.subheader("Site Visits")
        visits = read_csv(VISIT_FILE)
        st.write(f"Total visits: **{len(visits)}**")
        st.dataframe(visits)
        st.download_button("Download Visits CSV", visits.to_csv(index=False), "site_visits.csv")

        st.markdown("---")
        if st.button("Logout"):
            st.session_state.admin_authenticated = False
            st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown('<div class="footer">© AARA Dance Studio · Fate · Rockwall · Dallas, TX</div>', unsafe_allow_html=True)
