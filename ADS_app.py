```python
# ADS_app.py - B02 (B00 baseline + B01 fixes preserved; B02 updates: cleaned syntax, slideshow autoplay, single submit button label "Submit Form", robust validation, admin CSV export)
# Baseline: B00 theme + B01 fixes (always preserved)
# Version: B02

import streamlit as st
import pandas as pd
import os
import json
import glob
from datetime import datetime, date
from PIL import Image
import io

# Optional dependency
try:
    import qrcode
except ImportError:
    qrcode = None

# PAGE CONFIG
st.set_page_config(
    page_title="AARA Dance Studio",
    page_icon="🩰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# DATA PATHS
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
REG_FILE = os.path.join(DATA_DIR, "registrations.csv")
VISIT_FILE = os.path.join(DATA_DIR, "site_visits.csv")
LOGO_PATH = "logo.png"

# SESSION STATE
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

params = st.experimental_get_query_params()
if "page" in params:
    st.session_state.page = params["page"][0]

page = st.session_state.page

# THEME COLORS (flyer style baseline B00)
BG_TOP = "#0a0a0a"
BG_BOTTOM = "#1a1a1a"
GOLD = "#d4af37"
GOLD_SOFT = "#f5e8c7"
RED = "#8b0000"
TEXT = "#f5e8c7"
CARD_BG = "#111111"
BORDER = "#3a3a3a"

# CSS - Flyer theme + animations + form field styling + slideshow
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
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}}

.block-container {{
  padding-top: 40px !important;
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
  background: {GOLD};
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
  background:transparent;
  color:{GOLD} !important;
  border-radius:999px;
  border:1px solid {GOLD};
  text-decoration:none;
  font-weight:500;
  transition: background 0.2s ease;
}}
.btn-secondary:hover {{
  background: rgba(212,175,55,0.06);
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
  color: #ff4d4d;
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

/* === DARK-GOLD FORM THEME FIX === */
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
  opacity:0.85 !important;
}}

/* Selectbox + Dropdown */
div[data-baseweb="select"] {{
  background-color: #151515 !important;
  color: {GOLD_SOFT} !important;
  border: 1px solid {GOLD} !important;
  border-radius: 8px !important;
}}
div[data-baseweb="select"] * {{
  color: {GOLD_SOFT} !important;
}}
div[data-baseweb="select"] svg {{
  fill: {GOLD} !important;
}}

/* Multiselect */
.stMultiSelect div[data-baseweb="select"] {{
  background-color: #151515 !important;
  color: {GOLD_SOFT} !important;
  border: 1px solid {GOLD} !important;
}}
.stMultiSelect div[data-baseweb="select"] * {{
  color: {GOLD_SOFT} !important;
}}
div[data-baseweb="tag"] {{
  background-color: {RED} !important;
  color: {GOLD_SOFT} !important;
  border-radius: 6px !important;
  border: 1px solid {GOLD} !important;
}}

/* Radio buttons */
.stRadio label {{
  color: {GOLD_SOFT} !important;
  opacity: 1 !important;
}}
.stRadio div[role="radio"] {{
  background-color: #151515 !important;
  border: 2px solid {GOLD} !important;
  border-radius: 50% !important;
}}
.stRadio div[role="radio"] input[type="radio"] {{
  accent-color: {GOLD} !important;
}}

/* Date input */
.stDateInput input {{
  background-color: #151515 !important;
  color: {GOLD_SOFT} !important;
  border: 1px solid {GOLD} !important;
}}

/* Slideshow container */
.slideshow {{
  position: relative;
  width: 100%;
  max-width: 900px;
  height: 360px;
  overflow: hidden;
  border-radius: 12px;
  border:1px solid {BORDER};
  margin: 0 auto 12px auto;
}}
.slide {{
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 1s ease;
  background-size: cover;
  background-position: center;
}}
.slide.active {{
  opacity: 1;
}}
.slide-overlay {{
  position: absolute;
  left: 20px;
  bottom: 20px;
  color: {GOLD_SOFT};
  background: rgba(0,0,0,0.35);
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid rgba(212,175,55,0.08);
}}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# UTILITIES
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

# HEADER - use st.image for logo (centered, glowing)
def render_header():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists(LOGO_PATH):
            # center logo with gold glow via inline HTML wrapper
            st.markdown(
                f"""
                <div style="text-align:center;">
                  <div style="display:inline-block; padding:12px; border-radius:999px; box-shadow:0 8px 30px rgba(212,175,55,0.18); background: radial-gradient(circle at 30% 30%, rgba(212,175,55,0.06), transparent 40%);">
                    <img src="data:image/png;base64,{_img_to_base64(LOGO_PATH)}" width="120" style="border-radius:999px;"/>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='text-align:center; color:{GOLD}; font-size:1.6rem; font-weight:700; font-family:\"Playfair Display\", serif;'>AARA Dance Studio</div>",
                unsafe_allow_html=True,
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

# Helper to convert image to base64 for inline embedding (keeps logo rendering robust)
def _img_to_base64(path):
    import base64
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except Exception:
        return ""

# WHATSAPP BUTTON (Top Right)
st.markdown(
    f"""
    <a class="whatsapp-btn" href="https://wa.me/14692222222" target="_blank" title="Chat on WhatsApp">
      💬
    </a>
    """,
    unsafe_allow_html=True,
)

# QR CODE SECTION
def render_qr_section():
    if qrcode is None:
        return
    # Build registration URL from current page base
    base = st.experimental_get_query_params()
    # Use current host path if available; fallback to root
    try:
        # Attempt to build a relative link to the Register page
        reg_url = "/?page=Register"
        qr_img = qrcode.make(reg_url)
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        buf.seek(0)
        st.image(buf, caption="Scan to open registration page", width=140)
    except Exception:
        st.info("QR generation not available in this environment.")

# HOME PAGE - Hero + slideshow
def render_home():
    render_header()
    st.markdown(
        f"""
        <div class="section" style="display:flex; flex-direction:column; gap:18px;">
          <div>
            <div style="font-size:2rem; font-weight:800; color:{GOLD}; margin-bottom:6px;">
              Dance. Express. Shine.
            </div>
            <div style="font-size:1.05rem; color:#4b5563; max-width:720px;">
              AARA Dance Studio brings Bollywood, Kollywood, Tollywood, Kuthu, Hip Hop and more
              to Fate · Rockwall · Dallas. A fun, safe space for kids, teens, and adults to find their groove.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Slideshow: gather slide images named slide1.jpg ... slide5.jpg
    slide_paths = []
    for i in range(1, 6):
        for ext in ("jpg", "jpeg", "png", "webp"):
            p = f"slide{i}.{ext}"
            if os.path.exists(p):
                slide_paths.append(p)
                break

    # If fewer than 4 slides found, also include any slide*.jpg/png files
    if len(slide_paths) < 4:
        extras = sorted(glob.glob("slide*.jpg") + glob.glob("slide*.jpeg") + glob.glob("slide*.png"))
        for p in extras:
            if p not in slide_paths:
                slide_paths.append(p)
            if len(slide_paths) >= 5:
                break

    if not slide_paths:
        st.info("Upload slide1.jpg, slide2.jpg, slide3.jpg, slide4.jpg (etc.) in the root directory for a slideshow.")
    else:
        # Build slideshow HTML with autoplay (6s per slide) and fade transitions
        slides_html = []
        for idx, path in enumerate(slide_paths):
            b64 = _img_to_base64(path)
            style = f"background-image: url('data:image/png;base64,{b64}');"
            active = "active" if idx == 0 else ""
            slides_html.append(f'<div class="slide {active}" style="{style}"></div>')

        slides_block = "\n".join(slides_html)
        slideshow_html = f"""
        <div class="section">
          <div class="slideshow" id="slideshow">
            {slides_block}
            <div class="slide-overlay">Studio Moments</div>
          </div>
          <div style="text-align:center; margin-top:8px;">
            <a class="btn-primary" href="/?page=Register">Register Now</a>
            &nbsp;&nbsp;
            <a class="btn-secondary" href="/?page=Classes">View Classes</a>
          </div>
        </div>

        <script>
        (function() {{
          const slides = document.querySelectorAll('#slideshow .slide');
          let idx = 0;
          const total = slides.length;
          const interval = 6000; // 6s per slide
          function show(i) {{
            slides.forEach((s, si) => {{
              s.classList.toggle('active', si === i);
            }});
          }}
          if (total > 1) {{
            setInterval(() => {{
              idx = (idx + 1) % total;
              show(idx);
            }}, interval);
          }}
        }})();
        </script>
        """
        st.markdown(slideshow_html, unsafe_allow_html=True)

    render_qr_section()

# CLASSES PAGE
def render_classes():
    render_header()
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Programs & Fees</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Choose the program that fits your dancer best.</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="class-card">
          <b>Tiny Stars (Ages 5-8)</b><br>
          Beginner / Intermediate<br>
          Wed & Fri · 6:30-7:30 PM<br>
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
          Tue · 7-8 PM<br>
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
          Thu 6:30-7:30 PM · Sat 10:30-11:30 AM<br>
          4 classes: $50 · 8 classes: $80
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div style="margin-top:8px;"><a class="btn-primary" href="/?page=Register">Register Now</a></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ABOUT PAGE
def render_about():
    render_header()
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align:center; font-size:1.8rem; font-weight:800; margin-bottom:10px; color: {gold};">
          Find your Groove!
        </div>
        """.replace("{gold}", GOLD),
        unsafe_allow_html=True,
    )

    if os.path.exists("instructor.jpg"):
        st.image("instructor.jpg", width=260)
    else:
        st.info("Instructor photo placeholder (upload instructor.jpg in root directory).")

    st.markdown(
        """
        <ul style="font-size:1rem; line-height:1.6; margin-top:10px; color: #f5e8c7;">
          <li><b>Bollywood</b> - A fun and energetic dance style inspired by Hindi movie songs and Indian cinema.</li>
          <li><b>Kollywood</b> - A vibrant dance form based on Tamil movie music, known for expressive moves and powerful energy.</li>
          <li><b>Tollywood</b> - A lively dance style inspired by Telugu film songs, featuring fast beats and dynamic choreography.</li>
          <li><b>Semi-Classical</b> - A graceful blend of classical Indian dance techniques with modern expressions and music.</li>
          <li><b>Freestyle</b> - A creative dance form that allows dancers to move freely and express themselves without fixed rules.</li>
          <li><b>Hip Hop</b> - A trendy and energetic street dance style with sharp movements, rhythm, and attitude.</li>
          <li><b>Kuthu</b> - A high-energy South Indian folk-inspired dance style known for its fun beats and energetic moves.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ADMIN PAGE (password protected, CSV download)
def render_admin():
    render_header()
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Admin</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Restricted access. View registrations and site visits.</div>', unsafe_allow_html=True)

    if not st.session_state.admin_authenticated:
        pwd = st.text_input("Enter admin password", type="password", key="admin_pwd")
        if st.button("Authenticate"):
            # Simple password check - in production, replace with secure auth
            if pwd == "adminpass":
                st.session_state.admin_authenticated = True
                st.success("Authenticated.")
            else:
                st.error("Incorrect password.")
    else:
        regs = read_csv(REG_FILE)
        visits = read_csv(VISIT_FILE)
        st.markdown("**Registrations**")
        st.dataframe(regs)
        if not regs.empty:
            csv = regs.to_csv(index=False).encode("utf-8")
            st.download_button("Download registrations CSV", data=csv, file_name="registrations.csv", mime="text/csv")
        st.markdown("**Site Visits**")
        st.dataframe(visits)
        if not visits.empty:
            csv2 = visits.to_csv(index=False).encode("utf-8")
            st.download_button("Download visits CSV", data=csv2, file_name="site_visits.csv", mime="text/csv")

    st.markdown('</div>', unsafe_allow_html=True)

# REGISTRATION PAGE - Vertical Cards with Hover + Form
def render_register():
    render_header()
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Student Registration</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Fill in the details below to secure your spot.</div>', unsafe_allow_html=True)

    # placeholders used for JS highlighting
    required_placeholders = {
        "student_name": "_req_student_name",
        "dob": "_req_dob",
        "pref_time": "_req_pref_time",
        "signature": "_req_signature"
    }

    # Use a single form with one submit button labeled "Submit Form"
    with st.form("reg_form", clear_on_submit=False):
        # Card 1 - Student Info
        st.markdown(
            """
            <div class="reg-card">
              <div class="reg-card-header">
                <span>Student Information</span>
                <span></span>
              </div>
              <div class="reg-card-sub">Basic details about the student.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        student_name = st.text_input("Student Name", key="student_name",
                                     placeholder=required_placeholders["student_name"],
                                     label_visibility="visible")
        st.markdown('<span class="required-label"></span>', unsafe_allow_html=True)

        dob = st.text_input("Date of Birth (Age)", key="dob",
                            placeholder=required_placeholders["dob"], label_visibility="visible")
        st.markdown('<span class="required-label"></span>', unsafe_allow_html=True)

        gender = st.selectbox("Gender", ["", "Female", "Male", "Other", "Prefer not to say"], key="gender", label_visibility="visible")
        st.markdown('<span class="required-label"></span>', unsafe_allow_html=True)

        school = st.text_input("School Name (optional)", key="school", label_visibility="visible")

        # Card 2 - Class Details
        st.markdown(
            """
            <div class="reg-card">
              <div class="reg-card-header">
                <span>Class Details</span>
                <span></span>
              </div>
              <div class="reg-card-sub">Choose how and when you'd like to dance.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        enrollment = st.selectbox("Enrollment Type", ["", "Regular ($50/month)", "Drop-in ($15/session)"], key="enroll")
        mode = st.radio("Mode", ["In-Person", "Online"], key="mode")
        workshops = st.multiselect("Workshops", ["Ladies Kuthu Workshop", "Couple Dance Fitness Workshop"], key="workshops")
        level = st.selectbox("Level", ["", "Beginner", "Intermediate", "Advanced"], key="level")
        pref_time = st.text_input("Preferred Days/Time", key="pref_time", placeholder=required_placeholders["pref_time"])
        experience = st.text_area("Previous Experience", key="experience")

        # Card 3 - Parent & Emergency Contact
        st.markdown(
            """
            <div class="reg-card">
              <div class="reg-card-header">
                <span>Parent & Emergency Contact</span>
                <span></span>
              </div>
              <div class="reg-card-sub">Who should we reach out to if needed?</div>
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

        # Card 4 - Medical & Consent
        st.markdown(
            """
            <div class="reg-card">
              <div class="reg-card-header">
                <span>Medical & Consent</span>
                <span>☒</span>
              </div>
              <div class="reg-card-sub">Safety information and media consent.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        medical = st.text_area("Allergies / Injuries / Conditions", key="medical")
        consent = st.radio("Allow photo/video for promotions?", ["", "Yes", "No"], key="consent")
        signature = st.text_input("Parent/Guardian Signature", key="signature", placeholder=required_placeholders["signature"])
        sig_date = st.date_input("Date", value=date.today(), key="sig_date")

        # Single submit button labeled "Submit Form"
        submitted = st.form_submit_button("Submit Form")

    # Validation and saving
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

            # Client-side highlight + shake animation via JS
            js = f"""
            <script>
            (function() {{
              try {{
                const missing = {json.dumps(missing_placeholders)};
                missing.forEach(p => {{
                  const el = document.querySelector('[placeholder="'+p+'"]');
                  if (el) {{
                    el.style.borderColor = "#e11d48";
                    el.style.boxShadow = "0 0 0 3px rgba(225,29,72,0.08)";
                  }}
                }});
                const sections = window.parent.document.querySelectorAll('.section');
                if (sections.length > 0) {{
                  const last = sections[sections.length - 1];
                  last.classList.add('shake');
                  setTimeout(() => last.classList.remove('shake'), 600);
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
                "workshops": "; ".join(workshops) if workshops else "",
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

# PAGE ROUTER
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
    # default to home
    render_home()

# BOTTOM NAV
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
      <a class="{admin}" href="/?page=Admin"><span>🔒</span>Admin</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# FOOTER
st.markdown('<div class="footer">@ AARA Dance Studio · Fate · Rockwall · Dallas, TX</div>', unsafe_allow_html=True)
