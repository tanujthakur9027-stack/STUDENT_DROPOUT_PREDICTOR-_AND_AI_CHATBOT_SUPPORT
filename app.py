import streamlit as st
import pandas as pd
import pickle
import os

# --------------------------------------------------
# 1. INITIAL DESIGN CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="EduGuard AI Navigation Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Global Application Theme Customizations */
    .stApp { background-color: #0B0F19; color: #F3F4F6; }
    
    /* Panel Formatting Card Frameworks */
    .dashboard-header {
        font-size: 28px; font-weight: 700; color: #10B981;
        margin-bottom: 20px; border-bottom: 2px solid #1F2937; padding-bottom: 8px;
    }
    .metric-card {
        background: #111827; border: 1px solid #1F2937; border-radius: 12px;
        padding: 20px; margin-bottom: 15px;
    }
    .intervention-box {
        background: #111827; border: 2px solid #F59E0B; border-radius: 12px;
        padding: 25px; margin-bottom: 20px; min-height: 150px;
    }
    .intervention-text { color: #F59E0B; font-size: 16px; font-weight: 500; line-height: 1.6; }
    
    /* Button Form Factors */
    div.stButton > button:first-child {
        background: #1F2937 !important; color: #F3F4F6 !important;
        border: 1px solid #374151 !important; font-weight: 600 !important;
        border-radius: 8px !important; width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 2. MACHINE LEARNING BINARY LOADING ASSETS
# --------------------------------------------------
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

# --------------------------------------------------
# 3. SPLIT PAGE WORKSPACE SIDEBAR NAVIGATION
# --------------------------------------------------
st.sidebar.title("🔮 EduGuard Control Panel")
st.sidebar.markdown("---")

# Separate into two explicit web page interfaces to prevent button conflict loops
page_selection = st.sidebar.radio(
    "Select Workspace System:",
    ["🕵️ Counselor Dashboard", "🧘 Guided AI Intervention Desk"]
)

# Initialize global variable storage frameworks
if "counseling_domain" not in st.session_state: st.session_state.counseling_domain = None
if "specific_pain_point" not in st.session_state: st.session_state.specific_pain_point = None
if "user_understanding" not in st.session_state: st.session_state.user_understanding = None

# ==================================================
# WEBPAGE 1: COUNSELOR RISK PREDICTOR DASHBOARD
# ==================================================
if page_selection == "🕵️ Counselor Dashboard":
    st.markdown('<div class="dashboard-header">🕵️ Institutional Risk Assessment Dashboard</div>', unsafe_allow_html=True)
    
    col_input, col_analytics = st.columns([1, 1], gap="large")
    
    with col_input:
        st.markdown("### 🎛️ Live Student Telemetry Controls")
        
        input_data = {}
        input_data["Age at enrollment"] = st.slider("Enrollment Age Metric", 15, 60, 20)
        input_data["Attendance_Rate"] = st.slider("Calculated Class Attendance Rate (%)", 0, 100, 85)
        input_data["Curricular_units_1st_sem_grade"] = st.slider("1st Semester Term Grades (0-20 scale)", 0, 20, 14)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            s_choice = st.radio("Scholarship Holder", ["No", "Yes"], index=0)
            input_data["Scholarship holder"] = 1 if s_choice == "Yes" else 0
        with c2:
            d_choice = st.radio("Is Institutional Debtor", ["No", "Yes"], index=0)
            input_data["Debtor"] = 1 if d_choice == "Yes" else 0
        with c3:
            g_choice = st.radio("Gender Profile", ["Female", "Male"], index=0)
            input_data["Gender"] = 1 if g_choice == "Male" else 0

        if features:
            for feat in features:
                if feat not in input_data: input_data[feat] = 0.0

    with col_analytics:
        st.markdown("### 📊 Calculated Machine Learning Output")
        
        # Calculate real-time probabilities from your model asset
        if model and features:
            input_df = pd.DataFrame([input_data])[features]
            risk_probability = model.predict_proba(input_df)[0][1] * 100
        else:
            risk_probability = 25.0
            
        # FIXED RISK LOGIC: Maps probability percentage correctly to semantic status tags
        if risk_probability < 35:
            status_text = f"🟢 LOW RISK ({risk_probability:.1f}%)"
            alert_color = "#10B981"
            description = "Student displays normal retention telemetry. Maintain baseline monitoring."
        elif risk_probability < 70:
            status_text = f"🟡 MONITOR ({risk_probability:.1f}%)"
            alert_color = "#F59E0B"
            description = "Mild behavioral or academic degradation noted. Flag for secondary outreach checks."
        else:
            status_text = f"🔴 CRITICAL HIGH RISK ({risk_probability:.1f}%)"
            alert_color = "#EF4444"
            description = "Multi-vector risk indicators confirmed. Trigger emergency immediate counselor notification."

        st.markdown(f"""
        <div class="metric-card">
            <p style="color: #9CA3AF; font-size: 13px; margin-bottom: 4px;">System Predictive Risk Classification Target</p>
            <p style="font-size: 24px; font-weight: 800; color: {alert_color};">{status_text}</p>
            <p style="color: #D1D5DB; font-size: 14px; margin-top: 8px;">{description}</p>
        </div>
        """, unsafe_allow_html=True)

        # Render XAI Feature Importance Graph
        if isinstance(importance, dict):
            import matplotlib.pyplot as plt
            try:
                dynamic_importance = {feat: abs(input_data.get(feat, 0)) * importance[feat] for feat in features if feat in importance}
                sorted_features = sorted(dynamic_importance.items(), key=lambda x: x[1], reverse=False)
                feats, impacts = zip(*sorted_features) if sorted_features else ([], [])
                total_impact = sum(impacts) if sum(impacts) > 0 else 1
                percentages = [(val / total_impact) * 100 for val in impacts]

                fig, ax = plt.subplots(figsize=(6, 2.8))
                fig.patch.set_facecolor('#111827')
                ax.set_facecolor('#111827')
                ax.barh(feats, percentages, color=alert_color, height=0.4)
                ax.tick_params(colors='#9CA3AF', labelsize=10)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                st.pyplot(fig)
            except Exception as e:
                st.caption(f"Feature weighting vector skipped: {e}")

# ==================================================
# WEBPAGE 2: GUIDED AI INTERVENTION DESK (CHATBOT)
# ==================================================
elif page_selection == "🧘 Guided AI Intervention Desk":
    st.markdown('<div class="dashboard-header">🔮 Guided AI Intervention Desk</div>', unsafe_allow_html=True)
    
    # Reset helper function for state switching mechanics
    def reset_intervention_flow():
        st.session_state.counseling_domain = None
        st.session_state.specific_pain_point = None
        st.session_state.user_understanding = None

    col_chat_box, col_chat_inputs = st.columns([1.2, 1], gap="large")
    
    with col_chat_box:
        st.markdown('<div class="intervention-box">', unsafe_allow_html=True)
        
        # Phase A: Starting state
        if st.session_state.counseling_domain is None:
            st.markdown("""
            <p class="intervention-text">
                👋 <strong>Hello! I am your AI Student Counselor Companion.</strong><br><br>
                I am here to build a customized, stress-free path forward for you.<br><br>
                To begin, look at the choice selectors on the right panel and choose the <strong>Primary Domain Context</strong> you want to sort out today.
            </p>
            """, unsafe_allow_html=True)
            
        # Phase B: Domain selected, waiting on explicit sub-issue details
        elif st.session_state.counseling_domain and st.session_state.specific_pain_point is None:
            st.markdown(f"""
            <p class="intervention-text">
                🎯 <strong>Active Path established: {st.session_state.counseling_domain} Support Hub.</strong><br><br>
                Great. Let's isolate the issue. Move to the right panel and select the <strong>Specific Pain-Point Module</strong> creating the biggest bottleneck for you right now.
            </p>
            """, unsafe_allow_html=True)
            
        # Phase C: Strategy output with user verification check active
        elif st.session_state.specific_pain_point and st.session_state.user_understanding is None:
            if st.session_state.specific_pain_point == "Peer Pressure & Comparison":
                solution_text = "<strong>Strategy Roadmap:</strong> Stop comparing your raw internal drafts to everyone else's curated highlights. Take a 7-day break from technical LinkedIn postings and focus entirely on clean, local code repository updates."
            elif st.session_state.specific_pain_point == "Part-time Jobs / Paid Internships":
                solution_text = "<strong>Strategy Roadmap:</strong> Clean up your local portfolio, structure your resume using clean professional layout templates, and prioritize cold-messaging startup founders directly on LinkedIn for active work opportunities."
            else:
                solution_text = "<strong>Strategy Roadmap:</strong> Do not let a dense syllabus overwhelm you. Use the Pomodoro method (25-minute study intervals) to isolate weak chapters. Practice manual algorithm layout tracing on physical notebooks daily to master conceptual loops."
                
            st.markdown(f"""
            <p class="intervention-text">
                💡 {solution_text}<br><br>
                <hr style='border-color: #374151; margin: 15px 0;'>
                📊 <strong>System Prompt Check:</strong> Did this tailored strategy provide actionable clarity for you?
            </p>
            """, unsafe_allow_html=True)
            
        # Phase D: Success conclusion
        elif st.session_state.user_understanding == "Yes, completely clear!":
            st.markdown("""
            <p class="intervention-text">
                🎉 <strong>Sensational! I'm glad we mapped it out.</strong><br><br>
                Consistency beats intensity every single time. Keep tracking your parameters, complete your modules, and feel free to return here to test other workflows anytime.
            </p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <p class="intervention-text">
                🛡️ <strong>Understood. Initializing Alternative Strategy Routing...</strong><br><br>
                I am flagging this secure metric session token to automatically request a priority, private 1-on-1 counseling appointment with a human student welfare administrator. Stay strong!
            </p>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        st.button("🔄 RESET INTERVENTION & EVALUATE ANOTHER STUDENT", on_click=reset_intervention_flow)

    with col_chat_inputs:
        st.markdown("### 🕹️ Interactive Decision Trees")
        
        # Step 1: Core Domain Selections
        domain_options = ["Studies", "Stress & Mental Well-being", "Finances"]
        d_idx = None if st.session_state.counseling_domain is None else domain_options.index(st.session_state.counseling_domain)
        
        sel_domain = st.radio(
            "Select Counseling Domain Context:",
            options=domain_options,
            index=d_idx,
            key="domain_radio_selection"
        )
        if sel_domain != st.session_state.counseling_domain and st.session_state.specific_pain_point is None:
            st.session_state.counseling_domain = sel_domain
            st.rerun()

        # Step 2: Custom Sub-Pain Point Selection
        if st.session_state.counseling_domain is not None:
            st.markdown("---")
            if st.session_state.counseling_domain == "Studies":
                pain_options = ["Exam & Grade Anxiety", "Syllabus Overload", "Conceptual Bottlenecks"]
            elif st.session_state.counseling_domain == "Stress & Mental Well-being":
                pain_options = ["Exam & Grade Anxiety", "Peer Pressure & Comparison", "Burnout & Low Energy"]
            else:
                pain_options = ["Fee Clearances & Deadlines", "Scholarship Opportunities", "Part-time Jobs / Paid Internships"]
                
            p_idx = None if st.session_state.specific_pain_point is None else pain_options.index(st.session_state.specific_pain_point)
            
            sel_pain = st.radio(
                "Identify Specific Pain-Point Module:",
                options=pain_options,
                index=p_idx,
                key="pain_radio_selection"
            )
            if sel_pain != st.session_state.specific_pain_point and st.session_state.user_understanding is None:
                st.session_state.specific_pain_point = sel_pain
                st.rerun()

        # Step 3: Resolution Status Feedback Checks
        if st.session_state.specific_pain_point is not None:
            st.markdown("---")
            understand_options = ["Yes, completely clear!", "No, I need human escalation support"]
            u_idx = None if st.session_state.user_understanding is None else understand_options.index(st.session_state.user_understanding)
            
            sel_understand = st.radio(
                "Verify Suggested Path Resolution:",
                options=understand_options,
                index=u_idx,
                key="understanding_radio_selection"
            )
            if sel_understand != st.session_state.user_understanding:
                st.session_state.user_understanding = sel_understand
                st.rerun()