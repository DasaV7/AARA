# ADS_app.py — B01 (Registration form fields fixed)
# Baseline: A06.3 / B00 theme + B01 fixes
# Change in this file:
# - Only registration form styling adjusted so all form controls match the dark black–gold theme
# - Overrides for dropdowns, multiselects, radios, date inputs, placeholders, and select arrows
# - No other structural changes from B01

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
# THEME COLORS (flyer style baseline B00)
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
# CSS — Flyer theme + animations + form field styling + slideshow
# (Registration form fixes applied here)
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

* {{
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui;
}}

.block-container {{
    padding-top: 40px !important;   /* prevents banner clipping */
    max-width: 900px !important;
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
  transition: background 0.2s ease;
}}
.btn-primary:hover {{
  background:{GOLD_SOFT};
}}

.btn-secondary {{
  display:inline-block;
  padding:12px 22px;
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

.whatsapp-btn {{
  position:fixed;
  top:70px;
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

.bottom-nav {{
  position:fixed;
  bottom:0;
  left:0;
  right:0;
  background:{CARD_BG};
  border-top:1px solid {BORDER};
  display:flex;
  justify-content:space-around;
  padding:10px 0;
  z-index:999;
}}

.bottom-nav a {{
  text-decoration:none;
  font-size:0.85rem;
  color:{TEXT};
  text-align:center;
}}

.bottom-nav a span {{
  display:block;
  font-size:1.2rem;
}}

.bottom-nav a.active {{
  color:{GOLD};
}}

.class-card {{
  padding:10px;
  border-radius:10px;
  background:rgba(15,23,42,0.03);
  border:1px solid {BORDER};
  margin-bottom:8px;
}}

.required-label::after {{
    content: " *";
    color: #e11d48;
    font-weight: 700;
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

.reg-card {{
  border-radius:14px;
  border:1px solid {BORDER};
  background:{CARD_BG};
  padding:14px 16px;
  margin-bottom:12px;
  box-shadow:0 4px 10px rgba(15,23,42,0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  cursor:pointer;
}}
.reg-card:hover {{
  transform: translateY(-4px);
  box-shadow:0 10px 24px rgba(15,23,42,0.14);
  border-color:{GOLD};
}}

.reg-card-header {{
  display:flex;
  justify-content:space-between;
  align-items:center;
  font-weight:600;
  font-size:1rem;
  color:{TEXT};
}}

.reg-card-sub {{
  font-size:0.9rem;
  color:#6b7280;
  margin-top:4px;
}}

/* -------------------------
   REGISTRATION FORM FIXES
   Ensure all form controls match the dark theme:
   - Background: #151515
   - Text: soft gold (#f5e8c7)
   - Border: gold (#d4af37)
   - Placeholder color adjusted
   - Select arrow and radio visuals themed
   ------------------------- */

label {{
  color:{GOLD_SOFT} !important;
}}

input, textarea, select {{
  background:#151515 !important;
  color:{GOLD_SOFT} !important;
  border:1px solid {GOLD} !important;
  border-radius:8px !important;
}}

input::placeholder, textarea::placeholder {{
  color:{GOLD_SOFT} !important;
  opacity:0.1 !important;
}}

.stTextInput input,
.stTextArea textarea,
.stSelectbox select,
.stDateInput input {{
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
  background:#151515 !important;
  olor:{GOLD_SOFT} !important;
  fill:{GOLD} !important;
}}

.stMultiSelect div {{
  background:#151515 !important;
  color:{GOLD_SOFT} !important;
  border:1px solid {GOLD} !important;
}}

.stRadio label, .stRadio div[role="radio"] {{
  background:#151515 !important;
  color:{GOLD_SOFT} !important;
}}

.stRadio div[role="radio"] input[type="radio"] {{
  background:#151515 !important;
  accent-color: {GOLD} !important;
}}

.stDateInput input {{
  background:#151515 !important;
  color:{GOLD_SOFT} !important;
  border:1px solid {GOLD} !important;
}}

/* FORCE dark theme for selectbox, multiselect, dropdown */
div[data-baseweb="select"] {{
    background: #151515 !important;
    color: #f5e8c7 !important;
    border: 1px solid #d4af37 !important;
}}

div[data-baseweb="select"] * {{
    color: #f5e8c7 !important;
}}

div[data-baseweb="select"] svg {{
    fill: #d4af37 !important;
}}

/* Multiselect chips */
div[data-baseweb="tag"] {{
    background: #8b0000 !important;
    color: #f5e8c7 !important;
    border-radius: 6px !important;
}}

/* Fix radio button text opacity */
.stRadio label {{
    color: #f5e8c7 !important;
    opacity: 1 !important;
}}

/* Gold radio circle */
.stRadio div[role="radio"] {{
    border: 2px solid #d4af37 !important;
}}

.stRadio div[role="radio"] input[type="radio"] {{
    accent-color: #d4af37 !important;
}}

/* Red star for required fields */
.required-label::after {{
    content: " *";
    color: #ff4d4d;
    font-weight: 900;
}}

/* Date input fix */
.stDateInput input {{
    background: #151515 !important;
    color: #f5e8c7 !important;
    border: 1px solid #d4af37 !important;
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
# HEADER — use st.image for logo (fix blue question mark)
# ---------------------------------------------------------
def render_header():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=200)
        else:
            st.markdown(
                f"<div style='text-align:center; color:{GOLD}; font-size:1.6rem; font-weight:700;'>AARA Dance Studio</div>",
                unsafe_allow_html=True
            )

        st.markdown(
            f"""
            <div style="text-align:center; margin-top:6px;">
                <div style="font-size:1.9rem; font-weight:700; color:{GOLD}; font-family:'Playfair Display', serif;">
                    AARA Dance Studio
                </div>
                <div style="font-size:0.95rem; color:{GOLD_SOFT};">
                    Where Passion Meets Performance
                </div>
                <div style="font-size:0.95rem; color:{GOLD_SOFT};">
                    · Fate · Rockwall · Dallas, TX
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
# ---------------------------------------------------------
# WHATSAPP BUTTON (Top Right)
# ---------------------------------------------------------
st.markdown(
    """
    <a class="whatsapp-btn" href="https://wa.me/14692222222" target="_blank">💬</a>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# QR CODE SECTION
# ---------------------------------------------------------
def render_qr_section():
    if qrcode is None:
        return
    st.markdown("#### Quick Registration QR")
    base = st.request.url.split("?")[0] if hasattr(st, "request") else ""
    reg_url = base + "?page=Register"
    try:
        qr_img = qrcode.make(reg_url)
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        buf.seek(0)
        st.image(buf, caption="Scan to open registration page", width=140)
    except Exception:
        st.info("QR generation not available in this environment.")

# ---------------------------------------------------------
# HOME PAGE — Purdance-style hero + slideshow
# ---------------------------------------------------------
def render_home():
    st.markdown(
        f"""
        <div class="section" style="display:flex; flex-direction:column; gap:18px;">
            <div>
                <div style="font-size:2rem; font-weight:800; color:{GOLD}; margin-bottom:6px;">
                    Dance. Express. Shine.
                </div>
                <div style="font-size:1.05rem; color:#4b5563; max-width:520px;">
                    AARA Dance Studio brings Bollywood, Kollywood, Tollywood, Kuthu, Hip Hop and more
                    to Fate · Rockwall · Dallas. A fun, safe space for kids, teens, and adults to find their groove.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Slideshow
    # Slideshow (robust: skip invalid/corrupted files)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("### Studio Moments", unsafe_allow_html=True)

    raw_files = sorted(glob.glob("slide*.jpg")) + sorted(glob.glob("slide*.jpeg")) + sorted(glob.glob("slide*.png"))
    valid_images = []

    for path in raw_files:
        try:
            img = Image.open(path)
            img.load()  # force load to catch errors early
            valid_images.append(img)
        except Exception:
            # Skip files that are not valid images
            continue

    if valid_images:
        st.image(valid_images, width=700)
    else:
        st.info("Upload valid slide1.jpg, slide2.jpg, slide3.jpg (etc.) in the root directory for a slideshow.")


    st.markdown(
        f"""
        <div style="margin-top:10px;">
            <a class="btn-primary" href="/?page=Register">Register Now</a>
            &nbsp;&nbsp;
            <a class="btn-primary" href="/?page=Classes">View Classes</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
        """
        <div class="class-card">
            <b>Tiny Stars (Ages 5–8)</b><br>
            Beginner / Intermediate<br>
            Wed & Fri · 6:30–7:30 PM<br>
            4 classes: $60 · 8 classes: $100
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="class-card">
            <b>Shining Stars (Ages 9+)</b><br>
            Beginner / Intermediate<br>
            Tue · 7–8 PM<br>
            4 classes: $60 · 8 classes: $100
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="class-card">
            <b>Dream Chasers (Ladies 18+)</b><br>
            Beginner / Intermediate<br>
            Thu 6:30–7:30 PM · Sat 10:30–11:30 AM<br>
            4 classes: $50 · 8 classes: $80
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<a class="btn-primary" href="/?page=Register">Register Now</a>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# ABOUT PAGE
# ---------------------------------------------------------
def render_about():
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align:center; font-size:1.8rem; font-weight:800; margin-bottom:10px;">
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
        <ul style="font-size:1rem; line-height:1.6; margin-top:10px;">
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
# REGISTRATION PAGE — Vertical Cards with Hover + Form
# (Only styling changes applied above; structure unchanged)
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
                             placeholder=required_placeholders["student_name"],
                             label_visibility="visible")
        st.markdown('<span class="required-label"></span>', unsafe_allow_html=True)

        dob = st.text_input("Date of Birth (Age)", key="dob",
                            placeholder=required_placeholders["dob"],label_visibility="visible")
        st.markdown('<span class="required-label"></span>', unsafe_allow_html=True)
        
        gender = st.selectbox("Gender", ["", "Female", "Male", "Other", "Prefer not to say"], key="gender",label_visibility="visible")
        st.markdown('<span class="required-label"></span>', unsafe_allow_html=True)
        
        school = st.text_input("School Name (optional)", key="school",label_visibility="visible")
        st.markdown('<span class="required-label"></span>', unsafe_allow_html=True)

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


        submitted = st.form_submit_button("Submit Now")

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
