# ADS_app.py — B02 (Full)
# Baseline: B00 theme + B01 fixes + B02 improvements
# - Cinematic zoom-in slideshow
# - Fully themed form fields (dropdowns, radios, selects)
# - Larger centered circular logo (200px)
# - 60px top padding to avoid Streamlit banner overlap
# - Fixed safe query param handling and QR code generation
# - All pages accessible via query param routing

import streamlit as st
import pandas as pd
import os
import glob
import io
import json
from datetime import datetime, date
from PIL import Image

try:
    import qrcode
except Exception:
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
# SESSION STATE & ROUTING (safe)
# ---------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

# Use experimental_get_query_params for compatibility
params = st.experimental_get_query_params()
if "page" in params and params["page"]:
    st.session_state.page = params["page"][0]

page = st.session_state.page

# ---------------------------------------------------------
# THEME COLORS (B00 baseline)
# ---------------------------------------------------------
BG_TOP = "#0a0a0a"
BG_BOTTOM = "#1a1a1a"
GOLD = "#d4af37"
GOLD_SOFT = "#f5e8c7"
RED = "#8b0000"
TEXT = "#f5e8c7"
CARD_BG = "#111111"
BORDER = "#3a3a3a"

# ---------------------------------------------------------
# CSS — B02 (top padding, form fixes, slideshow zoom, logo spacing)
# ---------------------------------------------------------
CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&display=swap');

:root {{
    color-scheme: dark;
}}

html, body, [data-testid="stAppViewContainer"] {{
    background: linear-gradient(180deg, {BG_TOP} 0%, {BG_BOTTOM} 100%) !important;
    color: {TEXT} !important;
}}

.block-container {{
  padding-top: 60px !important; /* Prevent Streamlit banner overlap */
  max-width: 920px;
  animation: fadeIn 0.4s ease;
}}

