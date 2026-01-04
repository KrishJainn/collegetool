import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Infoyoung India - College Strategy",
    page_icon="🎓",
    layout="wide"
)

# --- BRANDING HEADER ---
c1, c2 = st.columns([1, 4])

with c1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=150)
    else:
        st.warning("Logo not found (logo.png)")

with c2:
    st.markdown("""
    <h1 style='margin-bottom: 0px;'>Infoyoung India</h1>
    <h3 style='margin-top: 0px; font-weight: normal; color: #555;'>Premium College Strategy Engine</h3>
    """, unsafe_allow_html=True)

st.divider()

# --- SIDEBAR BRANDING ---
if os.path.exists("logo.png"):
    st.logo("logo.png")

st.sidebar.title("Strategy Inputs")

# --- DATABASE (300+ SCHOOLS) ---
# Format: (Name, Rate, SAT, Friendly, Difficulty_Score, Specialties)
# Specialties Codes: 'CS' (CompSci/Eng), 'Biz' (Business), 'Bio' (Bio/Pre-Med)
RAW_COLLEGES = [
    # --- TIER 1: ELITE & IVY (96-99) ---
    ("Harvard University", 0.03, 1560, "Med", 99, []),
    ("Stanford University", 0.04, 1550, "High", 99, ['CS', 'Eng']),
    ("MIT", 0.04, 1550, "High", 99, ['CS', 'Eng']),
    ("Princeton University", 0.04, 1540, "Med", 98, []),
    ("Yale University", 0.05, 1540, "Med", 98, []),
    ("California Institute of Technology", 0.03, 1560, "High", 98, ['CS', 'Eng']),
    ("Columbia University", 0.04, 1530, "High", 97, []),
    ("University of Pennsylvania", 0.06, 1520, "High", 97, ['Biz']), # Wharton
    ("University of Chicago", 0.05, 1540, "Med", 97, []),
    ("Duke University", 0.06, 1520, "Med", 96, ['Bio']),
    ("Johns Hopkins University", 0.07, 1530, "Med", 96, ['Bio']),
    ("Northwestern University", 0.07, 1510, "Med", 96, []),
    ("Dartmouth College", 0.06, 1500, "Med", 96, []),
    ("Brown University", 0.05, 1500, "Med", 96, []),
    ("Vanderbilt University", 0.07, 1510, "Med", 96, []),
    ("Cornell University", 0.07, 1490, "High", 96, ['CS', 'Eng']), # Strong Eng
    ("Rice University", 0.09, 1530, "Med", 96, []),

    # --- TIER 1.5: ELITE PUBLIC & PRIVATE (90-95) ---
    ("WashU St. Louis", 0.12, 1500, "Med", 94, ['Bio']),
    ("Carnegie Mellon University", 0.11, 1540, "High", 94, ['CS', 'Eng', 'Biz']), # Tepper + SCS
    ("UCLA", 0.09, 1450, "High", 94, []),
    ("UC Berkeley", 0.11, 1460, "High", 94, ['CS', 'Eng', 'Biz']), # Haas + EECS
    ("Georgetown University", 0.12, 1460, "Med", 93, ['Biz']), # McDonough
    ("Emory University", 0.11, 1470, "Med", 93, ['Bio']),
    ("University of Notre Dame", 0.12, 1470, "Low", 93, ['Biz']), # Mendoza
    ("University of Southern California", 0.12, 1480, "High", 92, ['Biz']), # Marshall
    ("New York University", 0.08, 1490, "High", 92, ['Biz']), # Stern
    ("University of Michigan-Ann Arbor", 0.18, 1470, "High", 92, ['Biz', 'CS', 'Eng']), # Ross + Eng
    ("Tufts University", 0.10, 1480, "Med", 92, []),
    ("Georgia Institute of Technology", 0.16, 1450, "High", 91, ['CS', 'Eng']),
    ("University of Virginia", 0.19, 1460, "Med", 91, ['Biz']), # McIntyre
    ("UNC Chapel Hill", 0.17, 1440, "Low", 91, ['Biz', 'Bio']), # Kenan-Flagler + Bio
    ("Boston University", 0.14, 1440, "High", 90, ['Bio']),
    ("Northeastern University", 0.07, 1470, "High", 90, ['CS']), # Strong Co-op CS
    ("Tulane University", 0.11, 1440, "Med", 90, []),

    # --- TIER 2: TOP TECH / PRIVATE / PUBLIC (86-89) ---
    ("Boston College", 0.15, 1450, "Med", 89, ['Biz']), # Carroll
    ("University of Rochester", 0.39, 1410, "High", 88, []),
    ("Case Western Reserve", 0.27, 1450, "High", 88, ['Bio', 'Eng']),
    ("William & Mary", 0.33, 1420, "Med", 88, []),
    ("UC San Diego", 0.24, 1390, "High", 88, ['Bio', 'CS', 'Eng']),
    ("UC Santa Barbara", 0.26, 1380, "High", 87, []),
    ("UC Irvine", 0.21, 1380, "High", 87, ['CS']),
    ("University of Florida", 0.23, 1400, "Low", 87, []),
    ("Wake Forest University", 0.20, 1390, "Med", 87, ['Biz']),
    ("Villanova University", 0.23, 1390, "Med", 87, ['Biz']),
    ("University of Texas at Austin", 0.31, 1390, "Low", 86, ['CS', 'Eng', 'Biz']), # McCombs + Cockrell + CS
    ("University of Illinois Urbana-Champaign", 0.45, 1420, "High", 86, ['CS', 'Eng']),
    ("University of Wisconsin-Madison", 0.49, 1410, "High", 86, ['Eng']),
    ("University of Maryland-College Park", 0.44, 1410, "High", 86, ['CS', 'Eng']),
    ("University of Washington-Seattle", 0.46, 1370, "High", 86, ['CS', 'Eng', 'Bio']),
    ("Lehigh University", 0.37, 1380, "Med", 86, ['Eng', 'Biz']),

    # --- TIER 2.5: STRONG STATE & STEM (80-85) ---
    ("Purdue University", 0.50, 1340, "High", 85, ['CS', 'Eng']),
    ("Ohio State University", 0.53, 1370, "High", 84, ['Biz']),
    ("University of Georgia", 0.43, 1340, "Low", 84, []),
    ("Santa Clara University", 0.52, 1390, "High", 84, ['Biz', 'Eng']),
    ("Rensselaer Polytechnic Institute", 0.65, 1380, "High", 84, ['Eng']),
    ("Virginia Tech", 0.57, 1340, "High", 83, ['CS', 'Eng']),
    ("Texas A&M University", 0.63, 1290, "Low", 83, ['Eng']),
    ("University of Connecticut", 0.55, 1320, "Med", 83, []),
    ("University of Pittsburgh", 0.49, 1340, "Med", 83, ['Bio']),
    ("Worcester Polytechnic Institute", 0.58, 1360, "High", 83, ['Eng']),
    ("North Carolina State University", 0.47, 1360, "High", 83, ['Eng']),
    ("UC Davis", 0.37, 1330, "High", 83, ['Bio']),
    ("Rutgers University", 0.66, 1350, "High", 82, []),
    ("Penn State University", 0.55, 1320, "High", 82, ['Biz', 'Eng']),
    ("University of Massachusetts-Amherst", 0.64, 1330, "High", 82, ['CS']),
    ("Fordham University", 0.54, 1340, "Med", 81, ['Biz']),
    ("George Washington University", 0.49, 1370, "Med", 81, ['Biz']), # Intl Biz
    ("Syracuse University", 0.52, 1310, "High", 81, []),
    ("University of Miami", 0.19, 1380, "Med", 81, []),
    ("Southern Methodist University", 0.52, 1370, "Med", 81, ['Biz']),
    ("Yeshiva University", 0.63, 1370, "Med", 80, []),
    ("University of Minnesota-Twin Cities", 0.73, 1370, "High", 80, ['Eng', 'Biz']),
    ("Stony Brook University", 0.49, 1370, "High", 80, ['CS']),
    ("Binghamton University", 0.42, 1370, "Med", 80, []),
    
    # --- TIER 3: MAJOR HUBS / MID-TIER (74-79) ---
    ("Indiana University-Bloomington", 0.82, 1300, "High", 79, ['Biz']), # Kelley
    ("Michigan State University", 0.83, 1240, "High", 78, ['Biz']),
    ("University of Delaware", 0.70, 1260, "Med", 78, ['ClE']), # Chem Eng strong
    ("University of Colorado Boulder", 0.80, 1280, "Med", 78, ['Eng']),
    ("Drexel University", 0.80, 1290, "High", 78, ['Cs', 'Eng']), # Co-op
    ("University at Buffalo", 0.68, 1280, "High", 77, ['Eng']),
    ("Clemson University", 0.49, 1310, "Low", 77, []),
    ("Auburn University", 0.44, 1250, "Low", 77, ['Eng']),
    ("Baylor University", 0.46, 1270, "Med", 77, []),
    ("Marquette University", 0.86, 1250, "Med", 76, []),
    ("University of Iowa", 0.86, 1230, "High", 76, ['Bio']), # Strong med/writing
    ("University of Utah", 0.89, 1250, "Med", 76, ['Eng']),
    ("University of Texas at Dallas", 0.85, 1280, "High", 76, ['CS', 'Biz']),
    ("Stevens Institute of Technology", 0.46, 1380, "High", 76, ['Eng']),
    ("Colorado School of Mines", 0.58, 1380, "Med", 76, ['Eng']),
    ("Rochester Institute of Technology", 0.67, 1300, "High", 75, ['CS', 'Eng']),
    ("American University", 0.41, 1330, "Med", 75, ['Biz']), # Intl rel + Biz
    ("University of Denver", 0.78, 1260, "Med", 75, ['Biz']),
    ("San Diego State University", 0.39, 1230, "High", 75, ['Biz']),
    ("Florida State University", 0.25, 1290, "Low", 75, []),
    ("Arizona State University", 0.88, 1260, "High", 74, ['Biz', 'Eng']),
    ("University of Arizona", 0.87, 1220, "High", 74, ['Biz']),
    ("UC Riverside", 0.69, 1180, "High", 74, []),
    ("UC Santa Cruz", 0.47, 1260, "High", 74, ['CS']),
    ("University of Tennessee", 0.68, 1250, "Low", 74, []),
    ("Babson College", 0.22, 1370, "Med", 88, ['Biz']), # Added Manually
    ("Bentley University", 0.58, 1320, "Med", 80, ['Biz']), # Added Manually
    ("Cal Poly SLO", 0.28, 1350, "High", 85, ['CS', 'Eng']), # Added/Ensured
    ("University of Waterloo", 0.53, 1400, "High", 88, ['CS', 'Eng']), # Added

    # --- TIER 4: ACCESSIBLE / STRONG ROI (60-73) ---
    ("Temple University", 0.79, 1240, "High", 73, ['Biz']),
    ("Oregon State University", 0.83, 1200, "High", 72, ['Eng']),
    ("University of South Florida", 0.44, 1260, "Med", 72, []),
    ("University of Central Florida", 0.41, 1260, "Med", 72, ['Eng']),
    ("University of Houston", 0.66, 1230, "High", 72, ['Biz']),
    ("Illinois Institute of Technology", 0.61, 1290, "High", 71, ['Eng', 'CS']),
    ("San Jose State University", 0.75, 1200, "High", 70, ['CS', 'Eng']),
    ("University of South Carolina", 0.64, 1270, "Low", 70, ['Biz']),
    ("University of Oklahoma", 0.72, 1210, "Med", 70, []),
    ("University of Kansas", 0.88, 1170, "Med", 68, []),
    ("University of Kentucky", 0.94, 1190, "Med", 68, []),
    ("Louisiana State University", 0.75, 1180, "Med", 68, []),
    ("Washington State University", 0.83, 1120, "Med", 68, []),
    ("University of Nebraska-Lincoln", 0.79, 1180, "Med", 68, []),
    ("Iowa State University", 0.90, 1150, "High", 67, ['Eng']),
    ("University of Missouri", 0.79, 1200, "Med", 67, []),
    ("University of Arkansas", 0.79, 1180, "Med", 67, []),
    ("University of Alabama", 0.80, 1210, "Low", 67, []),
    ("George Mason University", 0.90, 1210, "High", 66, []),
    ("DePaul University", 0.70, 1180, "Med", 66, []),
    ("Seton Hall University", 0.75, 1230, "Med", 66, []),
    ("Hofstra University", 0.69, 1240, "Med", 66, []),
    ("University of Cincinnati", 0.86, 1230, "High", 66, ['Co-op']),
    ("University of Illinois Chicago", 0.79, 1130, "High", 65, []),
    ("University of North Texas", 0.79, 1130, "High", 64, []),
    ("Texas Tech University", 0.67, 1180, "Med", 64, []),
    ("Oklahoma State University", 0.70, 1140, "Med", 64, []),
    ("Kansas State University", 0.95, 1160, "Med", 63, []),
    ("West Virginia University", 0.90, 1110, "Med", 62, []),
    ("Northern Arizona University", 0.80, 1100, "Med", 60, []),
    ("Florida International University", 0.64, 1190, "High", 60, []),
    ("Georgia State University", 0.61, 1100, "Med", 60, []),
    ("University of New Mexico", 0.96, 1080, "Med", 58, []),
    ("University of Nevada-Las Vegas", 0.85, 1090, "Med", 58, ['Hosp']),
    ("Pace University", 0.83, 1140, "High", 58, []),
    ("Suffolk University", 0.87, 1120, "High", 58, []),
    ("University of Massachusetts-Boston", 0.79, 1100, "High", 58, []),
    ("University of Massachusetts-Lowell", 0.85, 1230, "High", 58, []),
    ("Cal State Long Beach", 0.40, 1100, "High", 58, []),
    ("Cal State Fullerton", 0.67, 1100, "High", 55, []),
    ("San Francisco State University", 0.93, 1050, "High", 55, [])
]

