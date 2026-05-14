# ADS_app.py — B02
# Baseline: B00 + B01 fixes + B02 improvements
# New in B02:
# - Cinematic zoom-in slideshow
# - Fully themed form fields (dropdowns, radios, selects)
# - Larger centered circular logo
# - 60px top padding to avoid Streamlit banner overlap
# - Adjusted WhatsApp button + header spacing

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
# CSS — B02 (slideshow zoom, form fixes, logo spacing)
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
  max-width: 900px;
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
  max-width: 820px;
  height: 320px;
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
  5% {{ opacity: 1; transform: scale(1.05); }}
  20% {{ opacity: 1; transform: scale(1.1); }}
  25% {{ opacity: 0; transform: scale(1.1); }}
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
# HEADER — Larger centered circular logo
# ---------------------------------------------------------
def render_header():
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)

    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=200)

    st.markdown(
        f"""
        <div style="text-align:center; margin-top:4px;">
            <div style="font-size:2.0rem; font-weight:700; margin-top:4px; color:{GOLD}; font-family:'Playfair Display', serif;">
                AARA Dance Studio
            </div>
            <div style="font-size:0.95rem; color:{GOLD_SOFT};">
                Where Passion Meets Performance · Fate · Rockwall · Dallas, TX
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

render_header()

# ---------------------------------------------------------
# WHATSAPP BUTTON (moved down)
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
    qr_img = qrcode.make(reg_url)
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)
    st.image(buf, caption="Scan to open registration page", width=140)

# ---------------------------------------------------------
# HOME PAGE — Cinematic slideshow
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
            <div style="font-size:2.3rem; font-weight:800; color:{GOLD}; font-family:'Playfair Display', serif;">
                Dance. Express. Shine.
            </div>
            <div style="font-size:1.05rem; color:{GOLD_SOFT}; max-width:540px;">
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

    images = sorted(glob.glob("slide*.jpg")) + sorted(glob.glob("slide*.jpeg")) + sorted(glob.glob("slide*.png"))
    images = images[:5]

    if images:
        slides_html = []
        for idx, path in enumerate(images):
            delay = idx * 6
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
        st.info("Upload slide1.jpeg, slide2.jpeg, slide3.jpeg (etc.) in the root directory for a slideshow.")

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

    st.markdown