@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(6px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

.section {{
  background:{CARD_BG};
  padding:18px;
  border-radius:14px;
  border:1px solid {BORDER};
  margin-bottom:14px;
  box-shadow:0 0 18px rgba(0,0,0,0.6);
}}

.title {{
  font-size:1.6rem;
  font-weight:700;
  color:{GOLD};
  font-family:'Playfair Display', serif;
}}

.subtitle {{
  font-size:1rem;
  color:{GOLD_SOFT};
  margin-bottom:10px;
}}

.btn-primary {{
  display:inline-block;
  padding:12px 22px;
  background:{GOLD};
  color:{BG_TOP} !important;
  border-radius:999px;
  text-decoration:none;
  font-weight:600;
  border:none;
  transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}}
.btn-primary:hover {{
  background:{GOLD_SOFT};
  transform:translateY(-1px);
  box-shadow:0 8px 20px rgba(0,0,0,0.6);
}}

.btn-secondary {{
  display:inline-block;
  padding:12px 22px;
  background:transparent;
  color:{GOLD_SOFT} !important;
  border-radius:999px;
  border:1px solid {GOLD};
  text-decoration:none;
  font-weight:500;
  transition: background 0.2s ease, color 0.2s ease, transform 0.2s ease;
}}
.btn-secondary:hover {{
  background:{GOLD};
  color:{BG_TOP} !important;
  transform:translateY(-1px);
}}

.class-card {{
  padding:12px;
  border-radius:12px;
  background:#151515;
  border:1px solid {GOLD};
  margin-bottom:10px;
  box-shadow:0 6px 18px rgba(0,0,0,0.7);
}}

.required-label::after {{
    content: " *";
    color: #e11d48;
    font-weight: 700;
}}

.footer {{
  text-align:center;
  color:{GOLD};
  font-size:0.8rem;
  margin-top:40px;
  margin-bottom:60px;
}}

.bottom-nav {{
  position:fixed;
  bottom:0;
  left:0;
  right:0;
  background:#050505;
  border-top:1px solid {BORDER};
  display:flex;
  justify-content:space-around;
  padding:10px 0;
  z-index:999;
}}

.bottom-nav a {{
  text-decoration:none;
  font-size:0.85rem;
  color:{GOLD_SOFT};
  text-align:center;
}}

.bottom-nav a span {{
  display:block;
  font-size:1.2rem;
}}

.bottom-nav a.active {{
  color:{GOLD};
}}

.whatsapp-btn {{
  position:fixed;
  top:80px; /* moved down to avoid banner */
  right:20px;
  background:#25D366;
  color:white;
  padding:14px 16px;
  border-radius:50%;
  font-size:22px;
  text-decoration:none;
  box-shadow:0 4px 12px rgba(0,0,0,0.8);
  z-index:9999;
}}

/* Registration vertical cards */
.reg-card {{
  border-radius:14px;
  border:1px solid {GOLD};
  background:#151515;
  padding:14px 16px;
  margin-bottom:12px;
  box-shadow:0 6px 18px rgba(0,0,0,0.8);
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
  cursor:pointer;
}}
.reg-card:hover {{
  transform: translateY(-6px);
  box-shadow:0 14px 32px rgba(0,0,0,0.9);
  border-color:{GOLD_SOFT};
}}

.reg-card-header {{
  display:flex;
  justify-content:space-between;
  align-items:center;
  font-weight:600;
  font-size:1rem;
  color:{GOLD_SOFT};
}}

.reg-card-sub {{
  font-size:0.9rem;
  color:#d1c7a5;
  margin-top:4px;
}}

/* FORM FIELD FIXES (B02) */
label {{
  color:{GOLD_SOFT} !important;
}}

input, textarea, select {{
  background:#151515 !important;
  color:{GOLD_SOFT} !important;
  border:1px solid {GOLD} !important;
  border-radius:8px !important;
}}

.stTextInput input,
.stTextArea textarea,
.stSelectbox select,
.stDateInput input {{
  background:#151515 !important;
  color:{GOLD_SOFT} !important;
  border:1px solid {GOLD} !important;
}}

.stRadio label {{
  color:{GOLD_SOFT} !important;
}}

.stRadio div[role="radio"] {{
  border:2px solid {GOLD} !important;
}}

.stMultiSelect div {{
  background:#151515 !important;
  color:{GOLD_SOFT} !important;
  border:1px solid {GOLD} !important;
}}

.stSelectbox div[data-baseweb="select"] {{
  background:#151515 !important;
  color:{GOLD_SOFT} !important;
  border:1px solid {GOLD} !important;
}}

.stSelectbox svg {{
  fill:{GOLD} !important;
}}

/* CINEMATIC ZOOM-IN SLIDESHOW */
.slideshow-container {{
  position: relative;
  width: 100%;
  max-width: 860px;
  height: 360px;
  margin: 0 auto;
  overflow: hidden;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.9);
  border: 1px solid {GOLD};
}}

.slide-zoom {{
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  animation: zoomFade 24s infinite;
}}

