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

# 2. CUSTOM SYSTEM UI CANVAS (CSS Stylesheet)
st.markdown("""
<style>
    .stApp { background-color: #0B0F19; color: #F3F4F6; }
    .landing-card {
        background: #111827; border: 1px solid #1F2937; border-radius: 16px;
        padding: 40px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        margin: auto; max-width: 650px;
    }
    .gradient-title {
        font-size: 38px; font-weight: 800;
        background: linear-gradient(135deg, #A7F3D0 0%, #93C5FD 50%, #C084FC 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        line-height: 1.3; margin-bottom: 15px;
    }
    .subtext { font-size: 15px; color: #9CA3AF; line-height: 1.6; margin-bottom: 25px; }
    .column-header {
        font-size: 18px; font-weight: 600; color: #93C5FD;
        margin-bottom: 15px; border-bottom: 1px solid #1F2937; padding-bottom: 6px;
    }
    .nudge-box {
        background: #1E293B; border-left: 4px solid #3B82F6;
        border-radius: 8px; padding: 15px; margin-top: 10px;
    }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #A7F3D0 0%, #93C5FD 100%) !important;
        color: #0F172A !important; font-weight: 700 !important;
        border: none !important; padding: 10px 20px !important;
        border-radius: 8px !important; transition: all 0.3s ease !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. SECURE ASSET LOADING
@st.cache_resource
def load_ai_assets():
    required_files = ["dropout_model.pkl", "features.pkl", "importance.pkl"]
    for file in required_files:
        if not os.path.exists(file):
            return None, None, None
    try:
        with open("dropout_model.pkl", "rb") as f: model = pickle.load(f)
        with open("features.pkl", "rb") as f: features = pickle.load(f)
        with open("importance.pkl", "rb") as f: importance = pickle.load(f)
        return model, features, importance
    except:
        return None, None, None

model, features, importance = load_ai_assets()

# 4. MULTI-USER SYSTEM NAVIGATION BLOCK
modes = [
    "📌 Home: Core Portal", 
    "🕵️ Counselor Console: Risk Engine", 
    "💬 Student Safe-Space: Anon Chatbot",
    "🤖 Counselor Smart Assistant: Search"
]

if "view_state" not in st.session_state:
    st.session_state.view_state = "📌 Home: Core Portal"

try:
    default_sidebar_index = modes.index(st.session_state.view_state)
except ValueError:
    default_sidebar_index = 0

st.sidebar.title("🔐 Authentication Guard")
user_role = st.sidebar.selectbox("Select Access Clearance", ["Student Access", "Authorized Counselor / Admin"])

st.sidebar.markdown("---")
st.sidebar.subheader("🧭 Terminal Navigation")

# Dynamic Menu Filtering based on Selected User Role Persona
if user_role == "Student Access":
    allowed_modes = ["📌 Home: Core Portal", "💬 Student Safe-Space: Anon Chatbot"]
else:
    allowed_modes = ["📌 Home: Core Portal", "🕵️ Counselor Console: Risk Engine", "🤖 Counselor Smart Assistant: Search"]

app_mode = st.sidebar.radio("Navigate Active Module", allowed_modes)

if app_mode != st.session_state.view_state:
    st.session_state.view_state = app_mode

# ==================================================
# MODULE 1: WELCOME PORTAL COVER
# ==================================================
if st.session_state.view_state == "📌 Home: Core Portal":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="landing-card">
        <div style='font-size: 55px; margin-bottom: 15px;'>🛡️</div>
        <div class="gradient-title">EduGuard AI Retention Framework</div>
        <div class="subtext">
            An automated early-warning weather forecast pipeline for academic success. 
            Detecting student attrition patterns and distributing immediate counseling safety nets.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# MODULE 2: COUNSELOR RISK DASHBOARD & NOTIFICATION ENGINE
# ==================================================
elif st.session_state.view_state == "🕵️ Counselor Console: Risk Engine":
    st.markdown("## 🕵️ Academic Early-Warning Diagnostic Console")
    
    col1, col2 = st.columns([1.1, 1], gap="large")

    with col1:
        st.markdown('<div class="column-header">Input Target Student Telemetry</div>', unsafe_allow_html=True)
        input_data = {}
        sub_col_l, sub_col_r = st.columns(2)
        
        with sub_col_l:
            input_data["Age at enrollment"] = st.slider("Enrollment Age Metric", 15, 60, 20)
            input_data["Attendance_Rate"] = st.slider("Calculated Class Attendance Rate (%)", 0, 100, 85)
            input_data["Curricular_units_1st_sem_grade"] = st.slider("1st Semester Term Grades (0-20)", 0, 20, 14)

        with sub_col_r:
            s_choice = st.radio("Scholarship Allocation Status", ["No", "Yes"], horizontal=True)
            input_data["Scholarship holder"] = 1 if s_choice == "Yes" else 0
            d_choice = st.radio("Outstanding Tuition Liabilities (Debtor)", ["No", "Yes"], horizontal=True)
            input_data["Debtor"] = 1 if d_choice == "Yes" else 0
            g_choice = st.radio("Student Gender Profile", ["Female", "Male"], horizontal=True)
            input_data["Gender"] = 1 if g_choice == "Male" else 0

        # Fill potential feature layout list anomalies safely
        if features:
            for feat in features:
                if feat not in input_data: input_data[feat] = 0.0

        st.markdown("---")
        st.subheader("🚨 Automated Notification Dispatch Settings")
        alert_threshold = st.slider("Configure Risk Alert Trigger Threshold (%)", 50, 95, 70)
        target_email = st.text_input("Counselor Emergency Notification Destination Email", "counselor.support@university.edu")

        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("EXECUTE SYSTEM RISK DIAGNOSTIC")

    with col2:
        st.markdown('<div class="column-header">AI Predictive Diagnostics Engine Output</div>', unsafe_allow_html=True)

        if analyze_btn and model:
            input_df = pd.DataFrame([input_data])[features]
            risk_probability = model.predict_proba(input_df)[0][1] * 100

            m1, m2 = st.columns(2)
            m1.metric(label="Calculated Attrition Risk", value=f"{risk_probability:.1f}%")

            if risk_probability < 35:
                m2.success("🟢 PROFILE STABLE")
            elif risk_probability < alert_threshold:
                m2.warning("🟡 ELEVATED STATUS")
            else:
                m2.error("🔴 CRITICAL WARNING ALERT")
                
                # --- AUTOMATED WARNING COMMUNICATIONS SYSTEM PIPELINE ---
                st.markdown("""<div class='nudge-box'><strong>⚡ Automated Communication Pipeline Fired!</strong></div>""", unsafe_allow_html=True)
                
                # 1. Dispatching Counselor Alert Hook
                st.info(f"📬 **Email Notification Sent to `{target_email}`**\n\n*Content:* ALERT: Student profile engagement drop detected. Attrition Risk profile index calculated at **{risk_probability:.1f}%**, bypassing your {alert_threshold}% safety boundary threshold limit. Action Required.")
                
                # 2. Dispatching Student Nudge Hook
                st.success(f"📱 **Supportive SMS Nudge Dispatched to Student Mobile Registry**\n\n*Content:* Hi! We noticed things have been a bit busy lately and you've missed a couple of checks. Just a reminder that free peer-tutoring networks and counseling sessions are open daily on the portal! Reply directly if you need to talk.")

            # Custom Matplotlib feature rendering logic goes beneath seamlessly
            if isinstance(importance, dict):
                import matplotlib.pyplot as plt
                dynamic_importance = {feat: abs(input_data.get(feat, 0)) * importance[feat] for feat in features if feat in importance}
                sorted_features = sorted(dynamic_importance.items(), key=lambda x: x[1], reverse=False)
                feats, impacts = zip(*sorted_features) if sorted_features else ([], [])
                total_impact = sum(impacts) if sum(impacts) > 0 else 1
                percentages = [(val / total_impact) * 100 for val in impacts]

                fig, ax = plt.subplots(figsize=(7, 3))
                fig.patch.set_facecolor('#111827'); ax.set_facecolor('#111827')
                colors = ['#3B82F6' if p < 30 else '#6366F1' if p < 60 else '#10B981' for p in percentages]
                bars = ax.barh(feats, percentages, color=colors, height=0.4)
                ax.tick_params(colors='#9CA3AF', labelsize=9)
                ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
                st.pyplot(fig)
        else:
            st.info("Awaiting structural parameters execution data matrices command.")

# ==================================================
# MODULE 3: STUDENT-FACING ANONYMOUS CHATBOT (RAG)
# ==================================================
elif st.session_state.view_state == "💬 Student Safe-Space: Anon Chatbot":
    st.subheader("💬 Anonymous Student Well-being Safe-Space")
    st.caption("🔒 Unconditionally confidential session. Connected to institutional resolution guidelines.")

    if "student_chat" not in st.session_state:
        st.session_state.student_chat = [{"role": "assistant", "content": "Hi there. I am an anonymous support space. Whether you are falling behind in classes, feeling overwhelmed by engineering concepts, or stressed about dues, tell me how you are doing."}]

    for msg in st.session_state.student_chat:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    @st.cache_resource
    def init_search():
        if not os.path.exists("counseling_data.csv"): return None, None, None
        df = pd.read_csv("counseling_data.csv")
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        matrix = vectorizer.fit_transform(df['Questions'].astype(str))
        return df, vectorizer, matrix

    df_qa, vectorizer, tfidf_matrix = init_search()

    if prompt := st.chat_input("Explain what's going on..."):
        st.session_state.student_chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)

        with st.chat_message("assistant"):
            if df_qa is not None and vectorizer is not None:
                from sklearn.metrics.pairwise import cosine_similarity
                q_vec = vectorizer.transform([prompt])
                scores = cosine_similarity(q_vec, tfidf_matrix).flatten()
                best = scores.argmax()
                
                if scores[best] > 0.15:
                    res = df_qa['Answers'].iloc[best]
                else:
                    res = "### 🤝 Adaptive Support Space\n\nI hear you, and I understand things feel tough right now. I don't have an exact matching scenario, but you do not have to carry this workload weight alone. Would you like me to securely and safely send a request to schedule a private, non-judgmental talk with an advisor?"
            else:
                res = "⚠️ Counseling data matrix registry uncompiled."
            st.write(res)
        st.session_state.student_chat.append({"role": "assistant", "content": res})
        st.rerun()

# ==================================================
# MODULE 4: COUNSELOR-FACING SMART ASSISTANT
# ==================================================
elif st.session_state.view_state == "🤖 Counselor Smart Assistant: Search":
    st.subheader("🤖 Internal Administrative Information Retrieval Assistant")
    st.caption("🔍 Search institutional dataset trends and extract quick performance metrics summary cards.")

    # Simulated administrative data indexing array records
    mock_students = [
        {"Name": "Student Profile #1042", "Branch": "B.Tech CSE", "Attendance": "62%", "Grade": "08/20", "Status": "🔴 Critical Attrition Risk Signature"},
        {"Name": "Student Profile #2081", "Branch": "B.Tech ECE", "Attendance": "89%", "Grade": "15/20", "Status": "🟢 Stable Performance Profile"},
        {"Name": "Student Profile #1105", "Branch": "B.Tech ME", "Attendance": "55%", "Grade": "07/20", "Status": "🔴 Critical Attrition Risk Signature"}
    ]

    if "counselor_chat" not in st.session_state:
        st.session_state.counselor_chat = [{"role": "assistant", "content": "Welcome, Administrator. Ask me to search performance rosters or extract group trends. E.g., 'Who are the high risk engineering students?'"}]

    for msg in st.session_state.counselor_chat:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if query := st.chat_input("Query institutional database metrics..."):
        st.session_state.counselor_chat.append({"role": "user", "content": query})
        with st.chat_message("user"): st.write(query)

        with st.chat_message("assistant"):
            q_low = query.lower()
            if "risk" in q_low or "engineering" in q_low or "who" in q_low:
                res = "### 📂 Extracted Critical Risk Profiles (Engineering Dev Department):\n\n"
                for student in mock_students:
                    if "Critical" in student["Status"]:
                        res += f"- **{student['Name']}** ({student['Branch']}) | Attendance: {student['Attendance']} | Grade: {student['Grade']} -> **{student['Status']}**\n"
            else:
                res = "### 📑 System Query Parsing Completed\n\nReturned 0 exact index matches. For optimization, please query explicit parameter syntax groupings such as: `risk profiles`, `attendance drop list`, or `term averages`."
            st.write(res)
        st.session_state.counselor_chat.append({"role": "assistant", "content": res})
        st.rerun()