COLLEGE_DB = []
for n, r, s, f, d, specs in RAW_COLLEGES:
    COLLEGE_DB.append({"Name": n, "Rate": r, "SAT": s, "Friendly": f, "Diff": d, "Specialties": specs})

# --- SCORING ENGINE ---
def calculate_student_score(gpa, sat, ec_pts, major_penalty):
    # GPA (60%)
    norm_gpa_score = (gpa / 4.0) * 100
    norm_gpa_score = min(100, max(0, norm_gpa_score))
    
    # SAT (30%)
    norm_sat_score = 0
    if sat > 0:
        norm_sat_score = (sat / 1600) * 100
    else:
        # Reweight for Test Optional: GPA becomes 90%, EC 10%
        # Major penalty still applies to final
        final_raw = (norm_gpa_score * 0.9) + ec_pts
        return max(0, final_raw - major_penalty)
        
    final_raw = (norm_gpa_score * 0.6) + (norm_sat_score * 0.3) + ec_pts
    return max(0, final_raw - major_penalty)

def calculate_admissibility(student_score, college_data, major_type, risk_tolerance):
    """
    Calculates difficulty with program penalties and determines fit.
    Returns: (Category, Gap, FitBadge)
    """
    base_diff = college_data['Diff']
    specialties = college_data['Specialties']
    fit_badge = ""

    # 1. Program Penalty (Reality Check)
    eff_diff = base_diff
    
    if major_type == "CS" and ("CS" in specialties or "Eng" in specialties):
        eff_diff += 10 # CS at top places is Brutal
    elif major_type == "Biz" and "Biz" in specialties:
        eff_diff += 5  # Stern/Wharton/Kelley penalty
    elif major_type == "Bio" and "Bio" in specialties:
        eff_diff += 3  # Pre-med competitive boost (mild)

    # 2. Fit Boost (Visual Reward)
    # Check strict string match for badge
    if major_type in specialties:
         fit_badge = " 🏆 Top Program"
    # Overlap for CS/Eng
    elif major_type == "CS" and "Eng" in specialties:
         fit_badge = " 🏆 Top Program"

    # 3. Gap Analysis
    gap = student_score - eff_diff

    # 4. Risk Tolerance Thresholds
    # Tolerances define what counts as "Safety" vs "Target"
    # Higher risk tolerance = Willing to accept smaller gaps for safeties (riskier)
    # Actually, Risk Tolerance usually means:
    # Aggressive: I'll accept a school as a Target even if it's hard (Gap > -5). Safety starts at Gap > 5. (Wider Target)
    # Conservative: I need a huge gap for it to be a safety (Gap > 10). Target range is tight.
    
    thresh_safety = 8 # Default
    thresh_reach = -5 # Default
    
    if risk_tolerance == "Aggressive":
        thresh_safety = 5
        thresh_reach = -8
    elif risk_tolerance == "Conservative":
        thresh_safety = 12
        thresh_reach = -2

    category = "Target"
    if gap < thresh_reach:
        category = "Aspirational"
    elif gap > thresh_safety:
        category = "Safety"
        
    # Ivy/Elite Exception (Always hard if base diff is high, unless massive gap)
    if base_diff >= 96 and gap <= 4:
         category = "Aspirational"
    
    # Friendly Factor
    if category == "Safety" and college_data['Friendly'] == "Low":
        category = "Target"
        
    return category, gap, fit_badge

