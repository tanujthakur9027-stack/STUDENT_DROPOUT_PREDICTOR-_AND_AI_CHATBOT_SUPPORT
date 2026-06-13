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
    page_icon="",
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
    """Fires a live SMTP server warning alert email directly to the counselor."""
    try:
        sender_email = st.secrets["SENDER_EMAIL"] 
        sender_password = st.secrets["SENDER_PASSWORD"] 
    except Exception:
        return False
        
    msg_contents = f"URGENT SYSTEM INTERVENTION: A student's retention index has reached {risk_score:.1f}%. Please initiate immediate contact protocols."
    
    msg = MIMEText(msg_contents)
    msg['Subject'] = f" EduGuard AI: Critical Risk Alert ({risk_score:.1f}%)"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True
    except Exception as e:
        st.sidebar.warning(f"SMTP Log Network Skip: {e}")
        return False

def dispatch_real_sms(recipient_phone, risk_score):
    """Fires an active Twilio programmatic cellular network SMS text message."""
    try:
        account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
        twilio_number = st.secrets["TWILIO_NUMBER"]
    except Exception:
        return False
        
    msg_body = f"Hi! We noticed things have been intense this term. Remember free peer-tutoring networks and counselor advisors are open to chat anytime! We are here to support you."
    
    try:
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=msg_body,
            from_=twilio_number,
            to=recipient_phone
        )
        return True
    except Exception as e:
        st.sidebar.warning(f"Cellular Gateway Link Skip: {e}")
        return False

# ==================================================
# MAIN SCREEN: COUNSELOR RISK PREDICTOR DASHBOARD
# ==================================================
st.markdown('<div class="dashboard-header"> Eduguard Risk Intelligence & Alert Center </div>', unsafe_allow_html=True)

col_input, col_analytics = st.columns([1, 1], gap="large")

with col_input:
    st.markdown("### Students Diagnostic & Performance Matrix")
    
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
    st.markdown("###  Live Communication Dispatches Config")
    alert_threshold = st.slider("Configure System Risk Trigger Threshold (%)", 50, 95, 70)
    counselor_email = st.text_input("Counselor Email", value="counselor@university.edu")
    student_phone = st.text_input("Student Phone (e.g. +91XXXXXXXXXX)", value="+91")
    
    if counselor_email and "@" not in counselor_email:
        st.warning("Please enter a valid email address style context.")
    if student_phone and not student_phone.startswith("+"):
        st.warning("Ensure student mobile registry contains international country prefix code (+).")

with col_analytics:
    st.markdown("###  Calculated Machine Learning Output")
    
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
                <span style="color: #3B82F6; font-weight: 700;"> Network Gateway Engaged!</span>
                <p style="font-size: 13px; color: #9CA3AF; margin-top: 5px; margin-bottom: 0;">
                    Outbound communications fired via API pipeline structures.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # 1. Fire Real SMTP Email Process Link
            email_fired = dispatch_real_email(counselor_email, risk_probability)
            if email_fired:
                st.error(f" **Real Email Alert successfully sent to `{counselor_email}`!**")
            else:
                st.caption(" Email fallback executed (Verify your local .streamlit/secrets.toml values).")
                
            # 2. Fire Real Cellular Network SMS Route Link
            sms_fired = dispatch_real_sms(student_phone, risk_probability)
            if sms_fired:
                st.success(f" **Real SMS Nudge successfully pushed to `{student_phone}`!**")
            else:
                st.caption("ℹ Cellular transmission fallback executed (Verify your local .streamlit/secrets.toml values).")

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