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

MAJOR_MAP = {
    "Computer Science & Engineering": {"tags": ['CS', 'Eng'], "penalty": 12},
    "Business & Finance": {"tags": ['Biz'], "penalty": 8},
    "Economics": {"tags": ['Econ'], "penalty": 8},
    "Natural Sciences": {"tags": ['Sci'], "penalty": 5},
    "Biology & Pre-Med": {"tags": ['Bio'], "penalty": 6},
    "Humanities & Arts": {"tags": [], "penalty": 0}
}

# --- SCORING ---
def calc_score(gpa, sat, ec):
    g = min(100, (gpa / 4.0) * 100)
    
    # SAT scoring with curve - makes lower scores drop faster
    # 1600 = 100, 1500 = 90, 1400 = 78, 1300 = 65, 1200 = 52
    if sat >= 1500:
        s = 90 + ((sat - 1500) / 100) * 10  # 1500-1600 maps to 90-100
    elif sat >= 1400:
        s = 78 + ((sat - 1400) / 100) * 12  # 1400-1500 maps to 78-90
    elif sat >= 1300:
        s = 65 + ((sat - 1300) / 100) * 13  # 1300-1400 maps to 65-78
    elif sat >= 1200:
        s = 52 + ((sat - 1200) / 100) * 13  # 1200-1300 maps to 52-65
    else:
        s = max(30, (sat / 1200) * 52)  # Below 1200 scales down
    
    # New weights: GPA 35%, SAT 55%, EC 10%
    return (g * 0.35) + (s * 0.55) + ec

def classify(score, college, major):
    name, avg_sat, diff, friendly, specs, school_names, state, fees = college
    m = MAJOR_MAP.get(major, {"tags": [], "penalty": 0})
    
    pen = m['penalty'] if any(t in specs for t in m['tags']) else 0
    intl = 15 if friendly == "Low" else (-5 if friendly == "High" else 0)
    
    eff = diff + pen + intl
    gap = score - eff
    
    # SAT comparison adjustment - compare student SAT with college avg
    student_sat = st.session_state.get('student', {}).get('sat', 0)
    sat_diff = student_sat - avg_sat
    sat_adjustment = sat_diff / 25  # Every 25 SAT points = ~1 point adjustment
    gap += sat_adjustment
    
    s_th, r_th = 8, -8
    
    cat = "Target"
    if gap > s_th: cat = "Safety"
    elif gap < r_th: cat = "Reach"
    if diff >= 95 and gap <= 3: cat = "Reach"
    
    # Get specific school name based on major
    display_name = name
    for tag in m['tags']:
        if tag in school_names:
            display_name = f"{name} ({school_names[tag]})"
            break
    
    return cat, gap, display_name, friendly, avg_sat, state, fees

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
                Our algorithm analyzes <strong>180+ US universities</strong> to find your Safety, Target, and Reach schools.
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
                gpa = 4.0 if pct >= 95 else 3.9 if pct >= 90 else 3.7 if pct >= 85 else 3.5 if pct >= 80 else 3.3 if pct >= 75 else 3.0 if pct >= 70 else 2.7
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
    
    score = calc_score(s['gpa'], s['sat'], s['ec'])
    
    safeties, targets, reaches = [], [], []
    
    for c in COLLEGES:
        cat, gap, display_name, friendly, avg_sat, state, fees = classify(score, c, s['major'])
        
        row = {
            "University": display_name,
            "State": state,
            "Avg SAT": avg_sat,
            "Est. Fees": f"${fees:,}",
            "Fit": gap,
            "_gap": gap,
            "_diff": c[2]
        }
        
        if cat == "Safety": safeties.append(row)
        elif cat == "Target": targets.append(row)
        else: reaches.append(row)
    
    if len(safeties) < 5 and targets:
        targets.sort(key=lambda x: x['_gap'], reverse=True)
        for _ in range(min(5 - len(safeties), len(targets))):
            m = targets.pop(0)
            safeties.append(m)
    
    safeties.sort(key=lambda x: x['_diff'], reverse=True)
    targets.sort(key=lambda x: abs(x['_gap']))
    reaches.sort(key=lambda x: x['_diff'], reverse=True)
    
    # Keep full lists for Excel export
    all_safeties, all_targets, all_reaches = safeties.copy(), targets.copy(), reaches.copy()
    
    # Limit display to top 15 each
    safeties, targets, reaches = safeties[:15], targets[:15], reaches[:15]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Score", f"{score:.0f}/100")
    c2.metric("Safety Schools", len(safeties))
    c3.metric("Target Schools", len(targets))
    c4.metric("Reach Schools", len(reaches))
    
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
            
            # Add category labels and combine all
            for r in safeties: r['Category'] = 'Safety'
            for r in targets: r['Category'] = 'Target'
            for r in reaches: r['Category'] = 'Reach'
            all_colleges = safeties + targets + reaches
            
            try:
                with pd.ExcelWriter(o, engine='xlsxwriter') as w:
                    # Student info sheet
                    student_info = pd.DataFrame([{
                        'Student Name': s['name'],
                        'Curriculum': s['curriculum'],
                        'GPA': f"{s['gpa']:.2f}",
                        'SAT': s['sat'],
                        'Major': s['major'],
                        'EC Score': f"{s['ec']}/10",
                        'Overall Score': f"{score:.0f}/100"
                    }])
                    student_info.to_excel(w, sheet_name='Student Profile', index=False)
                    
                    # Combined sheet with all 45
                    if all_colleges:
                        cols = ['Category', 'University', 'State', 'Avg SAT', 'Est. Fees', 'Fit']
                        df_all = pd.DataFrame(all_colleges)[cols]
                        df_all.to_excel(w, sheet_name='All Recommendations', index=False)
                    # Individual sheets
                    cols_single = ['University', 'State', 'Avg SAT', 'Est. Fees', 'Fit']
                    if safeties: pd.DataFrame(safeties)[cols_single].to_excel(w, sheet_name='Safety', index=False)
                    if targets: pd.DataFrame(targets)[cols_single].to_excel(w, sheet_name='Target', index=False)
                    if reaches: pd.DataFrame(reaches)[cols_single].to_excel(w, sheet_name='Reach', index=False)
            except:
                # Fallback to openpyxl
                with pd.ExcelWriter(o, engine='openpyxl') as w:
                    student_info = pd.DataFrame([{'Student Name': s['name'], 'Curriculum': s['curriculum'], 'GPA': f"{s['gpa']:.2f}", 'SAT': s['sat'], 'Major': s['major'], 'EC Score': f"{s['ec']}/10", 'Overall Score': f"{score:.0f}/100"}])
                    student_info.to_excel(w, sheet_name='Student Profile', index=False)
                    if all_colleges:
                        pd.DataFrame(all_colleges)[['Category', 'University', 'State', 'Avg SAT', 'Est. Fees', 'Fit']].to_excel(w, sheet_name='All Recommendations', index=False)
            return o.getvalue()
        
        st.download_button("Download Excel Report", xl(), f"{s['name']}_Strategy.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    
    st.write("")
    st.divider()
    
    t1, t2, t3 = st.tabs(["Safety", "Target", "Reach"])
    
    def show(data):
        if not data:
            st.info("No schools found in this category.")
            return
        df = pd.DataFrame([{
            "University": r['University'],
            "State": r['State'],
            "Avg SAT": r['Avg SAT'],
            "Est. Fees": r['Est. Fees'],
            "Fit": f"{r['Fit']:+.0f}"
        } for r in data])
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    with t1: show(safeties)
    with t2: show(targets)
    with t3: show(reaches)
