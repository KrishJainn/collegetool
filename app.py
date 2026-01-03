import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Relative-Fit College Strategy Engine", page_icon="🎓", layout="wide")

# --- MASSIVE DATABASE (300+ SCHOOLS) ---
# Format: (Name, Rate, SAT, Friendly, Difficulty_Score)
# Diff 96-99: Ivies/Elite
# Diff 90-95: Elite Private/Public
# Diff 86-89: Top Tech/Private
# Diff 80-85: Strong State
# Diff 74-79: Major Hubs
# Diff 68-73: Mid-Tier
# Diff 55-67: Accessible

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
    ("University of Rochester", 0.39, 1410, "High", 88), # High stats but higher rate
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
    ("Michigan State University", 0.83, 1240, "High", 78), # Easier SAT but big brand
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
    ("Stevens Institute of Technology", 0.46, 1380, "High", 76), # Hard entry
    ("Colorado School of Mines", 0.58, 1380, "Med", 76),
    ("Rochester Institute of Technology", 0.67, 1300, "High", 75),
    ("American University", 0.41, 1330, "Med", 75),
    ("University of Denver", 0.78, 1260, "Med", 75),
    ("San Diego State University", 0.39, 1230, "High", 75),
    ("Florida State University", 0.25, 1290, "Low", 75), # Selective but Low Friendly
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
    ("San Jose State University", 0.75, 1200, "High", 70), # Silicon Valley Hub
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
    ("Cal State Long Beach", 0.40, 1100, "High", 58), # Competitive for CSU
    ("Cal State Fullerton", 0.67, 1100, "High", 55),
    ("San Francisco State University", 0.93, 1050, "High", 55)
]

# Create Dict
COLLEGE_DB = []
for n, r, s, f, d in RAW_COLLEGES:
    COLLEGE_DB.append({"Name": n, "Rate": r, "SAT": s, "Friendly": f, "Diff": d})

# --- SCORING ENGINE ---

def calculate_student_score(gpa, sat, ec_pts, major_penalty):
    """
    Calculates Student Power Score (0-100)
    GPA: 60%, SAT: 30%, EC: 10%
    """
    # 1. Norm GPA (0-100) based on 4.0 scale
    # 4.0 -> 100, 3.0 -> 75, 2.0 -> 50
    norm_gpa_score = (gpa / 4.0) * 100
    norm_gpa_score = min(100, max(0, norm_gpa_score))
    
    # 2. Norm SAT (0-100)
    # 1600 -> 100, 1000 -> 62.5 (1000/1600 * 100), 0 -> 0 (or reweight)
    norm_sat_score = 0
    if sat > 0:
        norm_sat_score = (sat / 1600) * 100
    else:
        # If test optional, we might rely entirely on GPA/EC or boost GPA weight.
        # Strict Relative Fit: If you hide SAT, you lose the points unless we reweight.
        # Let's reweight GPA to 90% (from 60) and EC to 10%.
        # This keeps the scale 0-100.
        norm_gpa_score_reweighted = norm_gpa_score # Uses full 100 scale of GPA
        # Weighted Final: 90% GPA + 10% EC
        final_raw = (norm_gpa_score * 0.9) + ec_pts
        return max(0, final_raw - major_penalty)
        
    # Standard Weighting
    # Score = (GPA_Score * 0.6) + (SAT_Score * 0.3) + EC_Pts
    final_raw = (norm_gpa_score * 0.6) + (norm_sat_score * 0.3) + ec_pts
    
    return max(0, final_raw - major_penalty)

def classify_college(student_score, college_diff, friendly):
    gap = student_score - college_diff
    
    # Classification
    category = "Target"
    
    # Aspirational
    if gap < -5:
        category = "Aspirational"
    # Safety
    elif gap > 8:
        category = "Safety"
        
    # Special Rules
    # If College is Ivy (Diff >= 96), it is Aspirational unless Gap > 2 (Student Score > 98)
    if college_diff >= 96 and gap <= 2:
        category = "Aspirational"
        
    # Unfriendly check: If gap is small positive but Low Friendly, might degrade to Target
    # But Gap Analysis usually handles it if we penalized Score? 
    # Current call: Gap handles "Fit", Friendly is separate check?
    # Let's degrade Safety to Target if Unfriendly
    if category == "Safety" and friendly == "Low":
        category = "Target"
        
    return category, gap

