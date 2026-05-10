import streamlit as st
from datetime import time

# ---------- BASIC PAGE CONFIG ---------- #
st.set_page_config(
    page_title="AARA Dance Studio | Fate & Rockwall, TX",
    page_icon="💃",
    layout="wide",
)

# ---------- CUSTOM CSS FOR iOS-STYLE MINIMAL UI ---------- #
IOS_STYLE = """
<style>
/* Global */
* {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
}

body {
    background: radial-gradient(circle at top, #f7f9ff 0, #f3f4f7 40%, #eef0f5 100%);
}

/* Remove default Streamlit padding */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
}

/* Top nav bar */
.navbar {
    position: sticky;
    top: 0;
    z-index: 999;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    background: rgba(248, 250, 255, 0.82);
    border-radius: 18px;
    border: 1px solid rgba(180, 190, 210, 0.35);
    padding: 0.6rem 1.2rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Logo / brand */
.brand-title {
    font-weight: 700;
    letter-spacing: 0.04em;
    font-size: 0.95rem;
    text-transform: uppercase;
    color: #111827;
}

/* Nav links */
.nav-links {
    display: flex;
    gap: 0.75rem;
    font-size: 0.85rem;
}

.nav-pill {
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    border: 1px solid transparent;
    cursor: pointer;
    color: #4b5563;
    background: transparent;
    transition: all 0.18s ease-out;
    white-space: nowrap;
}

.nav-pill:hover {
    background: rgba(148, 163, 184, 0.12);
    border-color: rgba(148, 163, 184, 0.35);
    color: #111827;
}

.nav-pill-active {
    background: #111827;
    color: #f9fafb;
    border-color: #111827;
}

/* Hero card */
.hero-card {
    border-radius: 26px;
    padding: 1.8rem 1.6rem;
    background: linear-gradient(135deg, #0f172a, #111827);
    color: #f9fafb;
    position: relative;
    overflow: hidden;
}

.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(148, 163, 184, 0.5);
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #e5e7eb;
}

.hero-title {
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-top: 0.7rem;
    margin-bottom: 0.4rem;
}

.hero-subtitle {
    font-size: 0.95rem;
    color: #e5e7eb;
    max-width: 460px;
}

.hero-tagline {
    font-size: 0.8rem;
    color: #cbd5f5;
    margin-top: 0.4rem;
}

/* Hero gradient orb */
.hero-orb {
    position: absolute;
    right: -40px;
    top: -40px;
    width: 220px;
    height: 220px;
    background: radial-gradient(circle at 30% 30%, #f97316, #ec4899, #6366f1);
    opacity: 0.7;
    filter: blur(4px);
}

/* Hero stats */
.hero-stats {
    display: flex;
    gap: 1.5rem;
    margin-top: 1.2rem;
    flex-wrap: wrap;
}

.hero-stat {
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
}

.hero-stat-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #9ca3af;
}

.hero-stat-value {
    font-size: 0.95rem;
    font-weight: 600;
}

/* Primary button */
.btn-primary {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    padding: 0.55rem 1.1rem;
    border-radius: 999px;
    border: none;
    background: #f97316;
    color: #111827;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    margin-top: 0.9rem;
    box-shadow: 0 10px 25px rgba(249, 115, 22, 0.35);
    transition: transform 0.12s ease-out, box-shadow 0.12s ease-out, background 0.12s ease-out;
}

.btn-primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 30px rgba(249, 115, 22, 0.45);
    background: #fb923c;
}

/* Secondary ghost button */
.btn-ghost {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    padding: 0.55rem 1.1rem;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.6);
    background: rgba(15, 23, 42, 0.4);
    color: #e5e7eb;
    font-size: 0.85rem;
    cursor: pointer;
    margin-top: 0.9rem;
    margin-left: 0.4rem;
}

/* Section cards */
.section-card {
    border-radius: 22px;
    padding: 1.3rem 1.3rem;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(209, 213, 219, 0.7);
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.06);
    margin-top: 1rem;
}

/* Section titles */
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.2rem;
    color: #111827;
}

.section-subtitle {
    font-size: 0.8rem;
    color: #6b7280;
    margin-bottom: 0.8rem;
}

/* Chips */
.chip {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    background: #f3f4ff;
    color: #4f46e5;
    font-size: 0.75rem;
    margin-right: 0.3rem;
    margin-bottom: 0.3rem;
}

/* Instructor cards */
.instructor-card {
    border-radius: 18px;
    padding: 0.9rem 0.9rem;
    background: #f9fafb;
    border: 1px solid rgba(209, 213, 219, 0.8);
    margin-bottom: 0.7rem;
}

.instructor-name {
    font-weight: 600;
    font-size: 0.95rem;
    color: #111827;
}

.instructor-role {
    font-size: 0.8rem;
    color: #6b7280;
}

/* Class cards */
.class-card {
    border-radius: 18px;
    padding: 0.9rem 0.9rem;
    background: #f9fafb;
    border: 1px solid rgba(209, 213, 219, 0.8);
    margin-bottom: 0.7rem;
}

.class-title {
    font-weight: 600;
    font-size: 0.9rem;
    color: #111827;
}

.class-meta {
    font-size: 0.78rem;
    color: #6b7280;
}

/* Badge */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
    background: #ecfdf3;
    color: #15803d;
    font-size: 0.7rem;
}

/* Testimonials */
.testimonial-card {
    border-radius: 18px;
    padding: 0.9rem 0.9rem;
    background: #f9fafb;
    border: 1px solid rgba(209, 213, 219, 0.8);
    margin-bottom: 0.7rem;
    font-size: 0.85rem;
    color: #374151;
}

.testimonial-name {
    font-weight: 600;
    font-size: 0.8rem;
    margin-top: 0.4rem;
    color: #111827;
}

/* Contact */
.contact-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #4b5563;
    margin-bottom: 0.15rem;
}

.contact-value {
    font-size: 0.85rem;
    color: #111827;
}

/* Footer */
.footer {
    margin-top: 1.5rem;
    font-size: 0.75rem;
    color: #9ca3af;
    text-align: center;
}

/* Mobile tweaks */
@media (max-width: 768px) {
    .hero-title {
        font-size: 1.6rem;
    }
    .hero-card {
        padding: 1.4rem 1.2rem;
    }
    .navbar {
        padding: 0.5rem 0.8rem;
    }
    .nav-links {
        gap: 0.4rem;
        font-size: 0.8rem;
    }
}
</style>
"""