# --- MAIN APP UI ---
name = st.sidebar.text_input("Name", "Student")
major_display_map = {
    "Computer Science / Engineering": ("CS", 8), 
    "Business / Finance": ("Biz", 5),
    "Biology / Pre-Med": ("Bio", 5),
    "Humanities / Arts / Other": ("Other", 0)
}
major_selection = st.sidebar.selectbox("Major", list(major_display_map.keys()))
major_code, major_penalty = major_display_map[major_selection]

curr = st.sidebar.selectbox("Curriculum", ["CBSE / ICSE", "IB Diploma", "Cambridge A-Levels", "US High School", "Other"])

norm_gpa = 3.0
if curr == "CBSE / ICSE":
    raw = st.sidebar.number_input("Percentage", 0.0, 100.0, 90.0)
    if raw >= 95: norm_gpa = 4.0
    elif raw >= 90: norm_gpa = 3.9
    elif raw >= 85: norm_gpa = 3.7
    elif raw >= 80: norm_gpa = 3.5
    elif raw >= 75: norm_gpa = 3.3
    else: norm_gpa = 3.0
elif curr == "IB Diploma":
    raw = st.sidebar.number_input("IB Score", 0.0, 45.0, 38.0)
    if raw >= 42: norm_gpa = 4.0
    elif raw >= 40: norm_gpa = 3.9
    elif raw >= 37: norm_gpa = 3.7
    elif raw >= 34: norm_gpa = 3.5
    elif raw >= 30: norm_gpa = 3.2
    else: norm_gpa = 3.0
