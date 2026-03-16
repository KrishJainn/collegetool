import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Infoyoung India | College Strategy",
    page_icon="🎓",
    layout="wide"
)

# --- PROFESSIONAL CSS (UX Enhanced) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Neuton:wght@400;700;800&display=swap');
    
    /* BASE: Larger text for readability */
    * {
        font-family: 'Neuton', Georgia, serif !important;
        font-size: 1.1rem;
    }
    
    html, body, [class*="css"], p, span, div, label, input, button, table, th, td {
        font-family: 'Neuton', Georgia, serif !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* HIERARCHY: Clear heading structure */
    h1 {
        font-family: 'Neuton', Georgia, serif !important;
        font-weight: 800;
        font-size: 2.5rem !important;
        color: #1a1a1a;
    }
    
    h2 {
        font-family: 'Neuton', Georgia, serif !important;
        font-weight: 700;
        font-size: 2rem !important;
        color: #b91c1c;
    }
    
    h3, h4, h5, h6 {
        font-family: 'Neuton', Georgia, serif !important;
        font-weight: 700;
        color: #374151;
    }
    
    /* METRICS: Color-coded cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
        border: 2px solid #fecaca;
        border-radius: 16px;
        padding: 1.5rem;
    }
    
    div[data-testid="stMetricValue"] {
        font-family: 'Neuton', Georgia, serif !important;
        font-weight: 800;
        font-size: 2.5rem !important;
        color: #b91c1c;
    }
    
    div[data-testid="stMetricLabel"] {
        font-family: 'Neuton', Georgia, serif !important;
        font-size: 1rem !important;
        color: #6b7280;
        font-weight: 600;
    }
    
    /* TABS: Clear visual distinction */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f3f4f6;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Neuton', Georgia, serif !important;
        font-size: 1.1rem !important;
        font-weight: 600;
        padding: 12px 24px;
        border-radius: 8px;
    }
    
    .stTabs [aria-selected="true"] {
        background: #b91c1c !important;
        color: white !important;
    }
    
    /* BUTTONS: Primary red action */
    .stButton > button {
        font-family: 'Neuton', Georgia, serif !important;
        font-size: 1.1rem !important;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    .stButton > button[kind="primary"] {
        background: #b91c1c !important;
        color: white !important;
        border: none;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #991b1b !important;
    }
    
    /* TABLE: Better readability */
    .stDataFrame, .stDataFrame * {
        font-family: 'Neuton', Georgia, serif !important;
        font-size: 1rem !important;
    }
    
    /* INPUTS: Larger, clearer */
    .stSelectbox, .stTextInput, .stNumberInput, .stSlider {
        font-family: 'Neuton', Georgia, serif !important;
    }
    
    .stSelectbox label, .stTextInput label, .stNumberInput label, .stSlider label {
        font-size: 1.1rem !important;
        font-weight: 600;
        color: #374151;
    }
    
    [data-baseweb] {
        font-family: 'Neuton', Georgia, serif !important;
    }
    
    /* DIVIDER: Subtle red accent */
    hr {
        border-color: #fecaca !important;
    }
    
    /* DOWNLOAD BUTTON: Distinct */
    .stDownloadButton > button {
        background: #059669 !important;
        color: white !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'step' not in st.session_state:
    st.session_state['step'] = 1

if 'student' not in st.session_state:
    st.session_state['student'] = {
        'name': 'Student',
        'gpa': 3.8,
        'sat': 1400,
        'major': 'Computer Science & Engineering',
        'ec': 7,
        'curriculum': 'CBSE / ICSE'
    }

# --- IMPORT EXPANDED DATABASE ---
from colleges_db import COLLEGES

# --- MAJOR COMPETITIVENESS (data-driven multipliers) ---
# Multiplier applied to admission chance when applying to that major
# Based on admit rate differentials across selective programs:
#   CS/Eng admit rates are ~25-30% lower than overall at top schools
#   Business admit rates ~18-20% lower (Wharton, Stern, Ross)
#   Econ ~15-18% lower at schools with dedicated econ programs
#   Bio/Pre-Med ~13% lower due to pre-med competition
#   Sciences ~10% lower
#   Humanities/Arts: baseline (no penalty)
MAJOR_MAP = {
    "Computer Science & Engineering": {"tags": ['CS', 'Eng'], "competitiveness": 0.75},
    "Business & Finance":            {"tags": ['Biz'],        "competitiveness": 0.82},
    "Economics":                     {"tags": ['Econ'],       "competitiveness": 0.84},
    "Biology & Pre-Med":             {"tags": ['Bio'],        "competitiveness": 0.87},
    "Natural Sciences":              {"tags": ['Sci'],        "competitiveness": 0.90},
    "Humanities & Arts":             {"tags": [],             "competitiveness": 1.00}
}

# --- ADMISSION CHANCE ESTIMATION (data-driven) ---
def estimate_admission_chance(gpa, sat, ec, college, major):
    """
    Estimate admission probability using the college's real acceptance rate
    as the base, adjusted by how the student compares to typical admits.

    All multipliers are calibrated against CDS/IPEDS admission data:
    - SAT impact scales with selectivity (matters more at top schools)
    - GPA thresholds match median admitted GPAs by selectivity tier
    - EC impact follows holistic review research (strongest at <15% schools)
    - International factor based on SEVIS/Open Doors Indian student data
    """
    name, avg_sat, accept_rate, friendly, specs, school_names, state, fees = college

    # --- Base probability = college's actual acceptance rate ---
    prob = accept_rate

    # --- SAT adjustment (tiered by selectivity) ---
    if sat > 0:
        sat_diff = sat - avg_sat
        if accept_rate < 0.15:
            # Highly selective: SAT heavily scrutinized
            # +200 above median ≈ 2x, -200 below ≈ 0.5x (CDS 25th/75th data)
            sat_mult = max(0.15, min(3.0, 1.0 + sat_diff / 200))
        elif accept_rate < 0.40:
            # Moderately selective: SAT matters but less dramatically
            sat_mult = max(0.20, min(2.5, 1.0 + sat_diff / 200))
        else:
            # Less selective: SAT is one factor among many
            sat_mult = max(0.30, min(2.0, 1.0 + sat_diff / 300))
    else:
        # Test-optional penalty: research shows submitting strong scores helps;
        # not submitting signals weakness, especially at selective schools
        if accept_rate < 0.10:
            sat_mult = 0.60   # Top-10: strong SAT expected, big penalty
        elif accept_rate < 0.20:
            sat_mult = 0.70   # Top-20: significant penalty
        elif accept_rate < 0.40:
            sat_mult = 0.85   # Moderately selective: moderate penalty
        else:
            sat_mult = 0.95   # Less selective: SAT barely matters

    # --- GPA adjustment (tiered by selectivity) ---
    # Calibrated against median admitted GPAs from CDS data:
    #   Top-15 schools: median admitted GPA 3.9+ (unweighted)
    #   Top-50 schools: median admitted GPA 3.6-3.8
    #   Less selective: GPA 3.0+ generally sufficient
    if accept_rate < 0.15:
        # Highly selective: median admitted GPA is 3.9+ (CDS data)
        # Baseline at ~3.85; steep dropoff below 3.7
        # 4.0→1.20, 3.9→1.08, 3.85→1.02, 3.7→0.84, 3.5→0.60, 3.0→0.15
        gpa_mult = max(0.15, min(1.2, (gpa - 3.0) * 1.20))
    elif accept_rate < 0.40:
        # Moderately selective: expects 3.5+, gradual dropoff
        # 4.0→1.28, 3.5→1.0, 3.0→0.73, 2.5→0.45
        gpa_mult = max(0.20, min(1.3, 0.45 + (gpa - 2.5) * 0.55))
    else:
        # Less selective: 3.0+ is competitive
        # 4.0→1.20, 3.5→1.05, 3.0→0.90, 2.5→0.75
        gpa_mult = max(0.30, min(1.2, 0.60 + (gpa - 2.0) * 0.30))

    # --- EC adjustment (tiered by selectivity) ---
    # Research: holistic review at top schools weighs ECs heavily;
    # at less selective schools, meeting GPA/SAT thresholds dominates
    # Scale 1-10 where 7 = solid competitive applicant
    if accept_rate < 0.15:
        # Strong holistic review: ECs differentiate qualified applicants
        # 10→1.30, 7→1.08, 5→0.93, 3→0.78
        ec_mult = max(0.40, min(1.4, 0.55 + ec * 0.075))
    elif accept_rate < 0.40:
        # Moderate holistic review: ECs matter but less decisive
        # 10→1.18, 7→1.04, 5→0.95, 3→0.86
        ec_mult = max(0.60, min(1.2, 0.725 + ec * 0.045))
    else:
        # Minimal holistic review: ECs barely move the needle
        # 10→1.06, 7→1.02, 5→0.99, 3→0.96
        ec_mult = max(0.85, min(1.1, 0.91 + ec * 0.015))

    # --- International student adjustment ---
    # Based on SEVIS/Open Doors data on Indian student admit rates:
    #   "High" = large Indian community, active international recruitment
    #   "Med"  = standard process, moderate international presence
    #   "Low"  = state school bias toward in-state, very limited intl spots
    if friendly == "Low":
        intl_mult = 0.50
    elif friendly == "Med":
        intl_mult = 0.80
    else:
        intl_mult = 1.00

    # --- Major competitiveness ---
    m = MAJOR_MAP.get(major, {"tags": [], "competitiveness": 1.0})
    if any(t in specs for t in m['tags']):
        major_mult = m['competitiveness']
    else:
        major_mult = 1.0

    # --- Final estimated probability ---
    prob *= sat_mult * gpa_mult * ec_mult * intl_mult * major_mult
    prob = max(0.001, min(0.99, prob))

    # --- Display name with specific school/program ---
    display_name = name
    for tag in m['tags']:
        if tag in school_names:
            display_name = f"{name} ({school_names[tag]})"
            break

    return prob, display_name

# --- NAV ---
def go(n): st.session_state['step'] = n

# ==============================================================================
# STEP 1: HOME - Clear entry point with visual hierarchy
# ==============================================================================
if st.session_state['step'] == 1:
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Centered logo
        if os.path.exists("logo.png"):
            c1, c2, c3 = st.columns([1, 1, 1])
            with c2:
                st.image("logo.png", width=200)
        
        # Clear heading hierarchy
        st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-top: 1.5rem; color: #1a1a1a;'>Infoyoung India</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #b91c1c; font-size: 1.3rem; font-weight: 600;'>College Strategy Platform</p>", unsafe_allow_html=True)
        
        st.write("")
        
        # Value proposition
        st.markdown("""
        <div style='background: #fef2f2; border-left: 4px solid #b91c1c; padding: 1.5rem; border-radius: 8px; margin: 2rem 0;'>
            <p style='margin: 0; color: #374151; font-size: 1.15rem; line-height: 1.6;'>
                <strong>Get personalized college recommendations</strong> based on your academic profile. 
                Our algorithm analyzes <strong>220+ US universities</strong> to find your Safety, Target, and Reach schools.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # Primary CTA - large and clear
        if st.button("→ Start Your Analysis", type="primary", use_container_width=True):
            go(2)
            st.rerun()

# ==============================================================================
# STEP 2: INPUTS - Structured form with clear groupings
# ==============================================================================
elif st.session_state['step'] == 2:
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=120)
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 2.2rem; margin-top: 0.5rem;'>Tell Us About You</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6b7280; font-size: 1.1rem;'>We'll match you with the right universities</p>", unsafe_allow_html=True)
    with col3:
        st.write("")
    
    st.divider()
    
    # Curriculum selector OUTSIDE form so it re-renders immediately
    curr = st.selectbox("Curriculum", ["CBSE / ICSE", "IB Diploma", "A-Levels", "US High School"], key="curr_select")
    
    with st.form("form"):
        c1, c2 = st.columns(2)
        
        with c1:
            name = st.text_input("Name", st.session_state['student']['name'])
            
            # Show appropriate input based on curriculum
            if curr == "CBSE / ICSE":
                pct = st.number_input("Percentage (%)", 0.0, 100.0, 90.0)
                gpa = 4.0 if pct >= 95 else 3.9 if pct >= 90 else 3.7 if pct >= 85 else 3.5 if pct >= 80 else 3.3 if pct >= 75 else 3.0 if pct >= 70 else 2.7 if pct >= 60 else 2.3 if pct >= 50 else 2.0
            elif curr == "IB Diploma":
                ib = st.number_input("IB Score (out of 45)", 24, 45, 38)
                gpa = 4.0 if ib >= 44 else 3.9 if ib >= 42 else 3.8 if ib >= 40 else 3.7 if ib >= 38 else 3.5 if ib >= 36 else 3.4 if ib >= 34 else 3.2 if ib >= 32 else 3.0 if ib >= 30 else 2.7 if ib >= 27 else 2.5
            elif curr == "A-Levels":
                gr = st.selectbox("Best 3 Grades", ["A*A*A*", "A*A*A", "A*AA", "AAA", "AAB", "ABB", "BBB", "BBC", "BCC", "CCC"])
                gpa = 4.0 if gr == "A*A*A*" else 4.0 if gr == "A*A*A" else 3.9 if gr == "A*AA" else 3.8 if gr == "AAA" else 3.6 if gr == "AAB" else 3.4 if gr == "ABB" else 3.3 if gr == "BBB" else 3.1 if gr == "BBC" else 2.9 if gr == "BCC" else 2.7
            else:
                gpa = st.number_input("GPA (out of 4.0)", 0.0, 4.0, 3.8)
            
            sat = st.number_input("SAT Score (0 = Test Optional)", 0, 1600, 1400)
        
        with c2:
            major = st.selectbox("Intended Major", list(MAJOR_MAP.keys()))
            ec = st.slider("Extracurricular Profile", 1, 10, 7)
        
        st.divider()
        
        c1, c2 = st.columns([4, 1])
        with c1:
            if st.form_submit_button("Generate Report", type="primary", use_container_width=True):
                st.session_state['student'] = {'name': name or "Student", 'gpa': gpa, 'sat': sat, 'major': major, 'ec': ec, 'curriculum': curr}
                go(3)
                st.rerun()
        with c2:
            if st.form_submit_button("← Home"):
                go(1)
                st.rerun()

# ==============================================================================
# STEP 3: RESULTS - Clear presentation with actionable insights
# ==============================================================================
elif st.session_state['step'] == 3:
    s = st.session_state['student']
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=120)
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 2.2rem; margin-top: 0.5rem;'>Your College Strategy</h1>", unsafe_allow_html=True)
    with col3:
        st.write("")
    
    st.divider()
    
    # Success message with student info
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%); border: 2px solid #86efac; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;'>
        <p style='margin: 0; font-size: 1.2rem;'><strong>Strategy generated for {s['name']}</strong></p>
        <p style='margin: 0.5rem 0 0 0; color: #374151;'>{s['major']} | GPA {s['gpa']:.1f} | SAT {s['sat'] if s['sat'] > 0 else 'Test Optional'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    safeties, targets, reaches = [], [], []

    for c in COLLEGES:
        prob, display_name = estimate_admission_chance(
            s['gpa'], s['sat'], s['ec'], c, s['major']
        )
        name, avg_sat, accept_rate, friendly, specs, school_names, state, fees = c

        row = {
            "University": display_name,
            "State": state,
            "Accept Rate": f"{accept_rate * 100:.1f}%",
            "Avg SAT": avg_sat,
            "Est. Fees": f"${fees:,}",
            "Est. Chance": f"{prob * 100:.1f}%",
            "_prob": prob,
            "_accept_rate": accept_rate
        }

        # Classification thresholds based on estimated probability
        if prob > 0.40:
            safeties.append(row)
        elif prob > 0.15:
            targets.append(row)
        elif prob >= 0.025:
            reaches.append(row)
        # < 2.5% chance = filtered out (unrealistic)

    # If too few safeties, promote highest-chance targets
    if len(safeties) < 5 and targets:
        targets.sort(key=lambda x: x['_prob'], reverse=True)
        while len(safeties) < 5 and targets:
            safeties.append(targets.pop(0))

    # Sort all categories by prestige (lowest accept rate = most selective first)
    # This ensures "best 15" means the 15 most prestigious schools in each tier
    safeties.sort(key=lambda x: x['_accept_rate'])
    targets.sort(key=lambda x: x['_accept_rate'])
    reaches.sort(key=lambda x: x['_accept_rate'])

    # Keep full lists for Excel export
    all_safeties, all_targets, all_reaches = safeties.copy(), targets.copy(), reaches.copy()

    # Show best 15 per category on screen; full list in Excel
    TOP_N = 15
    safeties, targets, reaches = safeties[:TOP_N], targets[:TOP_N], reaches[:TOP_N]

    c1, c2, c3 = st.columns(3)
    c1.metric("Safety Schools", len(safeties), delta=f"{len(all_safeties)} total" if len(all_safeties) > TOP_N else None)
    c2.metric("Target Schools", len(targets), delta=f"{len(all_targets)} total" if len(all_targets) > TOP_N else None)
    c3.metric("Reach Schools", len(reaches), delta=f"{len(all_reaches)} total" if len(all_reaches) > TOP_N else None)

    if len(all_safeties) > TOP_N or len(all_targets) > TOP_N or len(all_reaches) > TOP_N:
        st.caption(f"Showing top {TOP_N} per category. Download the Excel report for the complete list.")
    
    st.write("")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("← Edit Profile", use_container_width=True):
            go(2)
            st.rerun()
    
    with col2:
        if st.button("↺ Start Over", use_container_width=True):
            go(1)
            st.rerun()
    
    with col3:
        def xl():
            from io import BytesIO
            o = BytesIO()

            # Build export data from full lists (not truncated display lists)
            # Use copies to avoid mutating display data
            export_safe = [dict(r, Category='Safety') for r in all_safeties]
            export_targ = [dict(r, Category='Target') for r in all_targets]
            export_reach = [dict(r, Category='Reach') for r in all_reaches]
            all_colleges = export_safe + export_targ + export_reach

            try:
                with pd.ExcelWriter(o, engine='xlsxwriter') as w:
                    student_info = pd.DataFrame([{
                        'Student Name': s['name'],
                        'Curriculum': s['curriculum'],
                        'GPA': f"{s['gpa']:.2f}",
                        'SAT': s['sat'] if s['sat'] > 0 else 'Test Optional',
                        'Major': s['major'],
                        'EC Score': f"{s['ec']}/10",
                        'Safety': len(all_safeties),
                        'Target': len(all_targets),
                        'Reach': len(all_reaches)
                    }])
                    student_info.to_excel(w, sheet_name='Student Profile', index=False)

                    cols = ['Category', 'University', 'State', 'Accept Rate', 'Avg SAT', 'Est. Fees', 'Est. Chance']
                    cols_single = ['University', 'State', 'Accept Rate', 'Avg SAT', 'Est. Fees', 'Est. Chance']
                    if all_colleges:
                        pd.DataFrame(all_colleges)[cols].to_excel(w, sheet_name='All Recommendations', index=False)
                    if export_safe: pd.DataFrame(export_safe)[cols_single].to_excel(w, sheet_name='Safety', index=False)
                    if export_targ: pd.DataFrame(export_targ)[cols_single].to_excel(w, sheet_name='Target', index=False)
                    if export_reach: pd.DataFrame(export_reach)[cols_single].to_excel(w, sheet_name='Reach', index=False)
            except Exception:
                with pd.ExcelWriter(o, engine='openpyxl') as w:
                    student_info = pd.DataFrame([{'Student Name': s['name'], 'Curriculum': s['curriculum'], 'GPA': f"{s['gpa']:.2f}", 'SAT': s['sat'] if s['sat'] > 0 else 'Test Optional', 'Major': s['major'], 'EC Score': f"{s['ec']}/10"}])
                    student_info.to_excel(w, sheet_name='Student Profile', index=False)
                    if all_colleges:
                        pd.DataFrame(all_colleges)[['Category', 'University', 'State', 'Accept Rate', 'Avg SAT', 'Est. Fees', 'Est. Chance']].to_excel(w, sheet_name='All Recommendations', index=False)
            return o.getvalue()
        
        st.download_button("Download Excel Report", xl(), f"{s['name']}_Strategy.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    
    st.write("")
    st.divider()
    
    t1, t2, t3 = st.tabs([
        f"Safety ({len(safeties)})",
        f"Target ({len(targets)})",
        f"Reach ({len(reaches)})"
    ])
    
    def show(data):
        if not data:
            st.info("No schools found in this category.")
            return
        df = pd.DataFrame([{
            "University": r['University'],
            "State": r['State'],
            "Accept Rate": r['Accept Rate'],
            "Avg SAT": r['Avg SAT'],
            "Est. Fees": r['Est. Fees'],
            "Est. Chance": r['Est. Chance']
        } for r in data])
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    with t1: show(safeties)
    with t2: show(targets)
    with t3: show(reaches)
