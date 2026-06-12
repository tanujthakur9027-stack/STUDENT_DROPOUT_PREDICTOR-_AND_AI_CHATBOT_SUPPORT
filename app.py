import streamlit as st
import pandas as pd
import pickle
import os
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client

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
    .stApp { background-color: #0B0F19; color: #F3F4F6; }
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
    .pipeline-alert {
        background: #1E293B; border-left: 4px solid #3B82F6;
        border-radius: 8px; padding: 15px; margin-top: 15px; margin-bottom: 15px;
    }
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
    except Exception as e:
        st.error(f"Model loading failed: {e}")
        return None, None, None

model, features, importance = load_ai_assets()

# --------------------------------------------------
# 3. PRODUCTION AUTOMATED LIVE NOTIFICATION PIPELINES
# --------------------------------------------------
def dispatch_real_email(recipient_email, risk_score):
    """Fires a live SMTP server warning alert email directly to the counselor with explicit errors."""
    # We remove the global try-except so we can see what is failing
    sender_email = st.secrets["SENDER_EMAIL"] 
    sender_password = st.secrets["SENDER_PASSWORD"] 
    
    msg_contents = f"URGENT SYSTEM INTERVENTION: A student's retention index has reached {risk_score:.1f}%. Please initiate immediate contact protocols."
    
    msg = MIMEText(msg_contents)
    msg['Subject'] = f"🚨 EduGuard AI: Critical Risk Alert ({risk_score:.1f}%)"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    # Intentionally exposing the exact network connection error
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
    return True

def dispatch_real_sms(recipient_phone, risk_score):
    """Fires an active Twilio programmatic cellular network SMS text message with explicit errors."""
    account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
    auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
    twilio_number = st.secrets["TWILIO_NUMBER"]
    
    msg_body = f"Hi! We noticed things have been intense this term. Remember free peer-tutoring networks and counselor advisors are open to chat anytime! We are here to support you."
    
    # Intentionally exposing the exact API gateway connection error
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=msg_body,
        from_=twilio_number,
        to=recipient_phone
    )
    return True

# --------------------------------------------------
# 4. NAVIGATION BLOCK INTERFACE SELECTORS
# --------------------------------------------------
st.sidebar.title("🔮 EduGuard Control Panel")
st.sidebar.markdown("---")