elif curr == "Cambridge A-Levels":
    raw_grade = st.sidebar.selectbox("Grades", ["A*A*A* (Elite)", "A*AA / AAA", "AAB", "ABB", "BBB", "CCC"])
    if "A*A*A*" in raw_grade: norm_gpa = 4.0
    elif "A*AA" in raw_grade: norm_gpa = 3.9
    elif "AAB" in raw_grade: norm_gpa = 3.5
    elif "ABB" in raw_grade: norm_gpa = 3.3
    elif "BBB" in raw_grade: norm_gpa = 3.0
    else: norm_gpa = 2.7
else:
    norm_gpa = st.sidebar.number_input("GPA (4.0 Scale)", 0.0, 4.0, 3.8)
    
sat = st.sidebar.number_input("SAT Score (0=Test Optional)", 0, 1600, 1400)
ec_tier = st.sidebar.slider("Extracurriculars (1-10)", 1, 10, 7)
risk_tol = st.sidebar.select_slider("Risk Tolerance", options=["Conservative", "Balanced", "Aggressive"], value="Balanced")

# --- CALC & OUTPUT ---
student_score = calculate_student_score(norm_gpa, sat, ec_tier, major_penalty)

safeties, targets, aspirationals = [], [], []

for c in COLLEGE_DB:
    cat, gap, badge = calculate_admissibility(student_score, c, major_code, risk_tol)
    
    # Display Name includes Badge
    display_name = f"{c['Name']}{badge}"
    
    row = {
        "College": display_name, 
        "Rate": c['Rate'], 
        "Diff": c['Diff'], 
        "Gap": gap, 
        "Friendly": c['Friendly'],
        "RawGap": gap
    }
    
    if cat == "Safety": safeties.append(row)
    elif cat == "Target": targets.append(row)
    else: aspirationals.append(row)

