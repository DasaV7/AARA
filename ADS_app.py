# app.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from PIL import Image
import io

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="AARA Dance Studio",
    page_icon="💃",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -------------------- THEME / COLORS --------------------
PRIMARY = "#b8860b"      # warm gold
ACCENT = "#111827"       # deep charcoal / near-black
MUTED = "#f7f7fa"        # soft background
CARD = "#ffffff"         # card background
BORDER = "#e6e6e8"

# -------------------- FILES & DATA --------------------
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
REG_FILE = os.path.join(DATA_DIR, "registrations.csv")
VISIT_FILE = os.path.join(DATA_DIR, "site_visits.csv")

# -------------------- LOGO --------------------
# Place your uploaded logo in the repo root and name it "logo.png" (or change LOGO_PATH)
LOGO_PATH = "logo.png"

# -------------------- CSS (minimal iOS-like) --------------------
CSS = f"""
<style>
* {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, "Helvetica Neue", Arial; }}
html, body {{ background: {MUTED}; }}
.block-container {{ padding-top: 1.0rem; padding-bottom: 2rem; max-width: 920px; }}

.header {{
  display:flex;
  align-items:center;
  gap:14px;
  padding:10px 14px;
  background: rgba(255,255,255,0.85);
  border-radius:14px;
  border:1px solid {BORDER};
  box-shadow: 0 6px 18px rgba(17,24,39,0.04);
  margin-bottom: 14px;
}}

.logo-wrap {{
  width:72px;
  height:72px;
  display:flex;
  align-items:center;
  justify-content:center;
  overflow:hidden;
  border-radius:14px;
  background: linear-gradient(180deg, rgba(0,0,0,0.02), rgba(0,0,0,0.01));
}}

.brand {{
  display:flex;
  flex-direction:column;
}}

.brand-title {{
  font-weight:700;
  color:{ACCENT};
  letter-spacing:0.02em;
  font-size:1.05rem;
}}

.brand-sub {{
  font-size:0.78rem;
  color:#6b7280;
}}

.nav {{
  margin-left:auto;
  display:flex;
  gap:8px;
}}

.nav a {{
  text-decoration:none;
  padding:8px 12px;
  border-radius:999px;
  color:{ACCENT};
  border:1px solid transparent;
  font-size:0.9rem;
}}

.nav a.active {{
  background:{PRIMARY};
  color:white;
  border-color:{PRIMARY};
}}

.section {{
  background:{CARD};
  padding:14px;
  border-radius:12px;
  border:1px solid {BORDER};
  margin-bottom:12px;
}}

.title {{
  font-size:1.2rem;
  font-weight:700;
  color:{ACCENT};
  margin-bottom:6px;
}}

.subtitle {{
  font-size:0.88rem;
  color:#6b7280;
  margin-bottom:10px;
}}

.class-card {{
  padding:10px;
  border-radius:10px;
  background:#fbfbfb;
  border:1px solid {BORDER};
  margin-bottom:8px;
}}

.btn {{
  display:inline-block;
  padding:8px 14px;
  border-radius:999px;
  background:{ACCENT};
  color:white;
  text-decoration:none;
  font-weight:600;
  border:none;
}}

.small {{
  font-size:0.85rem;
  color:#374151;
}}

.footer {{
  text-align:center;
  color:#9ca3af;
  font-size:0.78rem;
  margin-top:18px;
}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -------------------- UTILS --------------------
def log_visit():
    row = {"timestamp": datetime.now().isoformat()}
    df = pd.DataFrame([row])
    if os.path.exists(VISIT_FILE):
        df.to_csv(VISIT_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(VISIT_FILE, index=False)

def save_registration(record: dict):
    df = pd.DataFrame([record])
    if os.path.exists(REG_FILE):
        df.to_csv(REG_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(REG_FILE, index=False)

def read_registrations():
    if os.path.exists(REG_FILE):
        return pd.read_csv(REG_FILE)
    return pd.DataFrame()

def read_visits():
    if os.path.exists(VISIT_FILE):
        return pd.read_csv(VISIT_FILE)
    return pd.DataFrame()

# Log every site visit
log_visit()

# -------------------- NAV STATE --------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

# allow query param navigation
params = st.experimental_get_query_params()
if "page" in params:
    st.session_state.page = params["page"][0]

# -------------------- HEADER RENDER --------------------
def render_header():
    cols = st.columns([0.15, 0.75, 0.1])
    with cols[0]:
        if os.path.exists(LOGO_PATH):
            try:
                img = Image.open(LOGO_PATH)
                # scale to fit 72px box while preserving aspect ratio
                st.markdown('<div class="header">', unsafe_allow_html=True)
                st.markdown('<div class="logo-wrap">', unsafe_allow_html=True)
                st.image(img, use_column_width=False, width=72)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception:
                st.markdown('<div class="logo-wrap"></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="logo-wrap"></div>', unsafe_allow_html=True)

    with cols[1]:
        st.markdown(
            f"""
            <div class="brand">
              <div class="brand-title">AARA Dance Studio</div>
              <div class="brand-sub">Fate · Rockwall · Dallas, TX</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with cols[2]:
        page = st.session_state.get("page", "Home")
        home_cls = "active" if page == "Home" else ""
        classes_cls = "active" if page == "Classes" else ""
        reg_cls = "active" if page == "Register" else ""
        admin_cls = "active" if page == "Admin" else ""
        # Admin link visible to everyone but protected on click
        st.markdown(
            f"""
            <div class="nav">
              <a class="{home_cls}" href="/?page=Home">Home</a>
              <a class="{classes_cls}" href="/?page=Classes">Classes</a>
              <a class="{reg_cls}" href="/?page=Register">Register</a>
              <a class="{admin_cls}" href="/?page=Admin">Admin</a>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

render_header()
page = st.session_state.page

# -------------------- PAGES --------------------

# HOME
if page == "Home":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Welcome to AARA Dance Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Where passion meets performance — classes for kids, teens & adults.</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="small">
        <b>Choreography:</b> Mrs. Rekha Mahendran & Mahendran Ramachandran<br/>
        <b>Address:</b> 315 Spirehaven Dr, Rockwall, TX 75087
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('<a class="btn" href="/?page=Classes">View Classes</a> &nbsp; <a class="btn" href="/?page=Register" style="background:'+PRIMARY+'">Register</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# CLASSES
elif page == "Classes":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Programs & Fees</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Simple, transparent pricing — pick a plan that fits your family.</div>', unsafe_allow_html=True)

    st.markdown('<div class="class-card">', unsafe_allow_html=True)
    st.markdown('<b>Tiny Stars (Ages 5–8)</b>', unsafe_allow_html=True)
    st.markdown('<div class="small">Beginner / Intermediate<br><b>Wed & Fri · 6:30pm – 7:30pm</b></div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-top:8px;"><b>Pricing</b>: 4 classes · 1hr · <b>$60 / month</b> · 8 classes · <b>$100 / month</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="class-card">', unsafe_allow_html=True)
    st.markdown('<b>Shining Stars (Ages 9+)</b>', unsafe_allow_html=True)
    st.markdown('<div class="small">Beginner / Intermediate<br><b>Tuesday · 7:00pm – 8:00pm</b></div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-top:8px;"><b>Pricing</b>: 4 classes · 1hr · <b>$60 / month</b> · 8 classes · <b>$100 / month</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="class-card">', unsafe_allow_html=True)
    st.markdown('<b>Dream Chasers (Ladies 18+)</b>', unsafe_allow_html=True)
    st.markdown('<div class="small">Beginner / Intermediate<br><b>Thu 6:30pm – 7:30pm & Sat 10:30am – 11:30am</b></div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-top:8px;"><b>Pricing</b>: 4 classes · 1hr · <b>$50 / month</b> · 8 classes · <b>$80 / month</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top:10px;"><a class="btn" href="/?page=Register">Register Now</a></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# REGISTER
elif page == "Register":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Student Registration Form</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Complete the form below. Records are saved to the studio data folder.</div>', unsafe_allow_html=True)

    with st.form("registration", clear_on_submit=True):
        st.subheader("📌 Student Information")
        student_name = st.text_input("Student Name")
        dob = st.text_input("Date of Birth (Age)")
        gender = st.selectbox("Gender", ["Prefer not to say", "Female", "Male", "Other"])
        school = st.text_input("School Name (optional)")

        st.subheader("👨‍👩‍👧 Parent / Guardian Details")
        parent_name = st.text_input("Parent/Guardian Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        address = st.text_area("Address")

        st.subheader("💃 Class Details")
        enrollment = st.selectbox("Enrollment Type", ["Regular (Monthly – $50/month)", "Drop-in Class ($15 per session)"])
        mode = st.radio("Mode of Class", ["In-Person", "Online Batch"])
        workshops = st.multiselect("Special Workshops (Optional)", ["Ladies Kuthu Workshop – Saturday", "Couple Drop-in Dance Fitness Workshop"])
        preferred_level = st.selectbox("Preferred Class Type", ["Beginner", "Intermediate", "Advanced"])
        dance_style = st.text_input("Dance Style")
        preferred_time = st.text_input("Preferred Days/Time")
        prev_experience = st.text_area("Previous Dance Experience (if any)")

        st.subheader("🚨 Emergency Contact")
        em_name = st.text_input("Emergency Contact Name")
        em_rel = st.text_input("Relationship")
        em_phone = st.text_input("Emergency Phone Number")

        st.subheader("⚕️ Medical Information")
        medical = st.text_area("Allergies / Injuries / Medical Conditions")

        st.subheader("📸 Photo / Video Consent")
        consent = st.radio("I give permission for photos/videos for promotional use", ["Yes", "No"])

        st.subheader("✍️ Parent/Guardian Consent")
        signature = st.text_input("Parent/Guardian Name (acts as signature)")
        sig_date = st.date_input("Date", value=date.today())

        submitted = st.form_submit_button("Submit Registration")

    if submitted:
        record = {
            "timestamp": datetime.now().isoformat(),
            "student_name": student_name,
            "dob": dob,
            "gender": gender,
            "school": school,
            "parent_name": parent_name,
            "phone": phone,
            "email": email,
            "address": address,
            "enrollment": enrollment,
            "mode": mode,
            "workshops": "; ".join(workshops),
            "preferred_level": preferred_level,
            "dance_style": dance_style,
            "preferred_time": preferred_time,
            "prev_experience": prev_experience,
            "em_name": em_name,
            "em_rel": em_rel,
            "em_phone": em_phone,
            "medical": medical,
            "consent": consent,
            "signature": signature,
            "sig_date": sig_date.isoformat()
        }
        save_registration(record)
        st.success("Registration received. Thank you — we will contact you soon.")

# ADMIN (password protected)
elif page == "Admin":
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Admin Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Password protected — studio owner access only.</div>', unsafe_allow_html=True)

    # Admin password: set via environment variable ADMIN_PASS, default fallback below
    ADMIN_PASS = os.environ.get("ADMIN_PASS", "aara-admin-2026")  # change default before deploying

    if not st.session_state.admin_authenticated:
        with st.form("admin_login"):
            pwd = st.text_input("Enter admin password", type="password")
            login = st.form_submit_button("Login")
        if login:
            if pwd == ADMIN_PASS:
                st.session_state.admin_authenticated = True
                st.experimental_rerun()
            else:
                st.error("Incorrect password.")
    else:
        st.success("Admin authenticated.")
        regs = read_registrations()
        visits = read_visits()

        st.markdown("### Registrations")
        if regs.empty:
            st.info("No registrations yet.")
        else:
            st.dataframe(regs.sort_values(by="timestamp", ascending=False).reset_index(drop=True))
            # CSV download
            csv_bytes = regs.to_csv(index=False).encode("utf-8")
            st.download_button("Download registrations CSV", csv_bytes, file_name="registrations.csv", mime="text/csv")

        st.markdown("---")
        st.markdown("### Site Visits")
        if visits.empty:
            st.info("No visits recorded yet.")
        else:
            st.write(f"Total visits recorded: **{len(visits)}**")
            st.dataframe(visits.sort_values(by="timestamp", ascending=False).reset_index(drop=True))
            csv_vis = visits.to_csv(index=False).encode("utf-8")
            st.download_button("Download visits CSV", csv_vis, file_name="site_visits.csv", mime="text/csv")

        st.markdown("---")
        st.markdown("### Admin Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear registrations (delete file)"):
                if os.path.exists(REG_FILE):
                    os.remove(REG_FILE)
                    st.success("Registrations file deleted.")
                else:
                    st.info("No registrations file to delete.")
        with col2:
            if st.button("Clear visits (delete file)"):
                if os.path.exists(VISIT_FILE):
                    os.remove(VISIT_FILE)
                    st.success("Visits file deleted.")
                else:
                    st.info("No visits file to delete.")

        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.admin_authenticated = False
            st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown(f'<div class="footer">© AARA Dance Studio · Fate · Rockwall · Dallas, TX</div>', unsafe_allow_html=True)
