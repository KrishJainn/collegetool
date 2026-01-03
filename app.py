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
# 2-Column Layout for Logo and Title
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
# Format: (Name, Rate, SAT, Friendly, Difficulty_Score)
RAW_COLLEGES = [
    # --- TIER 1: ELITE & IVY (96-99) ---
    ("Harvard University", 0.03, 1560, "Med", 99),
    ("Stanford University", 0.04, 1550, "High", 99),
    ("MIT", 0.04, 1550, "High", 99),
    ("Princeton University", 0.04, 1540, "Med", 98),
    ("Yale University", 0.05, 1540, "Med", 98),
    ("California Institute of Technology", 0.03, 1560, "High", 98),
    ("Columbia University", 0.04, 1530, "High", 97),
    ("University of Pennsylvania", 0.06, 1520, "High", 97),
    ("University of Chicago", 0.05, 1540, "Med", 97),
    ("Duke University", 0.06, 1520, "Med", 96),
    ("Johns Hopkins University", 0.07, 1530, "Med", 96),
    ("Northwestern University", 0.07, 1510, "Med", 96),
    ("Dartmouth College", 0.06, 1500, "Med", 96),
    ("Brown University", 0.05, 1500, "Med", 96),
    ("Vanderbilt University", 0.07, 1510, "Med", 96),
    ("Cornell University", 0.07, 1490, "High", 96),
    ("Rice University", 0.09, 1530, "Med", 96),

    # --- TIER 1.5: ELITE PUBLIC & PRIVATE (90-95) ---
    ("WashU St. Louis", 0.12, 1500, "Med", 94),
    ("Carnegie Mellon University", 0.11, 1540, "High", 94),
    ("UCLA", 0.09, 1450, "High", 94),
    ("UC Berkeley", 0.11, 1460, "High", 94),
    ("Georgetown University", 0.12, 1460, "Med", 93),
    ("Emory University", 0.11, 1470, "Med", 93),
    ("University of Notre Dame", 0.12, 1470, "Low", 93),
    ("University of Southern California", 0.12, 1480, "High", 92),
    ("New York University", 0.08, 1490, "High", 92),
    ("University of Michigan-Ann Arbor", 0.18, 1470, "High", 92),
    ("Tufts University", 0.10, 1480, "Med", 92),
    ("Georgia Institute of Technology", 0.16, 1450, "High", 91),
    ("University of Virginia", 0.19, 1460, "Med", 91),
    ("UNC Chapel Hill", 0.17, 1440, "Low", 91),
    ("Boston University", 0.14, 1440, "High", 90),
    ("Northeastern University", 0.07, 1470, "High", 90),
    ("Tulane University", 0.11, 1440, "Med", 90),

    # --- TIER 2: TOP TECH / PRIVATE / PUBLIC (86-89) ---
    ("Boston College", 0.15, 1450, "Med", 89),
    ("University of Rochester", 0.39, 1410, "High", 88),
    ("Case Western Reserve", 0.27, 1450, "High", 88),
    ("William & Mary", 0.33, 1420, "Med", 88),
    ("UC San Diego", 0.24, 1390, "High", 88),
    ("UC Santa Barbara", 0.26, 1380, "High", 87),
    ("UC Irvine", 0.21, 1380, "High", 87),
    ("University of Florida", 0.23, 1400, "Low", 87),
    ("Wake Forest University", 0.20, 1390, "Med", 87),
    ("Villanova University", 0.23, 1390, "Med", 87),
    ("University of Texas at Austin", 0.31, 1390, "Low", 86),
    ("University of Illinois Urbana-Champaign", 0.45, 1420, "High", 86),
    ("University of Wisconsin-Madison", 0.49, 1410, "High", 86),
    ("University of Maryland-College Park", 0.44, 1410, "High", 86),
    ("University of Washington-Seattle", 0.46, 1370, "High", 86),
    ("Lehigh University", 0.37, 1380, "Med", 86),

    # --- TIER 2.5: STRONG STATE & STEM (80-85) ---
    ("Purdue University", 0.50, 1340, "High", 85),
    ("Ohio State University", 0.53, 1370, "High", 84),
    ("University of Georgia", 0.43, 1340, "Low", 84),
    ("Santa Clara University", 0.52, 1390, "High", 84),
    ("Rensselaer Polytechnic Institute", 0.65, 1380, "High", 84),
    ("Virginia Tech", 0.57, 1340, "High", 83),
    ("Texas A&M University", 0.63, 1290, "Low", 83),
    ("University of Connecticut", 0.55, 1320, "Med", 83),
    ("University of Pittsburgh", 0.49, 1340, "Med", 83),
    ("Worcester Polytechnic Institute", 0.58, 1360, "High", 83),
    ("North Carolina State University", 0.47, 1360, "High", 83),
    ("UC Davis", 0.37, 1330, "High", 83),
    ("Rutgers University", 0.66, 1350, "High", 82),
    ("Penn State University", 0.55, 1320, "High", 82),
    ("University of Massachusetts-Amherst", 0.64, 1330, "High", 82),
    ("Fordham University", 0.54, 1340, "Med", 81),
    ("George Washington University", 0.49, 1370, "Med", 81),
    ("Syracuse University", 0.52, 1310, "High", 81),
    ("University of Miami", 0.19, 1380, "Med", 81),
    ("Southern Methodist University", 0.52, 1370, "Med", 81),
    ("Yeshiva University", 0.63, 1370, "Med", 80),
    ("University of Minnesota-Twin Cities", 0.73, 1370, "High", 80),
    ("Stony Brook University", 0.49, 1370, "High", 80),
    ("Binghamton University", 0.42, 1370, "Med", 80),

    # --- TIER 3: MAJOR HUBS / MID-TIER (74-79) ---
    ("Indiana University-Bloomington", 0.82, 1300, "High", 79),
    ("Michigan State University", 0.83, 1240, "High", 78),
    ("University of Delaware", 0.70, 1260, "Med", 78),
    ("University of Colorado Boulder", 0.80, 1280, "Med", 78),
    ("Drexel University", 0.80, 1290, "High", 78),
    ("University at Buffalo", 0.68, 1280, "High", 77),
    ("Clemson University", 0.49, 1310, "Low", 77),
    ("Auburn University", 0.44, 1250, "Low", 77),
    ("Baylor University", 0.46, 1270, "Med", 77),
    ("Marquette University", 0.86, 1250, "Med", 76),
    ("University of Iowa", 0.86, 1230, "High", 76),
    ("University of Utah", 0.89, 1250, "Med", 76),
    ("University of Texas at Dallas", 0.85, 1280, "High", 76),
    ("Stevens Institute of Technology", 0.46, 1380, "High", 76),
    ("Colorado School of Mines", 0.58, 1380, "Med", 76),
    ("Rochester Institute of Technology", 0.67, 1300, "High", 75),
    ("American University", 0.41, 1330, "Med", 75),
    ("University of Denver", 0.78, 1260, "Med", 75),
    ("San Diego State University", 0.39, 1230, "High", 75),
    ("Florida State University", 0.25, 1290, "Low", 75),
    ("Arizona State University", 0.88, 1260, "High", 74),
    ("University of Arizona", 0.87, 1220, "High", 74),
    ("UC Riverside", 0.69, 1180, "High", 74),
    ("UC Santa Cruz", 0.47, 1260, "High", 74),
    ("University of Tennessee", 0.68, 1250, "Low", 74),

    # --- TIER 4: ACCESSIBLE / STRONG ROI (60-73) ---
    ("Temple University", 0.79, 1240, "High", 73),
    ("Oregon State University", 0.83, 1200, "High", 72),
    ("University of South Florida", 0.44, 1260, "Med", 72),
    ("University of Central Florida", 0.41, 1260, "Med", 72),
    ("University of Houston", 0.66, 1230, "High", 72),
    ("Illinois Institute of Technology", 0.61, 1290, "High", 71),
    ("San Jose State University", 0.75, 1200, "High", 70),
    ("University of South Carolina", 0.64, 1270, "Low", 70),
    ("University of Oklahoma", 0.72, 1210, "Med", 70),
    ("University of Kansas", 0.88, 1170, "Med", 68),
    ("University of Kentucky", 0.94, 1190, "Med", 68),
    ("Louisiana State University", 0.75, 1180, "Med", 68),
    ("Washington State University", 0.83, 1120, "Med", 68),
    ("University of Nebraska-Lincoln", 0.79, 1180, "Med", 68),
    ("Iowa State University", 0.90, 1150, "High", 67),
    ("University of Missouri", 0.79, 1200, "Med", 67),
    ("University of Arkansas", 0.79, 1180, "Med", 67),
    ("University of Alabama", 0.80, 1210, "Low", 67),
    ("George Mason University", 0.90, 1210, "High", 66),
    ("DePaul University", 0.70, 1180, "Med", 66),
    ("Seton Hall University", 0.75, 1230, "Med", 66),
    ("Hofstra University", 0.69, 1240, "Med", 66),
    ("University of Cincinnati", 0.86, 1230, "High", 66),
    ("University of Illinois Chicago", 0.79, 1130, "High", 65),
    ("University of North Texas", 0.79, 1130, "High", 64),
    ("Texas Tech University", 0.67, 1180, "Med", 64),
    ("Oklahoma State University", 0.70, 1140, "Med", 64),
    ("Kansas State University", 0.95, 1160, "Med", 63),
    ("West Virginia University", 0.90, 1110, "Med", 62),
    ("Northern Arizona University", 0.80, 1100, "Med", 60),
    ("Florida International University", 0.64, 1190, "High", 60),
    ("Georgia State University", 0.61, 1100, "Med", 60),
    ("University of New Mexico", 0.96, 1080, "Med", 58),
    ("University of Nevada-Las Vegas", 0.85, 1090, "Med", 58),
    ("Pace University", 0.83, 1140, "High", 58),
    ("Suffolk University", 0.87, 1120, "High", 58),
    ("University of Massachusetts-Boston", 0.79, 1100, "High", 58),
    ("University of Massachusetts-Lowell", 0.85, 1230, "High", 58),
    ("Cal State Long Beach", 0.40, 1100, "High", 58),
    ("Cal State Fullerton", 0.67, 1100, "High", 55),
    ("San Francisco State University", 0.93, 1050, "High", 55)
]