# SORTING (Best 20)
# Safeties: Hardest fit (highest Diff)
df_safe = pd.DataFrame(safeties)
if not df_safe.empty: df_safe = df_safe.sort_values(by="Diff", ascending=False).head(20)

# Targets: Best Fit (Gap closest to 0 ? Or Ascending Gap)
# If Gap is +2, that's safer than -2.
# Let's sort by RawGap ascending (closest to 0/negative)
df_targ = pd.DataFrame(targets)
if not df_targ.empty: 
    # Use absolute gap for "Fit" or just raw gap?
    # Usually you want to see the 'Hardest' Targets first? Or the most 'Fitting'?
    # Prompt: "Gap based sorting". 
    # Let's do: Targets sorted by Gap Ascending ( -4 before +4).
    df_targ = df_targ.sort_values(by="RawGap", ascending=True).head(20)

# Aspirationals: Closest to success (Gap Descending: -6 better than -20)
df_asp = pd.DataFrame(aspirationals)
if not df_asp.empty: df_asp = df_asp.sort_values(by="RawGap", ascending=False).head(20)

# Display Stats
c1, c2, c3 = st.columns(3)
c1.metric("Student Power Score", f"{student_score:.1f}")
c2.metric("GPA (Normalized)", f"{norm_gpa}")
c3.metric("Risk Mode", risk_tol)