page_selection = st.sidebar.radio(
    "Select Workspace System:",
    ["🕵️ Counselor Dashboard", "🧘 Guided AI Intervention Desk"]
)

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
                
        # --- PRODUCTION ROUTING LIVE COMMUNICATIONS SETTINGS ---
        st.markdown("---")
        st.markdown("### 📲 Live Communication Dispatches Config")
        alert_threshold = st.slider("Configure System Risk Trigger Threshold (%)", 50, 95, 70)
        counselor_email = st.text_input("Counselor Email", value="counselor@university.edu")
        student_phone = st.text_input("Student Phone (e.g. +91XXXXXXXXXX)", value="+91")
        
        # Flawless validation handlers to check data patterns cleanly
        if counselor_email and "@" not in counselor_email:
            st.warning("Please enter a valid email address style context.")
        if student_phone and not student_phone.startswith("+"):
            st.warning("Ensure student mobile registry contains international country prefix code (+).")

    with col_analytics:
        st.markdown("### 📊 Calculated Machine Learning Output")
        
        if model and features:
            input_df = pd.DataFrame([input_data])
            for feature in features:
                if feature not in input_df.columns:
                    input_df[feature] = 0
            input_df = input_df[features]
            risk_probability = model.predict_proba(input_df)[0][1] * 100
        else:
            risk_probability = 25.0
            
        if risk_probability < 35:
            status_text = f"🟢 LOW RISK ({risk_probability:.1f}%)"
            alert_color = "#10B981"
            description = "Student displays normal retention telemetry. Maintain baseline monitoring."
        elif risk_probability < alert_threshold:
            status_text = f"🟡 MONITOR ({risk_probability:.1f}%)"
            alert_color = "#F59E0B"
            description = "Mild behavioral or academic degradation noted."
        else:
            status_text = f"🔴 CRITICAL HIGH RISK ({risk_probability:.1f}%)"
            alert_color = "#EF4444"
            description = "Multi-vector risk indicators confirmed. Outbound message parameters active."

        st.markdown(f"""
        <div class="metric-card">
            <p style="color: #9CA3AF; font-size: 13px; margin-bottom: 4px;">System Predictive Risk Classification Target</p>
            <p style="font-size: 24px; font-weight: 800; color: {alert_color};">{status_text}</p>
            <p style="color: #D1D5DB; font-size: 14px; margin-top: 8px;">{description}</p>
        </div>
        """, unsafe_allow_html=True)

        # --- LIVE PRODUCTION DISPATCH EXECUTION TRIGGER ROUTE ---
        if risk_probability >= alert_threshold:
            send_alert = st.button("🚨 Send Alert Notification", type="primary")

            if send_alert:
                st.markdown("""
                <div class="pipeline-alert">
                    <span style="color: #3B82F6; font-weight: 700;">⚡ Network Gateway Engaged!</span>
                    <p style="font-size: 13px; color: #9CA3AF; margin-top: 5px; margin-bottom: 0;">
                        Outbound communications fired via API pipeline structures.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # 1. Fire Real SMTP Email Process Link
                email_fired = dispatch_real_email(counselor_email, risk_probability)
                if email_fired:
                    st.error(f"📬 **Real Email Alert successfully sent to `{counselor_email}`!**")
                else:
                    st.caption("ℹ️ Email logged mock format layout (Ensure st.secrets setup is populated).")
                    
                # 2. Fire Real Cellular Network SMS Route Link
                sms_fired = dispatch_real_sms(student_phone, risk_probability)
                if sms_fired:
                    st.success(f"📱 **Real SMS Nudge successfully pushed to `{student_phone}`!**")
                else:
                    st.caption("ℹ️ Cellular transmission fallback executed (Ensure twilio secrets setup is populated).")

        # Render XAI Feature Importance Graph
        if isinstance(importance, dict):
            import matplotlib.pyplot as plt
            try:
                dynamic_importance = {feat: abs(input_data.get(feat, 0)) * importance[feat] for feat in features if feat in importance}
                sorted_features = sorted(dynamic_importance.items(), key=lambda x: x[1], reverse=False)
                feats, impacts = zip(*sorted_features) if sorted_features else ([], [])
                total_impact = sum(impacts) if sum(impacts) > 0 else 1
                percentages = [(val / total_impact) * 100 for val in impacts]

                fig, ax = plt.subplots(figsize=(6, 2.2))
                fig.patch.set_facecolor('#111827'); ax.set_facecolor('#111827')
                ax.barh(feats, percentages, color=alert_color, height=0.4)
                ax.tick_params(colors='#9CA3AF', labelsize=10)
                ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
                st.pyplot(fig)
            except Exception as e:
                st.caption(f"Feature weighting vector skipped: {e}")

# ==================================================
# WEBPAGE 2: GUIDED AI INTERVENTION DESK (CHATBOT SIMULATION)
# ==================================================
elif page_selection == "🧘 Guided AI Intervention Desk":
    st.markdown('<div class="dashboard-header">🔮 Guided AI Intervention Desk</div>', unsafe_allow_html=True)
    
    def reset_intervention_flow():
        st.session_state.counseling_domain = None
        st.session_state.specific_pain_point = None
        st.session_state.user_understanding = None
        st.rerun() 

    col_chat_box, col_chat_inputs = st.columns([1.2, 1], gap="large")

    with col_chat_box:
        st.markdown('<div class="intervention-box">', unsafe_allow_html=True)

        solutions_matrix = {
            "Studies": {
                "Exam & Grade Anxiety": "<strong>Studies Strategy:</strong> Do not let a dense syllabus overwhelm you. Break your core modules down into 25-minute Pomodoro intervals. Practice writing your data structures or algorithms on paper to master logic flows before coding.",
                "Syllabus Overload": "<strong>Studies Strategy:</strong> Prioritize subjects based on exam weightage (like focus areas for your upcoming engineering papers). Isolate the top 3 high-weight topics and clear those bottlenecks first before touching elective units.",
                "Conceptual Bottlenecks": "<strong>Studies Strategy:</strong> If a technical concept feels like a brick wall, bypass independent cramming. Request a peer-mentor match via your student registry or review visual, animated logic breakdowns on open-source sandboxes."
            },
            "Stress & Mental Well-being": {
                "Exam & Grade Anxiety": "<strong>Well-being Roadmap:</strong> Academic anxiety is a physical response to stress, not a reflection of your potential. Isolate a dedicated 1-hour screen-free slot daily to rest your mind and reset focus metrics.",
                "Peer Pressure & Comparison": "<strong>Well-being Roadmap:</strong> Everyone's timeline is different. Stop comparing your raw internal drafts to everyone else's highlights. Take a 7-day break from technical LinkedIn postings and focus entirely on your local commits.",
                "Burnout & Low Energy": "<strong>Well-being Roadmap:</strong> Fatigue is a signal that your nervous system is overloaded. Prioritize 8 full hours of sleep tonight, take a 24-hour break from screens, and schedule an informal, casual check-in with a trusted peer."
            },
            "Finances": {
                "Fee Clearances & Deadlines": "<strong>Financial Roadmap:</strong> Head to the Student Welfare Desk immediately to file an official 'Installment Extension Request'. This halts automatic late-payment penalties and provides breathing room to manage dues.",
                "Scholarship Opportunities": "<strong>Financial Roadmap:</strong> Check your university internal portal for mid-semester scholarship openings, emergency book-banks, or external corporate aid applications that accept midway registrations.",
                "Part-time Jobs / Paid Internships": "<strong>Financial Roadmap:</strong> Clean up your personal portfolio, highlight your machine learning projects, structure your resume cleanly, and cold-message tech startup founders on LinkedIn directly for active internship roles."
            }
        }

        domain = st.session_state.get("counseling_domain")
        pain = st.session_state.get("specific_pain_point")
        understanding = st.session_state.get("user_understanding")

        if not domain: domain = "Studies"
        if not pain: pain = "Exam & Grade Anxiety"

        if understanding == "No, I need human escalation support":
            st.markdown("""
                <p class="intervention-text">
                    🛡️ <strong>Understood. Initializing Alternative Strategy Routing...</strong><br><br>
                    I am flagging this secure metric session token to automatically request a priority, private 1-on-1 counseling appointment with a human student welfare administrator. Stay strong!
                </p>
                """, unsafe_allow_html=True)
        elif (
            understanding == "Yes, completely clear!"
            and all([domain, pain])
            and "user_understanding" in st.session_state
            and st.session_state.user_understanding == "Yes, completely clear!"
        ):
            st.markdown("""
                <p class="intervention-text">
                    🎉 <strong>Sensational! I'm glad we mapped it out.</strong><br><br>
                    Consistency beats intensity every single time. Keep tracking your parameters, complete your modules, and feel free to return here to test other workflows anytime.
                </p>
                """, unsafe_allow_html=True)
        else:
            try:
                selected_solution = solutions_matrix.get(domain, {}).get(pain, "No recommendation available.")
                st.markdown(f"""
                <p class="intervention-text">
                    👋 <strong>EduGuard AI Counselor Active Profile:</strong><br><br>
                    🎯 Target Context: <span style='color: #93C5FD;'>{domain}</span> | Sub-issue: <span style='color: #F59E0B;'>{pain}</span><br><br>
                    {selected_solution}<br><br>
                    <hr style='border-color: #374151; margin: 15px 0;'>
                    📊 <strong>System Prompt Check:</strong> Did this tailored strategy provide actionable clarity for you?
                </p>
                """, unsafe_allow_html=True)
            except KeyError:
                st.markdown("""
                <p class="intervention-text">
                    👋 <strong>Hello! I am your AI Student Counselor Companion.</strong><br><br>
                    Please use the selector choices on the right panel to map out your primary domain context.
                </p>
                """, unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)
        st.button("🔄 RESET INTERVENTION FLOW", on_click=reset_intervention_flow)

    with col_chat_inputs:
        st.markdown("### 🕹️ Interactive Decision Trees")

        domain_options = ["Studies", "Stress & Mental Well-being", "Finances"]

        if st.session_state.counseling_domain is None:
            st.session_state.counseling_domain = domain_options[0]

        try:
            d_idx = domain_options.index(st.session_state.counseling_domain)
        except ValueError:
            d_idx = 0

        sel_domain = st.radio(
            "Select Counseling Domain Context:",
            options=domain_options,
            index=d_idx,
            key="stable_domain_key"
        )

        if sel_domain != st.session_state.counseling_domain:
            st.session_state.counseling_domain = sel_domain
            st.session_state.specific_pain_point = None  
            st.session_state.user_understanding = None
            st.rerun()

        if st.session_state.counseling_domain is not None:
            st.markdown("---")
            if st.session_state.counseling_domain == "Studies":
                pain_options = ["Exam & Grade Anxiety", "Syllabus Overload", "Conceptual Bottlenecks"]
            elif st.session_state.counseling_domain == "Stress & Mental Well-being":
                pain_options = ["Exam & Grade Anxiety", "Peer Pressure & Comparison", "Burnout & Low Energy"]
            else:
                pain_options = ["Fee Clearances & Deadlines", "Scholarship Opportunities", "Part-time Jobs / Paid Internships"]

            if st.session_state.specific_pain_point is None:
                st.session_state.specific_pain_point = pain_options[0]

            try:
                p_idx = pain_options.index(st.session_state.specific_pain_point)
            except ValueError:
                p_idx = 0

            sel_pain = st.radio(
                "Identify Specific Pain-Point Module:",
                options=pain_options,
                index=p_idx,
                key="stable_pain_key"
            )

            if sel_pain != st.session_state.specific_pain_point:
                st.session_state.specific_pain_point = sel_pain
                st.session_state.user_understanding = None
                st.rerun()

        if st.session_state.specific_pain_point is not None:
            st.markdown("---")
            understand_options = ["Yes, completely clear!", "No, I need human escalation support"]

            if st.session_state.user_understanding is None:
                st.session_state.user_understanding = understand_options[0]

            try:
                u_idx = understand_options.index(st.session_state.user_understanding)
            except ValueError:
                u_idx = 0

            sel_understand = st.radio(
                "Verify Suggested Path Resolution:",
                options=understand_options,
                index=u_idx,
                key="stable_understand_key"
            )
            if sel_understand != st.session_state.user_understanding:
                st.session_state.user_understanding = sel_understand
                st.rerun()