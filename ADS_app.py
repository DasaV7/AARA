# ADS_app.py - C04.1 (fixes)
# Baseline: C03/C04
# Fixes in this variant:
# - Classes page: class types displayed as vertical cards (stacked), new banner moved to just above Register button
# - Registration page: removed st.button() from inside form (caused StreamlitAPIException)
#   - "View Terms & Policies" is now an expander placed above the form (opens text box)
#   - Inside the form there is a required checkbox "I agree to the Terms & Policies" (st.checkbox inside form)
#   - Submit button restored using st.form_submit_button()
# - Minor layout tweaks to ensure the submit button and terms checkbox are visible and required
# - Preserves slideshow, logo centering, dark form styling, early-bird pricing, and other C04 features

import streamlit as st
import pandas as pd
import os
import json
import base64
from datetime import datetime, date

# Optional QR code support
try:
    import qrcode
except ImportError:
    qrcode = None

# PAGE CONFIG
st.set_page_config(
    page_title="AARA Dance Studio",
    page_icon="💃",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# DATA PATHS
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
REG_FILE = os.path.join(DATA_DIR, "registrations.csv")
VISIT_FILE = os.path.join(DATA_DIR, "site_visits.csv")
LOGO_PATH = "logo.png"

# SESSION STATE defaults
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False
# agree_terms will be stored by the checkbox inside the form (no pre-init required)

params = st.query_params
if "page" in params:
    st.session_state.page = params["page"]

page = st.session_state.page

# THEME COLORS (flyer style baseline)
BG_TOP = "#0a0a0a"
BG_BOTTOM = "#1a1a1a"
GOLD = "#d4af37"
GOLD_SOFT = "#f5e8c7"
RED = "#8b0000"
TEXT = "#f5e8c7"
CARD_BG = "#111111"
BORDER = "#3a3a3a"

# CSS: C02 global CSS (form fixes) + slideshow CSS (working engine) + logo centering override + button overrides
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
  padding-top: 40px !important;
  max-width: 900px !important;
  animation: fadeIn 0.4s ease;
}}

@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(6px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

.section {{
  background: {CARD_BG};
  padding: 18px;
  border-radius: 14px;
  border: 1px solid {BORDER};
  margin-bottom: 14px;
}}

.title {{
  font-size: 1.6rem;
  font-weight: 700;
  color: {GOLD};
  font-family: 'Playfair Display', serif;
}}

.subtitle {{
  font-size: 1rem;
  color: {GOLD_SOFT};
  margin-bottom: 10px;
}}

.btn-primary {{
  display: inline-block;
  padding: 12px 22px;
  background: {GOLD};
  color: {BG_TOP} !important;
  border-radius: 999px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.2s ease;
}}

.btn-primary:hover {{
  background: {GOLD_SOFT};
}}

.whatsapp-btn {{
  position: fixed;
  top: 70px;
  right: 20px;
  background: #25D366;
  color: white;
  padding: 14px 16px;
  border-radius: 50%;
  font-size: 22px;
  text-decoration: none;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  z-index: 9999;
}}

.bottom-nav {{
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: {CARD_BG};
  border-top: 1px solid {BORDER};
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  z-index: 999;
}}

.bottom-nav a {{
  text-decoration: none;
  font-size: 0.85rem;
  color: {TEXT};
  text-align: center;
}}

.bottom-nav a span {{
  display: block;
  font-size: 1.2rem;
}}

.bottom-nav a.active {{
  color: {GOLD};
}}

.class-card {{
  padding: 14px;
  border-radius: 12px;
  background: rgba(15,23,42,0.03);
  border: 1px solid {BORDER};
  margin-bottom: 12px;
  max-width: 920px;
  margin-left: auto;
  margin-right: auto;
}}

.required-label::after {{
  content: " *";
  color: #ff4d4d;
  font-weight: 900;
}}

.footer {{
  text-align: center;
  color: #9ca3af;
  font-size: 0.8rem;
  margin-top: 40px;
  margin-bottom: 60px;
}}

.reg-card {{
  border-radius: 14px;
  border: 1px solid {BORDER};
  background: {CARD_BG};
  padding: 14px 16px;
  margin-bottom: 12px;
  box-shadow: 0 4px 10px rgba(15,23,42,0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  cursor: pointer;
}}

.reg-card:hover {{
  transform: translateY(-4px);
  box-shadow: 0 10px 24px rgba(15,23,42,0.14);
  border-color: {GOLD};
}}

.reg-card-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 1rem;
  color: {TEXT};
}}