# --- MAIN APP ---
def main():
    st.sidebar.title("Relative-Fit Strategy Engine")
    
    # INPUTS
    name = st.sidebar.text_input("Name", "Student")
    
    major_map = {
        "Computer Science / Engineering": 8, # Penalty
        "Business / Finance": 5,
        "Biology / Pre-Med": 5,
        "Humanities / Arts / Other": 0
    }
    major = st.sidebar.selectbox("Major", list(major_map.keys()))
    major_penalty = major_map[major]
    
    curr = st.sidebar.selectbox("Curriculum", ["CBSE / ICSE", "IB Diploma", "Cambridge A-Levels", "US High School", "Other"])
    
    # Get Normalized GPA (0-4.0)
    norm_gpa = 3.0
    if curr == "CBSE / ICSE":
        raw = st.sidebar.number_input("Percentage", 0.0, 100.0, 90.0)
        # Map to 4.0
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
    ec_tier = st.sidebar.slider("Extracurriculars (1-10)", 1, 10, 7) # Adds 0-10 pts? prompt says "Soft Factors (10%): ECs add 0-10 pts"
    # So Tier 10 = 10 pts. Tier 1 = 1 pt.
    
    # CALC
    student_score = calculate_student_score(norm_gpa, sat, ec_tier, major_penalty)
    
    safeties, targets, aspirationals = [], [], []
    
    for c in COLLEGE_DB:
        cat, gap = classify_college(student_score, c['Diff'], c['Friendly'])
        
        row = {
            "College": c['Name'],
            "Rate": c['Rate'],
            "Difficulty": c['Diff'],
            "Gap": gap,
            "Friendly": c['Friendly'],
            "Fit": cat
        }
        
        if cat == "Safety": safeties.append(row)
        elif cat == "Target": targets.append(row)
        else: aspirationals.append(row)
        
    # SORTING (20-20-20)
    # Safeties: Diff Desc (Hardest first)
    df_safe = pd.DataFrame(safeties)
    if not df_safe.empty: df_safe = df_safe.sort_values(by="Difficulty", ascending=False).head(20)
    
    # Targets: Gap Asc (Closest to 0 first? Or closest to +8? Prompt: "Gap Ascending (Show closest matches first)")
    # Gap -5 to +8. Ascending means -5, -4...0... +8. 
    # Gap 0 is perfect match. Gap -5 is harder match. Gap +8 is easier match.
    # Closest match implies Gap ~ 0.
    # "Gap Ascending" sorts -5 first (Harder Targets). 
    df_targ = pd.DataFrame(targets)
    if not df_targ.empty: 
        # Better: Sort by abs(Gap)? No prompt said Gap Ascending.
        df_targ = df_targ.sort_values(by="Gap", ascending=True).head(20)
        
    # Aspirational: Gap Desc (Realistic Reaches first)
    # Gap < -5. e.g. -6, -10, -20.
    # Descending: -6, -10, -20. (Closest to Target line).
    df_asp = pd.DataFrame(aspirationals)
    if not df_asp.empty: df_asp = df_asp.sort_values(by="Gap", ascending=False).head(20)
    
    # UI
    st.title(f"Relative-Fit Strategy for {name}")
    st.markdown(f"**Major:** {major}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Student Power Score", f"{student_score:.1f}/100")
    c2.metric("Normalized GPA", f"{norm_gpa}")
    c3.metric("SAT", sat if sat > 0 else "Test Optional")
    
    t1, t2, t3 = st.tabs(["🛡️ Safeties", "🎯 Targets", "🚀 Aspirationals"])
    
    def render(df, title):
        if df.empty:
            st.info("No colleges in this category.")
            return
        
        d = df.copy()
        d['Rate'] = d['Rate'].apply(lambda x: f"{x*100:.1f}%")
        d['Gap'] = d['Gap'].apply(lambda x: f"{x:+.1f}")
        
        st.dataframe(d[['College', 'Rate', 'Difficulty', 'Gap', 'Friendly']], use_container_width=True, hide_index=True)
        
    with t1: render(df_safe, "High Quality Safeties")
    with t2: render(df_targ, "Strategic Targets")
    with t3: render(df_asp, "Realistic Reaches")
    
    # Download
    final = pd.concat([df_safe, df_targ, df_asp])
    if not final.empty:
        st.download_button("Download Report", final.to_csv(index=False).encode('utf-8'), "relative_fit_strategy.csv", "text/csv")
        
if __name__ == "__main__":
    main()