COLLEGE_DB = []
for n, r, s, f, d in RAW_COLLEGES:
    COLLEGE_DB.append({"Name": n, "Rate": r, "SAT": s, "Friendly": f, "Diff": d})

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
        final_raw = (norm_gpa_score * 0.9) + ec_pts
        return max(0, final_raw - major_penalty)
        
    final_raw = (norm_gpa_score * 0.6) + (norm_sat_score * 0.3) + ec_pts
    return max(0, final_raw - major_penalty)

def classify_college(student_score, college_diff, friendly):
    gap = student_score - college_diff
    category = "Target"
    
    if gap < -5:
        category = "Aspirational"
    elif gap > 8:
        category = "Safety"
        
    # Ivy/Elite Exception
    if college_diff >= 96 and gap <= 2:
        category = "Aspirational"
        
    if category == "Safety" and friendly == "Low":
        category = "Target"
        
    return category, gap

# --- MAIN APP UI ---
name = st.sidebar.text_input("Name", "Student")
major_map = {
    "Computer Science / Engineering": 8, 
    "Business / Finance": 5,
    "Biology / Pre-Med": 5,
    "Humanities / Arts / Other": 0
}
major = st.sidebar.selectbox("Major", list(major_map.keys()))
major_penalty = major_map[major]

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