st.markdown(IOS_STYLE, unsafe_allow_html=True)

# ---------- NAVIGATION STATE ---------- #
if "section" not in st.session_state:
    st.session_state.section = "Home"

def set_section(name: str):
    st.session_state.section = name

# ---------- TOP NAVBAR ---------- #
with st.container():
    nav_cols = st.columns([2, 5, 1])
    with nav_cols[0]:
        st.markdown(
            """
            <div class="navbar">
                <div class="brand-title">AARA DANCE STUDIO</div>
            """,
            unsafe_allow_html=True,
        )
    with nav_cols[1]:
        st.markdown(
            """
            <div class="nav-links">
            """,
            unsafe_allow_html=True,
        )
        nav_home, nav_classes, nav_instructors, nav_gallery, nav_contact = st.columns(
            [1, 1, 1.3, 1, 1.2]
        )
        with nav_home:
            if st.button(
                "Home",
                key="nav_home",
                use_container_width=True,
            ):
                set_section("Home")
        with nav_classes:
            if st.button(
                "Classes",
                key="nav_classes",
                use_container_width=True,
            ):
                set_section("Classes")
        with nav_instructors:
            if st.button(
                "Instructors",
                key="nav_instructors",
                use_container_width=True,
            ):
                set_section("Instructors")
        with nav_gallery:
            if st.button(
                "Gallery",
                key="nav_gallery",
                use_container_width=True,
            ):
                set_section("Gallery")
        with nav_contact:
            if st.button(
                "Contact",
                key="nav_contact",
                use_container_width=True,
            ):
                set_section("Contact")
        st.markdown("</div>", unsafe_allow_html=True)
    with nav_cols[2]:
        st.markdown(
            """
            <div style="display:flex;justify-content:flex-end;">
                <span style="font-size:0.75rem;color:#6b7280;">Fate · Rockwall · Dallas</span>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")  # small spacer

# ---------- HERO SECTION (ALWAYS VISIBLE) ---------- #
hero_col1, hero_col2 = st.columns([2, 1.4])

with hero_col1:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-orb"></div>
            <div class="hero-pill">
                <span>Texas · Fate · Dallas · Rockwall</span>
            </div>
            <div class="hero-title">AARA Dance Studio</div>
            <div class="hero-subtitle">
                Classical grace, cinematic energy, and community spirit—crafted in the heart of Texas.
                Learn Bharatanatyam, Bollywood, Semi-Classical and more in an uplifting, family-first space.
            </div>
            <div class="hero-tagline">
                Choreography by Mrs. Rekha Mahendran &amp; Mahendran Ramachandran
            </div>
            <div>
                <button class="btn-primary">Book a Trial Class</button>
                <button class="btn-ghost">View Class Schedule</button>
            </div>
            <div class="hero-stats">
                <div class="hero-stat">
                    <span class="hero-stat-label">Focus</span>
                    <span class="hero-stat-value">Indian Classical · Bollywood · Kids &amp; Adults</span>
                </div>
                <div class="hero-stat">
                    <span class="hero-stat-label">Location</span>
                    <span class="hero-stat-value">315 Spirehaven Dr, Rockwall, TX 75087</span>
                </div>
                <div class="hero-stat">
                    <span class="hero-stat-label">Serving</span>
                    <span class="hero-stat-value">Fate · Rockwall · Dallas Metro</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_col2:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Quick Info</div>
            <div class="section-subtitle">Perfect for families, beginners, and performance-focused dancers.</div>
            <div class="chip">Kids (4+)</div>
            <div class="chip">Teens</div>
            <div class="chip">Adults</div>
            <div class="chip">Performance Teams</div>
            <br/><br/>
            <div class="contact-label">Studio Address</div>
            <div class="contact-value">315 Spirehaven Dr<br/>Rockwall, TX 75087</div>
            <br/>
            <div class="contact-label">Service Areas</div>
            <div class="contact-value">Fate · Rockwall · Royse City · Dallas Metro</div>
            <br/>
            <div class="contact-label">Typical Hours</div>
            <div class="contact-value">Weekday evenings &amp; weekend batches</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# ---------- SECTION RENDERING ---------- #
section = st.session_state.section

# ----- HOME SECTION ----- #
if section == "Home":
    about_col1, about_col2 = st.columns([1.6, 1.4])

    with about_col1:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">About AARA Dance Studio</div>
                <div class="section-subtitle">
                    Rooted in Indian classical traditions and inspired by contemporary Bollywood, AARA is a warm,
                    inclusive studio where every student is seen, guided, and celebrated.
                </div>
                <p style="font-size:0.9rem;color:#374151;">
                    At AARA Dance Studio, we believe dance is more than choreography—it is culture, confidence,
                    and community. From foundational Bharatanatyam to expressive Semi-Classical and high-energy
                    Bollywood, our programs are thoughtfully designed for kids, teens, and adults.
                </p>
                <p style="font-size:0.9rem;color:#374151;">
                    Whether you are stepping into a studio for the first time or returning after years,
                    our small-batch classes, performance opportunities, and personalized attention help you grow
                    at your own pace while having fun.
                </p>
                <p style="font-size:0.9rem;color:#374151;">
                    AARA proudly serves families in Fate, Rockwall, Royse City, and the greater Dallas area,
                    bringing the joy of Indian dance closer to home.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with about_col2:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Why families love AARA</div>
                <ul style="padding-left:1.1rem;font-size:0.88rem;color:#374151;margin-top:0.4rem;">
                    <li>Structured curriculum with clear progression for each age group</li>
                    <li>Performance-focused training for recitals, competitions, and cultural events</li>
                    <li>Strong emphasis on posture, expressions, rhythm, and stage presence</li>
                    <li>Safe, nurturing environment with patient, detail-oriented teaching</li>
                    <li>Opportunities to connect with Indian culture through music, stories, and movement</li>
                </ul>
                <br/>
                <span class="badge">Now enrolling · Limited batch sizes</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Programs at a glance</div>
            <div class="section-subtitle">Curated tracks for every age and experience level.</div>
            <div style="display:flex;flex-wrap:wrap;gap:0.8rem;font-size:0.85rem;color:#374151;">
                <div style="flex:1;min-width:180px;">
                    <div class="class-card">
                        <div class="class-title">Little Stars (Ages 4–7)</div>
                        <div class="class-meta">Foundations · Rhythm · Fun movement</div>
                        <p style="font-size:0.8rem;margin-top:0.4rem;">
                            Gentle introduction to Indian dance through stories, music, and playful choreography.
                        </p>
                    </div>
                </div>
                <div style="flex:1;min-width:180px;">
                    <div class="class-card">
                        <div class="class-title">Junior &amp; Teen (Ages 8–15)</div>
                        <div class="class-meta">Technique · Expressions · Stage confidence</div>
                        <p style="font-size:0.8rem;margin-top:0.4rem;">
                            Strong focus on technique, expressions, and performance-ready routines.
                        </p>
                    </div>
                </div>
                <div style="flex:1;min-width:180px;">
                    <div class="class-card">
                        <div class="class-title">Adults &amp; Fitness</div>
                        <div class="class-meta">Bollywood · Semi-Classical · Conditioning</div>
                        <p style="font-size:0.8rem;margin-top:0.4rem;">
                            Feel-good choreography, musicality, and movement for adults of all levels.
                        </p>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----- CLASSES SECTION ----- #
elif section == "Classes":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Class structure &amp; schedule</div>
            <div class="section-subtitle">
                Sample weekly structure. Exact timings may vary by batch and season.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="section-card">
                <div class="class-title">Kids · Little Stars (4–7)</div>
                <div class="class-meta">Foundations · Coordination · Joyful movement</div>
                <ul style="padding-left:1.1rem;font-size:0.85rem;color:#374151;margin-top:0.4rem;">
                    <li>Warm-up, stretches, and rhythm games</li>
                    <li>Basic steps inspired by Bharatanatyam &amp; Bollywood</li>
                    <li>Short, age-appropriate choreographies</li>
                    <li>Focus on listening, memory, and group work</li>
                </ul>
                <br/>
                <span class="badge">Recommended: 1–2 classes per week</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-card">
                <div class="class-title">Junior &amp; Teen (8–15)</div>
                <div class="class-meta">Technique · Expressions · Performance</div>
                <ul style="padding-left:1.1rem;font-size:0.85rem;color:#374151;margin-top:0.4rem;">
                    <li>Structured warm-up and conditioning</li>
                    <li>Technique drills for lines, footwork, and expressions</li>
                    <li>Classical, Semi-Classical &amp; Bollywood choreographies</li>
                    <li>Stage presence, formations, and performance polish</li>
                </ul>
                <br/>
                <span class="badge">Performance &amp; competition opportunities</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="section-card">
                <div class="class-title">Adults</div>
                <div class="class-meta">Bollywood · Semi-Classical · Fitness</div>
                <ul style="padding-left:1.1rem;font-size:0.85rem;color:#374151;margin-top:0.4rem;">
                    <li>Beginner-friendly choreography with options to level up</li>
                    <li>Focus on musicality, grace, and stamina</li>
                    <li>Great for parents, working professionals, and dance returners</li>
                    <li>No prior experience required</li>
                </ul>
                <br/>
                <span class="badge">Trial classes available</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-card">
                <div class="class-title">Private &amp; Event Choreography</div>
                <div class="class-meta">Weddings · Sangeet · Competitions · School shows</div>
                <ul style="padding-left:1.1rem;font-size:0.85rem;color:#374151;margin-top:0.4rem;">
                    <li>Custom choreography for couples, families, and groups</li>
                    <li>Song selection guidance and medley creation</li>
                    <li>Flexible scheduling for busy families</li>
                    <li>On-site or studio-based rehearsals (as available)</li>
                </ul>
                <br/>
                <span class="badge">By appointment only</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Sample weekly timings</div>
            <div class="section-subtitle">Indicative only – final schedule shared upon enrollment.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Simple interactive schedule mock using Streamlit widgets
    st.write("")
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("**Weekday Evenings**")
        st.write("Kids (4–7):", time(17, 30), "–", time(18, 15))
        st.write("Junior/Teen:", time(18, 30), "–", time(19, 30))

    with col_b:
        st.markdown("**Weekends**")
        st.write("Kids (4–7):", time(10, 0), "–", time(10, 45))
        st.write("Junior/Teen:", time(11, 0), "–", time(12, 0))
        st.write("Adults:", time(16, 0), "–", time(17, 0))

    with col_c:
        st.markdown("**Private Sessions**")
        st.write("By appointment on select weekday evenings and weekends.")
        st.write("Use the contact form below to request a slot.")

# ----- INSTRUCTORS SECTION ----- #
elif section == "Instructors":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Meet your choreographers</div>
            <div class="section-subtitle">
                AARA Dance Studio is artistically led by Mrs. Rekha Mahendran and Mahendran Ramachandran.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    i1, i2 = st.columns(2)

    with i1:
        st.markdown(
            """
            <div class="instructor-card">
                <div class="instructor-name">Mrs. Rekha Mahendran</div>
                <div class="instructor-role">Founder · Artistic Director · Choreographer</div>
                <p style="font-size:0.85rem;color:#374151;margin-top:0.4rem;">
                    Rekha brings a deep love for Indian classical and cinematic dance, blending strong technique
                    with expressive storytelling. Her teaching style is patient, structured, and nurturing—perfect
                    for young children and serious learners alike.
                </p>
                <p style="font-size:0.85rem;color:#374151;">
                    She focuses on building strong foundations in posture, rhythm, and expressions while ensuring
                    every student feels confident and supported on their dance journey.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with i2:
        st.markdown(
            """
            <div class="instructor-card">
                <div class="instructor-name">Mahendran Ramachandran</div>
                <div class="instructor-role">Co-Founder · Choreographer · Performance Coach</div>
                <p style="font-size:0.85rem;color:#374151;margin-top:0.4rem;">
                    Mahendran brings energy, precision, and stagecraft to AARA’s performances. With a keen eye
                    for formations, musicality, and crowd-pleasing choreography, he helps students shine on stage
                    at cultural events, recitals, and competitions.
                </p>
                <p style="font-size:0.85rem;color:#374151;">
                    His sessions are dynamic and motivating, encouraging dancers to push their boundaries while
                    still having fun and enjoying the music.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Teaching philosophy</div>
            <div class="section-subtitle">Grace, discipline, and joy—balanced in every class.</div>
            <ul style="padding-left:1.1rem;font-size:0.88rem;color:#374151;margin-top:0.4rem;">
                <li>Every student is unique—progress is guided, not rushed.</li>
                <li>Strong basics first: posture, rhythm, and expressions before complex choreography.</li>
                <li>Encouraging environment where questions, mistakes, and retries are welcome.</li>
                <li>Focus on cultural connection and respect for the art form.</li>
                <li>Performance opportunities that build confidence and lifelong memories.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----- GALLERY SECTION ----- #
elif section == "Gallery":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Gallery &amp; moments</div>
            <div class="section-subtitle">
                A glimpse into the energy, colors, and smiles at AARA Dance Studio.
                (Replace placeholders with your photos later.)
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    g1, g2, g3 = st.columns(3)

    for col, label in zip(
        [g1, g2, g3],
        ["Studio rehearsals", "Stage performances", "Community events"],
    ):
        with col:
            st.markdown(
                f"""
                <div class="section-card" style="text-align:center;">
                    <div style="
                        width:100%;
                        border-radius:18px;
                        background:linear-gradient(135deg,#f97316,#ec4899,#6366f1);
                        height:160px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        color:#f9fafb;
                        font-size:0.9rem;
                        font-weight:500;
                        ">
                        {label}<br/>(Photo placeholder)
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Video &amp; social</div>
            <div class="section-subtitle">
                Add your Instagram, YouTube, or Facebook links here when ready.
            </div>
            <p style="font-size:0.85rem;color:#374151;">
                Share reels, performance clips, behind-the-scenes rehearsals, and student spotlights to give
                families a feel for the studio’s vibe and teaching style.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----- CONTACT SECTION ----- #
elif section == "Contact":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Visit &amp; connect</div>
            <div class="section-subtitle">
                Located in Rockwall, serving families across Fate, Rockwall, Royse City, and the Dallas metro.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    contact_col1, contact_col2 = st.columns([1.4, 1.6])

    with contact_col1:
        st.markdown(
            """
            <div class="section-card">
                <div class="contact-label">Studio Address</div>
                <div class="contact-value">
                    AARA Dance Studio<br/>
                    315 Spirehaven Dr<br/>
                    Rockwall, TX 75087
                </div>
                <br/>
                <div class="contact-label">Service Areas</div>
                <div class="contact-value">
                    Fate · Rockwall · Royse City · Dallas Metro
                </div>
                <br/>
                <div class="contact-label">Contact</div>
                <div class="contact-value">
                    (Add phone / email here)<br/>
                    Trial classes &amp; enrollment by prior booking.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Google Maps</div>
                <div class="section-subtitle">Embed your live map once available.</div>
                <p style="font-size:0.8rem;color:#374151;">
                    For now, families can search “315 Spirehaven Dr, Rockwall, TX 75087” on Google Maps
                    to navigate to the studio.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with contact_col2:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Inquiry form</div>
                <div class="section-subtitle">
                    Collect leads directly from the website. (This is a simple demo form.)
                </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("inquiry_form"):
            name = st.text_input("Parent / Student Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            dancer_age = st.text_input("Dancer age(s)")
            interest = st.multiselect(
                "Interested in",
                [
                    "Kids classes (4–7)",
                    "Junior / Teen classes (8–15)",
                    "Adult classes",
                    "Private / Event choreography",
                    "Not sure yet",
                ],
            )
            message = st.text_area("Tell us a little about your goals")
            submitted = st.form_submit_button("Submit inquiry")

        if submitted:
            st.success(
                "Thank you for reaching out! We’ve received your inquiry. "
                "AARA Dance Studio will get back to you shortly."
            )

        st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ---------- #
st.markdown(
    """
    <div class="footer">
        © AARA Dance Studio · Fate · Rockwall · Dallas, TX · Designed with a minimalist iOS-inspired aesthetic.
    </div>
    """,
    unsafe_allow_html=True,
)