.reg-card-sub {{
  font-size: 0.9rem;
  color: #6b7280;
  margin-top: 4px;
}}

/* REGISTRATION FORM FIXES - dark fields + gold labels (C02) */
label {{
  color: {GOLD_SOFT} !important;
}}

input, textarea, select {{
  background: #151515 !important;
  color: {GOLD_SOFT} !important;
  border: 1px solid {GOLD} !important;
  border-radius: 8px !important;
}}

input::placeholder,
textarea::placeholder {{
  color: {GOLD_SOFT} !important;
  opacity: 0.4 !important;
}}

.stTextInput input,
.stTextArea textarea,
.stDateInput input {{
  background: #151515 !important;
  color: {GOLD_SOFT} !important;
  border: 1px solid {GOLD} !important;
}}

/* Force dark theme for selectbox and multiselect (C02) */
.stSelectbox > div > div {{
  background: #151515 !important;
  color: {GOLD_SOFT} !important;
  border: 1px solid {GOLD} !important;
}}

.stMultiSelect > div > div {{
  background: #151515 !important;
  color: {GOLD_SOFT} !important;
  border: 1px solid {GOLD} !important;
}}

.stMultiSelect div[data-baseweb="select"] {{
  background: #151515 !important;
  color: #f5e8c7 !important;
  border: 1px solid #d4af37 !important;
}}

.stMultiSelect div[data-baseweb="select"] * {{
  background: #151515 !important;
  color: #f5e8c7 !important;
}}

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

/* Gold radio circle */
.stRadio div[role="radio"] {{
  border: 2px solid #d4af37 !important;
}}

.stRadio div[role="radio"] input[type="radio"] {{
  accent-color: #d4af37 !important;
}}

/* Logo glow wrapper - ensure perfect centering on all devices */
.logo-wrapper {{
  display: flex;
  justify-content: center !important;
  align-items: center;
  width: 100%;
  margin: 0 auto 8px auto !important;
  text-align: center;
}}
.logo-circle {{
  border-radius: 50%;
  padding: 10px;
  box-shadow: 0 0 40px rgba(212,175,55,0.7);
  background: radial-gradient(circle, rgba(212,175,55,0.35) 0%, rgba(0,0,0,0.9) 60%);
}}
.logo-circle img {{
  display: block;
  margin: 0 auto;
  max-width: 340px;
  height: auto;
}}

/* Force Streamlit buttons (including submit) to use dark/gold theme even in light mode */
.stButton>button, .stDownloadButton>button {{
  background: {GOLD} !important;
  color: {BG_TOP} !important;
  border-radius: 999px !important;
  border: 1px solid {GOLD} !important;
  padding: 8px 18px !important;
  font-weight: 600 !important;
}}
.stButton>button:hover, .stDownloadButton>button:hover {{
  background: {GOLD_SOFT} !important;
  color: {BG_TOP} !important;
}}