@keyframes zoomFade {{
  0% {{ opacity: 0; transform: scale(1); }}
  5% {{ opacity: 1; transform: scale(1.03); }}
  20% {{ opacity: 1; transform: scale(1.08); }}
  25% {{ opacity: 0; transform: scale(1.08); }}
  100% {{ opacity: 0; transform: scale(1); }}
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
# HEADER — Larger centered circular logo (200px)
# ---------------------------------------------------------
def render_header():
    # Use columns to center reliably
    left, center, right = st.columns([1, 2, 1])
    with center:
        if os.path.exists(LOGO_PATH):
            try:
                st.image(LOGO_PATH, width=200)
            except Exception:
                # fallback: show text if image fails
                st.markdown(f'<div style="text-align:center; color:{GOLD}; font-weight:700; font-size:1.6rem;">AARA Dance Studio</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align:center; color:{GOLD}; font-weight:700; font-size:1.6rem;">AARA Dance Studio</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="text-align:center; margin-top:6px;">
                <div style="font-size:1.05rem; color:{GOLD_SOFT};">
                    Where Passion Meets Performance · Fate · Rockwall · Dallas, TX
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

render_header()

# ---------------------------------------------------------
# WHATSAPP BUTTON (moved down to avoid banner)
# ---------------------------------------------------------
st.markdown(
    """
    <a class="whatsapp-btn" href="https://wa.me/14692222222" target="_blank">💬</a>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# QR CODE SECTION (safe)
# ---------------------------------------------------------
def render_qr_section():
    if qrcode is None:
        return
    st.markdown("#### Quick Registration QR")
    # If you have a deployed URL, replace the placeholder below with it.
    reg_url = "https://your-app-url/?page=Register"
    try:
        qr_img = qrcode.make(reg_url)
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        buf.seek(0)
        st.image(buf, caption="Scan to open registration page", width=140)
    except Exception:
        st.info("QR generation not available in this environment.")

# ---------------------------------------------------------
# HOME PAGE — Cinematic zoom-in slideshow
# ---------------------------------------------------------
def render_home():
    st.markdown(
        f"""
        <div style="
            background:{RED};
            color:{GOLD_SOFT};
            text-align:center;
            padding:10px;
            border-radius:10px;
            margin-bottom:14px;
            box-shadow:0 8px 20px rgba(0,0,0,0.8);
            font-weight:600;
        ">
          ★ EARLY BIRD OFFER ★ — First 10 Registrations Only $50/month for 3 Months!<br>
          <span style="font-size:0.9rem; font-weight:400;">Limited spots · Register now to lock in your rate</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="section">
            <div style="font-size:2.2rem; font-weight:800; color:{GOLD}; font-family:'Playfair Display', serif;">
                Dance. Express. Shine.
            </div>
            <div style="font-size:1.02rem; color:{GOLD_SOFT}; max-width:640px; margin-top:8px;">
                AARA Dance Studio brings Bollywood, Kollywood, Tollywood, Kuthu, Hip Hop and more
                to Fate · Rockwall · Dallas. A fun, safe space for kids, teens, and adults to find their groove.
            </div>
            <div style="margin-top:12px; font-size:0.95rem; color:{GOLD_SOFT};">
                Dance Instructor: <b>Mrs. Rekha Mahendran &amp; Mahendran Ramachandran</b><br>
                📍 315 Spirehaven Dr, Rockwall, TX 75087
            </div>
            <div style="margin-top:14px;">
                <a class="btn-primary" href="/?page=Register">Register Now</a>
                &nbsp;&nbsp;
                <a class="btn-secondary" href="/?page=Classes">View Classes</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown(f'<div class="title" style="font-size:1.4rem;">Studio Moments</div>', unsafe_allow_html=True)

    # Collect slide images (jpg/jpeg/png)
    images = sorted(glob.glob("slide*.jpg")) + sorted(glob.glob("slide*.jpeg")) + sorted(glob.glob("slide*.png"))
    images = images[:5]  # limit to 5 slides

    if images:
        slides_html = []
        for idx, path in enumerate(images):
            delay = idx * 6  # 6s per slide in 24s cycle
            # Use basename so relative path works when served
            slides_html.append(
                f'<img src="{os.path.basename(path)}" class="slide-zoom" style="animation-delay:{delay}s;" />'
            )
        slides_html = "\n".join(slides_html)
        st.markdown(
            f"""
            <div class="slideshow-container">
                {slides_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Upload slide1.jpeg, slide2.jpeg, slide3.jpeg (etc.) in the app root for a cinematic slideshow.")

    st.markdown('</div>', unsafe_allow_html=True)
    render_qr_section()

# ---------------------------------------------------------
# CLASSES PAGE
# ---------------------------------------------------------
def render_classes():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Programs & Fees</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Choose the program that fits your dancer best.</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="class-card">
            <div style="color:{GOLD}; font-weight:700;">Tiny Stars (Ages 5–8)</div>
            <div style="color:{GOLD_SOFT};">Beginner / Intermediate · Wed &amp; Fri · 6:30–7:30 PM</div>
            <div style="margin-top:6px; color:{GOLD_SOFT};">4 classes: $60 · 8 classes: $100</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="class-card">
            <div style="color:{GOLD}; font-weight:700;">Shining Stars (Ages 9+)</div>
            <div style="color:{GOLD_SOFT};">Beginner / Intermediate · Tue · 7–8 PM</div>
            <div style="margin-top:6px; color:{GOLD_SOFT};">4 classes: $60 · 8 classes: $100</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="class-card">
            <div style="color:{GOLD}; font-weight:700;">Dream Chasers (Ladies 18+)</div>
            <div style="color:{GOLD_SOFT};">Beginner / Intermediate · Thu 6:30–7:30 PM · Sat 10:30–11:30 AM</div>
            <div style="margin-top:6px; color:{GOLD_SOFT};">4 classes: $50 · 8 classes: $80</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div style="margin-top:8px;"><a class="btn-primary" href="/?page=Register">Register Now</a></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# ABOUT PAGE
# ---------------------------------------------------------
def render_about():
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align:center; font-size:1.9rem; font-weight:800; margin-bottom:10px; color:{GOLD}; font-family:'Playfair Display', serif;">
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
        f"""
        <ul style="font-size:1rem; line-height:1.6; margin-top:10px; color:{GOLD_SOFT};">
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

# ---------------------------------------------------------
# ADMIN PAGE
# ---------------------------------------------------------
def render_admin():
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
            st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# REGISTRATION PAGE — Vertical cards, single "Submit Form" button
# (All form controls themed to match B00)
# ---------------------------------------------------------
def render_register():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Student Registration</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Fill in the details below to secure your spot.</div>', unsafe_allow_html=True)

    required_placeholders = {
        "student_name": "__req_student_name",
        "dob": "__req_dob",
        "pref_time": "__req_pref_time",
        "signature": "__req_signature"
    }

    with st.form("reg_form", clear_on_submit=False):
        # Card 1 — Student Info
        st.markdown(
            """
            <div class="reg-card">
              <div class="reg-card-header">
                <span>Student Information</span>
                <span>👧🧒</span>
              </div>
              <div class="reg-card-sub">
                Basic details about the student.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        student_name = st.text_input("Student Name", key="student_name",
                                     placeholder=required_placeholders["student_name"])
        dob = st.text_input("Date of Birth (Age)", key="dob",
                            placeholder=required_placeholders["dob"])
        gender = st.selectbox("Gender", ["", "Female", "Male", "Other", "Prefer not to say"], key="gender")
        school = st.text_input("School Name (optional)", key="school")

        # Card 2 — Class Details
        st.markdown(
            """
            <div class="reg-card">
              <div class="reg-card-header">
                <span>Class Details</span>
                <span>💃</span>
              </div>
              <div class="reg-card-sub">
                Choose how and when you’d like to dance.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
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

        # Card 3 — Parent & Emergency Contact
        st.markdown(
            """
            <div class="reg-card">
              <div class="reg-card-header">
                <span>Parent & Emergency Contact</span>
                <span>📞</span>
              </div>
              <div class="reg-card-sub">
                Who should we reach out to if needed?
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        parent = st.text_input("Parent/Guardian Name", key="parent")
        phone = st.text_input("Phone Number", key="phone")
        email = st.text_input("Email Address", key="email")
        address = st.text_area("Address", key="address")
        em_name = st.text_input("Emergency Contact Name", key="em_name")
        em_rel = st.text_input("Relationship", key="em_rel")
        em_phone = st.text_input("Emergency Phone", key="em_phone")

        # Card 4 — Medical & Consent
        st.markdown(
            """
            <div class="reg-card">
              <div class="reg-card-header">
                <span>Medical & Consent</span>
                <span>✅</span>
              </div>
              <div class="reg-card-sub">
                Safety information and media consent.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        medical = st.text_area("Allergies / Injuries / Conditions", key="medical")
        consent = st.radio("Allow photo/video for promotions?", ["", "Yes", "No"], key="consent")
        signature = st.text_input("Parent/Guardian Signature", key="signature",
                                  placeholder=required_placeholders["signature"])
        sig_date = st.date_input("Date", value=date.today(), key="sig_date")

        # SINGLE submit button with new label
        submitted = st.form_submit_button("Submit Form")

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
                            el.style.boxShadow = '0 0 0 1px rgba(225,29,72,0.4)';
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

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE ROUTER
# ---------------------------------------------------------
if page == "Home":
    render_home()
elif page == "Classes":
    render_classes()
elif page == "About":
    render_about()
elif page == "Register":
    render_register()
elif page == "Admin":
    render_admin()
else:
    # fallback to home if unknown
    render_home()

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
    f'<div class="footer">© AARA Dance Studio · ADS · Dallas · Fate, TX</div>',
    unsafe_allow_html=True,
)