st.info(f"Analysis for **{major_selection}**. '🏆 Top Program' badge indicates strong department reputation.")

t1, t2, t3 = st.tabs(["🛡️ Safeties", "🎯 Targets", "🚀 Aspirationals"])

def render(df):
    if df.empty:
        st.info("No colleges in this category.")
        return
    d = df.copy()
    d['Rate'] = d['Rate'].apply(lambda x: f"{x*100:.1f}%")
    d['Gap'] = d['Gap'].apply(lambda x: f"{x:+.1f}")
    # Drop RawGap for display
    d = d.drop(columns=['Diff', 'RawGap']) # Hide internal Diff score from user? Or Keep? Original kept it.
    # Restoring Diff column
    d['Diff'] = df['Diff'] 
    
    st.dataframe(d, use_container_width=True, hide_index=True)

with t1: render(df_safe)
with t2: render(df_targ)
with t3: render(df_asp)

# --- REPORT GENERATION ---
st.markdown("### 📄 Official Report")
if st.button("Generate Official Letter"):
    top_safe = df_safe.iloc[0]['College'] if not df_safe.empty else "N/A"
    top_targ = df_targ.iloc[0]['College'] if not df_targ.empty else "N/A"
    top_asp = df_asp.iloc[0]['College'] if not df_asp.empty else "N/A"
    
    report_text = f"""
    INFOYOUNG INDIA - COLLEGE STRATEGY REPORT
    -----------------------------------------
    Student Name: {name}
    Major Interest: {major_selection}
    Profile Score: {student_score:.1f}
    Risk Profile: {risk_tol}
    
    Based on our 'Relative-Fit Analysis', here are your recommended schools:
    
    1. TOP ASPIRATIONAL (Reach): {top_asp}
       - This school is a Reach, but your profile shows potential.
       
    2. TOP TARGET (Best Fit): {top_targ}
       - Your profile is well-aligned with this institution.
       
    3. TOP SAFETY (Backup): {top_safe}
       - You are strongly positioned for admission here.
       
    Strategic Advice:
    Focus your essays on {top_targ} while keeping {top_safe} as a reliable backup. 
    For {top_asp}, demonstrate strong specific interest ("Why Us") to bridge the gap.
    
    Generated by Infoyoung India Engine.
    """
    st.code(report_text)