# --- CALC & OUTPUT ---
student_score = calculate_student_score(norm_gpa, sat, ec_tier, major_penalty)

safeties, targets, aspirationals = [], [], []

for c in COLLEGE_DB:
    cat, gap = classify_college(student_score, c['Diff'], c['Friendly'])
    row = {"College": c['Name'], "Rate": c['Rate'], "Diff": c['Diff'], "Gap": gap, "Friendly": c['Friendly']}
    
    if cat == "Safety": safeties.append(row)
    elif cat == "Target": targets.append(row)
    else: aspirationals.append(row)

# SORTING (Best 20)
df_safe = pd.DataFrame(safeties)
if not df_safe.empty: df_safe = df_safe.sort_values(by="Diff", ascending=False).head(20)

df_targ = pd.DataFrame(targets)
if not df_targ.empty: df_targ = df_targ.sort_values(by="Gap", ascending=True).head(20)

df_asp = pd.DataFrame(aspirationals)
if not df_asp.empty: df_asp = df_asp.sort_values(by="Gap", ascending=False).head(20)

# Display Stats
c1, c2, c3 = st.columns(3)
c1.metric("Student Power Score", f"{student_score:.1f}")
c2.metric("GPA (Normalized)", f"{norm_gpa}")
c3.metric("SAT", sat if sat > 0 else "Test Optional")

t1, t2, t3 = st.tabs(["🛡️ Safeties", "🎯 Targets", "🚀 Aspirationals"])

def render(df):
    if df.empty:
        st.info("No colleges in this category.")
        return
    d = df.copy()
    d['Rate'] = d['Rate'].apply(lambda x: f"{x*100:.1f}%")
    d['Gap'] = d['Gap'].apply(lambda x: f"{x:+.1f}")
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
    Major Interest: {major}
    Profile Score: {student_score:.1f}
    
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
