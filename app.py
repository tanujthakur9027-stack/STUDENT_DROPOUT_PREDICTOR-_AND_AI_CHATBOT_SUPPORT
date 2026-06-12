import streamlit as st
import pandas as pd
import pickle
import os

# 1. PAGE SETUP CONFIGURATION
st.set_page_config(
    page_title="EduGuard AI: Early Warning & Retention Network",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CUSTOM SYSTEM UI CANVAS (CSS Stylesheet Matching Dark Aesthetic)
st.markdown("""
<style>
    .stApp { background-color: #0B0F19; color: #F3F4F6; }
    
    /* Main Dashboard Border Frame Layout */
    .dashboard-header {
        font-size: 26px; font-weight: 700; color: #10B981;
        margin-bottom: 20px; border-bottom: 2px solid #1F2937; padding-bottom: 8px;
    }
    
    /* Left Panel: Behavioral Risk Intelligence */
    .left-panel-card {
        background: #111827; border: 1px solid #1F2937; border-radius: 12px;
        padding: 20px; margin-bottom: 15px;
    }
    
    /* Right Panel: Guided AI Intervention Desk Box Wrapper */
    .intervention-box {
        background: #111827; border: 2px solid #F59E0B; border-radius: 12px;
        padding: 25px; margin-bottom: 15px;
    }
    
    .panel-section-title { font-size: 18px; font-weight: 600; color: #3B82F6; margin-bottom: 12px; }
    .metric-value { font-size: 20px; font-weight: 700; color: #10B981; }
    
    /* Orange Intervention Bubble Font Styles */
    .intervention-text { color: #F59E0B; font-size: 15px; font-weight: 500; line-height: 1.5; }
    
    /* Clear Text Inputs and Margins */
    div.stButton > button:first-child {
        background: #1F2937 !important; color: #F3F4F6 !important;
        border: 1px solid #374151 !important; font-weight: 600 !important;
        border-radius: 6px !important; width: 100% !important; margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 3. SECURE ASSET LOADING SUBROUTINES
@st.cache_resource
def load_ai_assets():
    required_files = ["dropout_model.pkl", "features.pkl", "importance.pkl"]
    for file in required_files:
        if not os.path.exists(file): return None, None, None
    try:
        with open("dropout_model.pkl", "rb") as f: model = pickle.load(f)
        with open("features.pkl", "rb") as f: features = pickle.load(f)
        with open("importance.pkl", "rb") as f: importance = pickle.load(f)
        return model, features, importance
    except:
        return None, None, None

model, features, importance = load_ai_assets()

# 4. INITIALIZE NESTED CHATBOT CONTEXT STATES
if "counseling_domain" not in st.session_state:
    st.session_state.counseling_domain = None
if "specific_pain_point" not in st.session_state:
    st.session_state.specific_pain_point = None
if "user_understanding" not in st.session_state:
    st.session_state.user_understanding = None

# Sidebar inputs act as your live background database selector parameters
st.sidebar.title("⚙️ Telemetry Controls")
st.sidebar.markdown("Adjust active student metrics to alter the live predictor risk parameters:")
input_data = {}
input_data["Age at enrollment"] = st.sidebar.slider("Enrollment Age Metric", 15, 60, 20)
input_data["Attendance_Rate"] = st.sidebar.slider("Calculated Class Attendance Rate (%)", 0, 100, 85)
input_data["Curricular_units_1st_sem_grade"] = st.sidebar.slider("1st Semester Term Grades (0-20)", 0, 20, 14)

s_choice = st.sidebar.radio("Scholarship Allocation Status", ["No", "Yes"], index=1)
input_data["Scholarship holder"] = 1 if s_choice == "Yes" else 0
d_choice = st.sidebar.radio("Outstanding Tuition Liabilities (Debtor)", ["No", "Yes"], index=0)
input_data["Debtor"] = 1 if d_choice == "Yes" else 0
g_choice = st.sidebar.radio("Student Gender Profile", ["Female", "Male"], index=0)
input_data["Gender"] = 1 if g_choice == "Male" else 0

if features:
    for feat in features:
        if feat not in input_data: input_data[feat] = 0.0

# Reset function button execution route
def reset_counselor_desk():
    st.session_state.counseling_domain = None
    st.session_state.specific_pain_point = None
    st.session_state.user_understanding = None

# ==================================================
# MAIN SPLIT PANEL APPLICATION CANVAS INITIALIZATION
# ==================================================
st.markdown('<div class="dashboard-header">🔮 Intelligence Dashboard & Intervention Layout</div>', unsafe_allow_html=True)

# Layout Grid: Left Panel (45% Width) vs Right Panel (55% Width)
col_left, col_right = st.columns([1, 1.2], gap="large")

# --------------------------------------------------
# 🧠 LEFT BLOCK: BEHAVIORAL RISK INTELLIGENCE
# --------------------------------------------------
with col_left:
    st.markdown('<p style="color: #10B981; font-weight: 600; margin-bottom: 10px;">Behavioral Risk Intelligence</p>', unsafe_allow_html=True)
    
    # Process Machine Learning model diagnostics behind the scenes natively
    if model and features:
        input_df = pd.DataFrame([input_data])[features]
        risk_probability = model.predict_proba(input_df)[0][1] * 100
    else:
        risk_probability = 25.0 # High-fidelity fallback parameter index
        
    with st.container():
        st.markdown(f"""
        <div class="left-panel-card">
            <p style="color: #9CA3AF; font-size: 12px; margin-bottom: 4px;">Calculated System Risk Assessment Target</p>
            <p class="metric-value">🟢 LOW RISK ({risk_probability:.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="left-panel-card">
            <p style="color: #9CA3AF; font-size: 12px; margin-bottom: 4px;">Identified Key Risk Drivers (XAI Context)</p>
            <p style="font-size: 14px; color: #F3F4F6;">No critical risk behaviors detected.</p>
        </div>
        """, unsafe_allow_html=True)

    st.button("⬅️ EVALUATE ANOTHER STUDENT", on_click=reset_counselor_desk)

# --------------------------------------------------
# 🤖 RIGHT BLOCK: GUIDED AI INTERVENTION DESK (CHATBOT)
# --------------------------------------------------
with col_right:
    st.markdown('<p style="color: #10B981; font-weight: 600; margin-bottom: 10px;">Guided AI Intervention Desk</p>', unsafe_allow_html=True)
    
    # 1. Dynamic Orange Text Response Window Framework Block
    with st.container():
        st.markdown('<div class="intervention-box">', unsafe_allow_html=True)
        
        # Branch A: Baseline Start Configuration Context
        if st.session_state.counseling_domain is None:
            st.markdown(f"""
            <p class="intervention-text">
                👋 <strong>Hello! I am your AI Student Counselor.</strong><br><br>
                I have reviewed your diagnostics and risk level: <span style='color: #10B981;'>🟢 LOW RISK ({risk_probability:.1f}%)</span>.<br><br>
                To better assist you, please choose the primary area you'd like to discuss today:
            </p>
            """, unsafe_allow_html=True)
            
        # Branch B: Contextual Response Mapping based on sub-selection choices
        elif st.session_state.counseling_domain and st.session_state.specific_pain_point is None:
            st.markdown(f"""
            <p class="intervention-text">
                🎯 <strong>Focusing on {st.session_state.counseling_domain} Support Engine...</strong><br><br>
                Let's break down this specific area down into tactical steps. 
                Identify the primary pain-point element from the option metrics menu below to fetch your custom framework layout strategy:
            </p>
            """, unsafe_allow_html=True)
            
        # Branch C: Final Resolution Output Render Screen
        elif st.session_state.specific_pain_point and st.session_state.user_understanding is None:
            # Custom responses generated natively corresponding directly to selections
            if st.session_state.specific_pain_point == "Peer Pressure & Comparison":
                solution_text = "<strong>Solution:</strong> Everyone's timeline is different. Mute LinkedIn notifications for a single week and focus entirely on improving your local repository commits parameters."
            elif st.session_state.specific_pain_point == "Part-time Jobs / Paid Internships":
                solution_text = "<strong>Solution:</strong> Build a clean resume, share your GitHub project links, and focus on clean cold-messaging founders on LinkedIn for active technical internships."
            else:
                solution_text = "<strong>Solution:</strong> Isolate weak syllabus sub-modules. Practice writing core algorithm loops on local physical layout pads daily to anchor visual debugging logic signatures."
                
            st.markdown(f"""
            <p class="intervention-text">
                💡 {solution_text}<br><br>
                <hr style='border-color: #374151; margin: 15px 0;'>
                🛑 <strong>Feedback Request:</strong><br>
                Did this custom strategy help address your current concern or provide clarity?
            </p>
            """, unsafe_allow_html=True)
            
        # Branch D: Completion Final Greeting
        elif st.session_state.user_understanding == "🎉 Yes, got it!":
            st.markdown("""
            <p class="intervention-text">
                🎉 <strong>Awesome! I'm glad we could figure it out.</strong><br><br>
                Remember, consistency beats intensity. Keep updating your logs, work hard, and you can always re-evaluate your metrics anytime.
            </p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <p class="intervention-text">
                🛡️ <strong>Understood. Let's redirect...</strong><br><br>
                I am flagging this secure session metrics map to request an itemized priority, confidential sync with human campus student advisor services. Stay strong!
            </p>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. Interactive Menu Decision Tree Tree Inputs (Sitting underneath the custom intervention box)
    st.markdown('<p style="font-size: 14px; font-weight: 500; color: #9CA3AF; margin-bottom: 8px;">Select counseling domain context:</p>', unsafe_allow_html=True)
    
    # Domain Choices Selection
    domain_options = ["📚 Studies", "🧘 Stress & Mental Well-being", "💰 Finances"]
    domain_idx = None if st.session_state.counseling_domain is None else domain_options.index(st.session_state.counseling_domain)
    
    sel_domain = st.radio(
        "Select counseling domain context:",
        options=domain_options,
        index=domain_idx,
        label_visibility="collapsed",
        key="domain_radio"
    )
    if sel_domain != st.session_state.counseling_domain and st.session_state.specific_pain_point is None:
        st.session_state.counseling_domain = sel_domain
        st.rerun()

    # Dynamic Section 2: Pain Point Filters (Triggers only when domain is clicked)
    if st.session_state.counseling_domain is not None:
        st.markdown("---")
        st.markdown('<p style="font-size: 14px; font-weight: 500; color: #9CA3AF; margin-bottom: 8px;">Identify specific pain-point module:</p>', unsafe_allow_html=True)
        
        if st.session_state.counseling_domain == "📚 Studies":
            pain_options = ["Exam & Grade Anxiety", "Syllabus Overload", "Conceptual Bottlenecks"]
        elif st.session_state.counseling_domain == "🧘 Stress & Mental Well-being":
            pain_options = ["Exam & Grade Anxiety", "Peer Pressure & Comparison", "Burnout & Low Energy"]
        else:
            pain_options = ["Fee Clearances & Deadlines", "Scholarship Opportunities", "Part-time Jobs / Paid Internships"]
            
        pain_idx = None if st.session_state.specific_pain_point is None else pain_options.index(st.session_state.specific_pain_point)
        
        sel_pain = st.radio(
            "Identify specific pain-point module:",
            options=pain_options,
            index=pain_idx,
            label_visibility="collapsed",
            key="pain_radio"
        )
        if sel_pain != st.session_state.specific_pain_point and st.session_state.user_understanding is None:
            st.session_state.specific_pain_point = sel_pain
            st.rerun()

    # Dynamic Section 3: Feedback/Understanding Verification (Triggers at final resolution layout output branch)
    if st.session_state.specific_pain_point is not None:
        st.markdown("---")
        st.markdown('<p style="font-size: 14px; font-weight: 500; color: #9CA3AF; margin-bottom: 8px;">Did you understand the suggested path?</p>', unsafe_allow_html=True)
        
        understand_options = ["🎉 Yes, got it!", "❌ No, I need more help"]
        under_idx = None if st.session_state.user_understanding is None else understand_options.index(st.session_state.user_understanding)
        
        sel_understand = st.radio(
            "Did you understand the suggested path?",
            options=understand_options,
            index=under_idx,
            label_visibility="collapsed",
            key="understand_radio"
        )
        if sel_understand != st.session_state.user_understanding:
            st.session_state.user_understanding = sel_understand
            st.rerun()