/* === SLIDESHOW SECTION (working CSS-only slideshow) ===
   Full-width inside content column, cinematic height 400px, rounded corners 12px.
*/
.slideshow {{
  position: relative;
  width: 100%;
  max-width: 920px;
  height: 400px;
  margin: 0 auto 12px auto;
  border-radius: 12px;
  overflow: hidden;
  border:1px solid {BORDER};
  box-shadow: 0 10px 30px rgba(0,0,0,0.6);
}}
.slide {{
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  opacity: 0;
  animation-name: slidefade;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
}}
@keyframes slidefade {{
  0%   {{ opacity: 0; }}
  8%   {{ opacity: 1; }}
  25%  {{ opacity: 1; }}
  33%  {{ opacity: 0; }}
  100% {{ opacity: 0; }}
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
  z-index: 6;
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


def get_registration_count():
    if os.path.exists(REG_FILE):
        try:
            df = pd.read_csv(REG_FILE)
            return len(df)
        except Exception:
            return 0
    return 0


def is_early_bird_active():
    return get_registration_count() < 10


def get_pricing():
    # Early bird: cheaper 4-class price, 8-class updated to $100
    if is_early_bird_active():
        return {
            "four": 50,
            "eight": 100,
            "enrollment": 50,  # $50/month early bird
        }
    else:
        return {
            "four": 60,
            "eight": 100,
            "enrollment": 60,
        }


log_visit()

# Helper: convert image file to base64 string
def _img_to_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except Exception:
        return None

# HEADER - centered glowing logo (used on all pages)
def render_header():
    # Use a full-width HTML block with embedded base64 image to ensure perfect centering on desktop + mobile
    if os.path.exists(LOGO_PATH):
        b64 = _img_to_base64(LOGO_PATH)
        if b64:
            img_tag = f'<img src="data:image/png;base64,{b64}" alt="AARA Dance Studio logo" style="max-width:340px; height:auto;">'
        else:
            img_tag = f'<img src="{LOGO_PATH}" alt="AARA Dance Studio logo" style="max-width:340px; height:auto;">'
        st.markdown(
            f"<div class='logo-wrapper'><div class='logo-circle'>{img_tag}</div></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class='logo-wrapper'>
              <div class='logo-circle' style='padding:14px;'>
                <div style='font-size:1.6rem; font-weight:800; color:{GOLD};'>AARA Dance Studio</div>
              </div>
            </div>
            """,
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


def render_early_banner():
    pricing = get_pricing()
    enroll_price = pricing["enrollment"]
    # Early bird message includes time-specific offer for 3 months
    if is_early_bird_active():
        st.markdown(
            f"""
            <div class="early-banner" style="max-width:980px; margin:10px auto 16px auto; text-align:center; border:1px solid {GOLD}; background:{RED}; color:{GOLD_SOFT}; padding:10px 16px; border-radius:999px;">
              ★ Early Bird Offer ★&nbsp;&nbsp;
              <b>${enroll_price}/month for 3 months (June, July &amp; August)</b> — Limited to first 10 registrations!
              <br>
              4 classes early-bird: <b>${pricing['four']}</b> · 8 classes: <b>${pricing['eight']}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # If early bird not active, show a subtle banner with current pricing
        st.markdown(
            f"""
            <div class="early-banner" style="max-width:980px; margin:10px auto 16px auto; text-align:center; border:1px solid {GOLD}; background:transparent; color:{GOLD_SOFT}; padding:8px 16px; border-radius:999px;">
              Enrollment: <b>${pricing['enrollment']}</b>/month · 4 classes: <b>${pricing['four']}</b> · 8 classes: <b>${pricing['eight']}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )


render_header()
render_early_banner()

# WHATSAPP BUTTON (Top Right)
st.markdown(
    """
    <a class="whatsapp-btn" href="https://wa.me/14692222222" target="_blank">
      💬
    </a>
    """,
    unsafe_allow_html=True,
)

# QR CODE SECTION
def render_qr_section():
    if qrcode is None:
        return
    st.markdown("#### Quick Registration QR")
    base = ""
    try:
        if hasattr(st, "request") and hasattr(st.request, "url"):
            base = st.request.url.split("?")[0]
    except Exception:
        base = ""
    reg_url = (base or "/") + "?page=Register"
    try:
        qr_img = qrcode.make(reg_url)
        st.image(qr_img, caption="Scan to open registration page", width=140)
    except Exception:
        st.info("QR generation not available in this environment.")

# Build CSS-only slideshow HTML block (no components, no iframe)
def render_slideshow(slide_paths, per_slide_seconds=6):
    # If no slides, show placeholder
    if not slide_paths:
        st.markdown(
            f"""
            <div class="section" style="max-width:920px; margin:0 auto;">
              <h3 style="margin-top:0; margin-bottom:8px;">Studio Moments</h3>
              <p style="color:#9ca3af;">Upload slide1.jpg, slide2.jpg, slide3.jpg (etc.) in the root directory for a slideshow.</p>
              <div style="margin-top:10px;">
                <a class="btn-primary" href="/?page=Register">Register Now</a>
                &nbsp;&nbsp;
                <a class="btn-primary" href="/?page=Classes">View Classes</a>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Prepare slides HTML with base64 backgrounds and staggered animation delays.
    n = len(slide_paths)
    total_duration = n * per_slide_seconds  # seconds
    slides_html = []
    for idx, path in enumerate(slide_paths):
        b64 = _img_to_base64(path)
        if b64:
            mime = "jpeg" if path.lower().endswith((".jpg", ".jpeg")) else "png"
            bg = f"url('data:image/{mime};base64,{b64}')"
        else:
            # fallback to path (if accessible)
            bg = f"url('{path}')"
        # Negative delay ensures sequencing; use seconds with 's'
        delay = -(idx * per_slide_seconds)
        slides_html.append(
            f'<div class="slide" style="background-image: {bg}; animation-duration: {total_duration}s; animation-delay: {delay}s;"></div>'
        )

    slides_block = "\n".join(slides_html)
    html = f"""
    <div class="section" style="padding:0; border-radius:12px; border:0; background:transparent;">
      <div class="slideshow" id="slideshow">
        {slides_block}
        <div class="slide-overlay">Studio Moments</div>
      </div>
      <div style="text-align:center; margin-top:10px;">
        <a class="btn-primary" href="/?page=Register">Register Now</a>
        &nbsp;&nbsp;
        <a class="btn-primary" href="/?page=Classes">View Classes</a>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# HOME PAGE - hero + slideshow
def render_home():
    # Hero text
    st.markdown(
        f"""
        <div class="section" style="display:flex; flex-direction:column; gap:18px;">
          <div>
            <div style="font-size:2rem; font-weight:800; color:{GOLD}; margin-bottom:6px;">
              Dance. Express. Shine.
            </div>
            <div style="font-size:1.05rem; color:#e5e7eb; max-width:720px;">
              AARA Dance Studio brings Bollywood, Kollywood, Tollywood, Kuthu, Hip Hop and more
              to Fate · Rockwall · Dallas. A fun, safe space for kids, teens, and adults to find their groove.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Collect slideshow images (slide1.jpg ... slide5.jpg)
    image_paths = []
    for i in range(1, 6):
        candidate = f"slide{i}.jpg"
        if os.path.exists(candidate):
            image_paths.append(candidate)

    # Render CSS-only slideshow (full-width inside content column)
    render_slideshow(image_paths, per_slide_seconds=6)

    render_qr_section()

# CLASSES PAGE (dynamic pricing) with vertical cards and banner moved before Register button
def render_classes():
    pricing = get_pricing()
    four = pricing["four"]
    eight = pricing["eight"]

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Programs & Fees</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Choose the program that fits your dancer best.</div>',
        unsafe_allow_html=True,
    )

    # Vertical cards (stacked) for each class type
    st.markdown(
        f"""
        <div class="class-card">
          <b>Tiny Stars (Ages 5-8)</b><br>
          Beginner / Intermediate<br>
          Wed &amp; Fri · 6:30-7:30 PM<br>
          4 classes: ${four} · 8 classes: ${eight}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="class-card">
          <b>Shining Stars (Ages 9+)</b><br>
          Beginner / Intermediate<br>
          Tue · 7-8 PM<br>
          4 classes: ${four} · 8 classes: ${eight}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="class-card">
          <b>Dream Chasers (Ladies 18+)</b><br>
          Beginner / Intermediate<br>
          Thu 6:30-7:30 PM · Sat 10:30-11:30 AM<br>
          4 classes: ${four} · 8 classes: ${eight}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # New banner placed just above the Register button (as requested)
    st.markdown(
        f"""
        <div style="max-width:920px; margin:12px auto 8px auto; padding:12px; border-radius:12px; background: rgba(17,17,17,0.6); border:1px solid {BORDER}; text-align:center;">
          <div style="font-weight:700; color:{GOLD}; margin-bottom:6px;">Online &amp; Zoom sessions are available</div>
          <div style="color:{GOLD_SOFT};">Drop-in classes for any batch: <b>$15/session</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Register CTA
    st.markdown(
        '<div style="text-align:center; margin-top:10px;"><a class="btn-primary" href="/?page=Register">Register Now</a></div>',
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ABOUT PAGE
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
          <li><b>Bollywood · Kollywood · Tollywood · Kuthu · Hip Hop</b></li>
          <li>Fun, high-energy choreography tailored for kids, teens, and adults.</li>
          <li>Safe, inclusive environment where every dancer can shine.</li>
          <li>Performance opportunities at local events and showcases.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ADMIN PAGE
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
            st.download_button(
                "Download Registrations CSV",
                regs.to_csv(index=False),
                "registrations.csv",
            )

        st.subheader("Site Visits")
        if visits.empty:
            st.info("No visits yet.")
        else:
            st.dataframe(visits)
            st.download_button(
                "Download Visits CSV",
                visits.to_csv(index=False),
                "site_visits.csv",
            )

        st.markdown("---")
        if st.button("Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# REGISTRATION PAGE - vertical cards + terms expander + required checkbox + submit button
def render_register():
    pricing = get_pricing()
    enroll_price = pricing["enrollment"]
    eight_price = pricing["eight"]

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Student Registration</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Fill in the details below to secure your spot.</div>',
        unsafe_allow_html=True,
    )

    required_placeholders = {
        "student_name": "_req_student_name",
        "dob": "_req_dob",
        "pref_time": "_req_pref_time",
        "signature": "_req_signature",
    }

    # Terms & Policies expander (outside the form) - opens a text box with the policy
    with st.expander("View Terms & Policies", expanded=False):
        st.markdown(
            """
            📜 **Terms & Policies**
            - Monthly fees must be paid on time.
            - Drop-in classes must be paid before each session.
            - Missed classes are non-refundable.
            - Students are expected to maintain discipline and regular attendance.
            - Opportunities for stage performances, community events & competitions will be provided.
            - Priority will be given to regular (monthly) students for performances and events.
            """,
            unsafe_allow_html=True,
        )

    # The form (submit button must be inside the form)
    with st.form("reg_form", clear_on_submit=False):
        # Card 1 - Student Info
        st.markdown(
            """
            <div class="reg-card">
              <div class="reg-card-header">
                <span>Student Information</span>
                <span></span>
              </div>
              <div class="reg-card-sub">
                Basic details about the student.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<label class="required-label">Student Name</label>', unsafe_allow_html=True)
        student_name = st.text_input("", key="student_name", placeholder=required_placeholders["student_name"], label_visibility="collapsed")

        st.markdown('<label class="required-label">Date of Birth (Age)</label>', unsafe_allow_html=True)
        dob = st.text_input("", key="dob", placeholder=required_placeholders["dob"], label_visibility="collapsed")

        st.markdown('<label class="required-label">Gender</label>', unsafe_allow_html=True)
        gender = st.selectbox("", ["", "Female", "Male", "Other", "Prefer not to say"], key="gender", label_visibility="collapsed")

        st.markdown('<label>School Name (optional)</label>', unsafe_allow_html=True)
        school = st.text_input("", key="school", label_visibility="collapsed")

        # Card 2 - Class Details
        st.markdown(
            """
            <div class="reg-card">
              <div class="reg-card-header">
                <span>Class Details</span>
                <span></span>
              </div>
              <div class="reg-card-sub">
                Choose how and when you'd like to dance.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<label class="required-label">Enrollment Type</label>', unsafe_allow_html=True)
        enrollment = st.selectbox(
            "",
            [
                "",
                f"Regular (${enroll_price}/month)",
                f"4 Classes (${pricing['four']})",
                f"8 Classes (${eight_price})",
                "Drop-in ($15/session)",
            ],
            key="enroll",
            label_visibility="collapsed",
        )

        st.markdown('<label class="required-label">Mode</label>', unsafe_allow_html=True)
        mode = st.radio("", ["In-Person", "Online"], key="mode", label_visibility="collapsed")

        st.markdown('<label>Workshops</label>', unsafe_allow_html=True)
        workshops = st.multiselect("", ["Ladies Kuthu Workshop", "Couple Dance Fitness Workshop"], key="workshops", label_visibility="collapsed")

        st.markdown('<label class="required-label">Level</label>', unsafe_allow_html=True)
        level = st.selectbox("", ["", "Beginner", "Intermediate", "Advanced"], key="level", label_visibility="collapsed")

        st.markdown('<label class="required-label">Preferred Days/Time</label>', unsafe_allow_html=True)
        pref_time = st.text_input("", key="pref_time", placeholder=required_placeholders["pref_time"], label_visibility="collapsed")

        st.markdown('<label>Previous Experience</label>', unsafe_allow_html=True)
        experience = st.text_area("", key="experience", label_visibility="collapsed")

        # Card 3 - Parent & Emergency Contact
        st.markdown(
            """
            <div class="reg-card">
              <div class="reg-card-header">
                <span>Parent &amp; Emergency Contact</span>
                <span></span>
              </div>
              <div class="reg-card-sub">
                Who should we reach out to if needed?
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<label>Parent/Guardian Name</label>', unsafe_allow_html=True)
        parent = st.text_input("", key="parent", label_visibility="collapsed")

        st.markdown('<label>Phone Number</label>', unsafe_allow_html=True)
        phone = st.text_input("", key="phone", label_visibility="collapsed")

        st.markdown('<label>Email Address</label>', unsafe_allow_html=True)
        email = st.text_input("", key="email", label_visibility="collapsed")

        st.markdown('<label>Address</label>', unsafe_allow_html=True)
        address = st.text_area("", key="address", label_visibility="collapsed")

        st.markdown('<label>Emergency Contact Name</label>', unsafe_allow_html=True)
        em_name = st.text_input("", key="em_name", label_visibility="collapsed")

        st.markdown('<label>Relationship</label>', unsafe_allow_html=True)
        em_rel = st.text_input("", key="em_rel", label_visibility="collapsed")

        st.markdown('<label>Emergency Phone</label>', unsafe_allow_html=True)
        em_phone = st.text_input("", key="em_phone", label_visibility="collapsed")

        # Card 4 - Medical & Consent
        st.markdown(
            """
            <div class="reg-card">
              <div class="reg-card-header">
                <span>Medical &amp; Consent</span>
                <span>☑</span>
              </div>
              <div class="reg-card-sub">
                Safety information and media consent.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<label>Allergies / Injuries / Conditions</label>', unsafe_allow_html=True)
        medical = st.text_area("", key="medical", label_visibility="collapsed")

        st.markdown('<label class="required-label">Allow photo/video for promotions?</label>', unsafe_allow_html=True)
        consent = st.radio("", ["", "Yes", "No"], key="consent", label_visibility="collapsed")

        # Terms checkbox inside the form (required)
        st.markdown('<div style="margin-top:8px; margin-bottom:6px;">', unsafe_allow_html=True)
        agree = st.checkbox("I agree to the Terms & Policies", key="agree_terms")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<label class="required-label">Parent/Guardian Signature</label>', unsafe_allow_html=True)
        signature = st.text_input("", key="signature", placeholder=required_placeholders["signature"], label_visibility="collapsed")

        st.markdown('<label class="required-label">Date</label>', unsafe_allow_html=True)
        sig_date = st.date_input("", value=date.today(), key="sig_date", label_visibility="collapsed")

        # Submit button (must be inside the form)
        submitted = st.form_submit_button("Submit Form")

    # Form submission handling
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
        # Terms checkbox required
        if not st.session_state.get("agree_terms", False):
            missing.append("Agreement to Terms & Policies")
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
              const missing = {json.dumps(missing_placeholders)};
              try {{
                missing.forEach(function(ph) {{
                  if (!ph) return;
                  var el = document.querySelector('[placeholder="' + ph + '"]');
                  if (el) {{
                    el.style.borderColor = '#e11d48';
                    el.style.boxShadow = '0 0 0 1px rgba(225,29,72,0.4)';
                  }}
                }});
                var sections = document.querySelectorAll('.section');
                if (sections.length > 0) {{
                  var last = sections[sections.length - 1];
                  last.classList.add('shake');
                  setTimeout(function() {{
                    last.classList.remove('shake');
                  }}, 400);
                }}
              }} catch (e) {{
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
                "agreed_terms": st.session_state.get("agree_terms", False),
                "signature": signature,
                "sig_date": sig_date.isoformat(),
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
      <a class="{admin}" href="/?page=Admin"><span>🔐</span>Admin</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# FOOTER
st.markdown(
    '<div class="footer">@ AARA Dance Studio · Fate · Rockwall · Dallas, TX</div>',
    unsafe_allow_html=True,
)
