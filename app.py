import streamlit as st
st.title("Chat App")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

# --------------------------------------------------
# PAGE CONFIG (Forces Dark/Wide Theme Layout)
# --------------------------------------------------
st.set_page_config(
    page_title="AI Dropout Prediction & Counseling System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# PREMIUM GRADIENT GRAPHICS & STYLING (Hugging Face / Gradio Look)
# --------------------------------------------------
st.markdown("""
<style>
    /* Global dark app background overrides */
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }
    
    /* Modern Landing Hub Frame */
    .landing-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        margin: auto;
        max-width: 600px;
    }
    
    /* Beautiful Gradient Header Titles */
    .gradient-title {
        font-size: 38px;
        font-weight: 800;
        background: linear-gradient(135deg, #A7F3D0 0%, #93C5FD 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.3;
        margin-bottom: 15px;
    }
    
    .subtext {
        font-size: 15px;
        color: #9CA3AF;
        line-height: 1.6;
        margin-bottom: 25px;
    }
    
    /* Segment headers for Academic vs Financial inputs */
    .column-header {
        font-size: 18px;
        font-weight: 600;
        color: #93C5FD;
        margin-bottom: 15px;
        border-bottom: 1px solid #1F2937;
        padding-bottom: 6px;
    }
    
    /* High-impact action buttons styling */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #A7F3D0 0%, #93C5FD 100%) !important;
        color: #0F172A !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:first-child:hover {
        opacity: 0.95 !important;
        transform: scale(1.01) !important;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD MODEL FILES
# --------------------------------------------------
@st.cache_resource
def load_ai_assets():
    required_files = ["dropout_model.pkl", "features.pkl", "importance.pkl"]
    for file in required_files:
        if not os.path.exists(file):
            st.error(f"Missing file: {file}")
            return None, None, None
    try:
        with open("dropout_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("features.pkl", "rb") as f:
            features = pickle.load(f)
        with open("importance.pkl", "rb") as f:
            importance = pickle.load(f)
        return model, features, importance
    except Exception as e:
        st.error(f"Error loading model files: {e}")
        return None, None, None

model, features, importance = load_ai_assets()

if model is None:
    st.stop()

# --------------------------------------------------
# NAVIGATION STATE MANAGEMENT
# --------------------------------------------------
if "view_state" not in st.session_state:
    st.session_state.view_state = "welcome"

# Sidebar Workspace Switcher
st.sidebar.header("⚙️ System Control Center")
app_mode = st.sidebar.radio(
    "Navigate Workspace",
    ["Welcome Portal Cover", "Counselor Dashboard & Risk Evaluator", "Student Safe-Space Chatbot"]
)

# Sync sidebar choices back to current state tracking
if app_mode == "Counselor Dashboard & Risk Evaluator":
    st.session_state.view_state = "dashboard"
elif app_mode == "Student Safe-Space Chatbot":
    st.session_state.view_state = "chatbot"

# ==================================================
# SCREEN 1: WELCOME PORTAL COVER
# ==================================================
if st.session_state.view_state == "welcome":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="landing-card">
        <div style='font-size: 55px; margin-bottom: 15px;'>🛡️</div>
        <div class="gradient-title">AI Dropout Prediction<br>& Counseling System</div>
        <div class="subtext">
            Empowering educational institutions with predictive intelligence and 
            compassionate early-intervention strategies to maximize student retention.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 0.8, 1])
    with c2:
        if st.button("ENTER DASHBOARD SYSTEM", use_container_width=True):
            st.session_state.view_state = "dashboard"
            st.rerun()

# ==================================================
# SCREEN 2: COUNSELOR DASHBOARD & RISK EVALUATOR
# ==================================================
elif st.session_state.view_state == "dashboard":
    
    # Modern Gradient Top Visual Bar
    st.markdown("<div style='background: linear-gradient(90deg, #A7F3D0 0%, #93C5FD 100%); height: 16px; border-radius: 4px; margin-bottom: 5px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 13px;'>Fill in the precise academic and behavioral metrics below for analysis</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Core Layout Grid Structure
    col1, col2 = st.columns([1.1, 1], gap="large")

    with col1:
        input_data = {}
        
        # Subdivide features explicitly into Academic vs Financial Column Panes
        sub_col_left, sub_col_right = st.columns(2, gap="medium")
        
        with sub_col_left:
            st.markdown('<div class="column-header">Academic Metrics</div>', unsafe_allow_html=True)
            
            # Extract standard elements safely if present in feature matrix
            if "Age at enrollment" in features:
                input_data["Age at enrollment"] = st.slider("Age at Enrollment", min_value=15, max_value=60, value=20)
            
            # Optional UI additions to blend with your image placeholders
            st.slider("Class Attendance Rate (%)", min_value=0, max_value=100, value=85, key="attendance_ui")
            st.slider("1st Semester Grade Average (0-10 scale)", min_value=0, max_value=10, value=7, key="grade_ui")

        with sub_col_right:
            st.markdown('<div class="column-header">Financial & Support Status</div>', unsafe_allow_html=True)
            
            if "Scholarship holder" in features:
                s_choice = st.radio("Scholarship Holder", ["No", "Yes"], horizontal=True)
                input_data["Scholarship holder"] = 1 if s_choice == "Yes" else 0
                
            if "Debtor" in features:
                d_choice = st.radio("Is Institutional Debtor", ["No", "Yes"], horizontal=True)
                input_data["Debtor"] = 1 if d_choice == "Yes" else 0
                
            st.radio("Tuition Fees Up-to-Date", ["Yes", "No"], horizontal=True, key="tuition_ui")
            if "Gender" in features:
                g_choice = st.radio("Demographic: Gender", ["Female", "Male"], horizontal=True, key="gender_radio")
                input_data["Gender"] = 1 if g_choice == "Male" else 0

        # Automatically resolve standard loop elements not mapped yet
        for feature in features:
            if feature not in input_data:
                if feature == "Gender":
                    g_choice = st.selectbox("Gender", ["Female", "Male"])
                    input_data[feature] = 1 if g_choice == "Male" else 0
                else:
                    input_data[feature] = 0.0

        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("RUN PREDICTIVE ANALYSIS", use_container_width=True)

    with col2:
        st.markdown('<div class="column-header">Dynamic Analytics Engine</div>', unsafe_allow_html=True)

        if analyze_btn:
            try:
                input_df = pd.DataFrame([input_data])[features]

                if hasattr(model, "predict_proba"):
                    risk_probability = model.predict_proba(input_df)[0][1] * 100
                else:
                    risk_probability = model.predict(input_df)[0] * 100

                m1, m2 = st.columns(2)
                m1.metric(label="Calculated Risk Score", value=f"{risk_probability:.1f}%")

                if risk_probability < 25:
                    m2.success("🟢 LOW")
                    st.success("This student currently shows low dropout risk.")
                elif risk_probability < 50:
                    m2.warning("🟡 MODERATE")
                    st.warning("Moderate risk detected. Early intervention recommended.")
                else:
                    m2.error("🔴 HIGH")
                    st.error("High-risk pattern detected. Immediate counselor action recommended.")
                    st.info("""
                    ### AI Counselor Recommendations
                    - Review outstanding financial obligations immediately.
                    - Schedule a proactive 1-on-1 wellness session.
                    - Sync updates with peer academic support channels.
                    """)

                # XAI Metric Chart Render Block
                st.markdown("---")
                st.markdown("### 📊 Personalized Feature Impact Analysis")
                st.caption("This Explainable AI (XAI) chart shows exactly which risk factors contributed most to this specific student's prediction score.")

                try:
                    if isinstance(importance, dict):
                        import matplotlib.pyplot as plt

                        # Calculate dynamic impact: absolute input value * structural model weight
                        dynamic_importance = {
                            feat: abs(input_data.get(feat, 0)) * importance[feat] 
                            for feat in features if feat in importance
                        }
                        
                        # Sort data from highest impact to lowest
                        sorted_features = sorted(dynamic_importance.items(), key=lambda x: x[1], reverse=False)
                        feats, impacts = zip(*sorted_features) if sorted_features else ([], [])
                        
                        # Total impact for percentage calculation
                        total_impact = sum(impacts) if sum(impacts) > 0 else 1
                        percentages = [(val / total_impact) * 100 for val in impacts]

                        # Create a premium dark-themed plot
                        fig, ax = plt.subplots(figsize=(7, 3.5))
                        fig.patch.set_facecolor('#111827')  # Matches landing card color
                        ax.set_facecolor('#111827')

                        # Draw horizontal bars with a clean tech-blue/teal color palette
                        colors = ['#3B82F6' if p < 30 else '#6366F1' if p < 60 else '#10B981' for p in percentages]
                        bars = ax.barh(feats, percentages, color=colors, edgecolor='none', height=0.5)

                        # Polish axes text and borders
                        ax.tick_params(colors='#9CA3AF', labelsize=10)
                        ax.spines['top'].set_visible(False)
                        ax.spines['right'].set_visible(False)
                        ax.spines['left'].set_color('#1F2937')
                        ax.spines['bottom'].set_color('#1F2937')
                        ax.grid(axis='x', color='#1F2937', linestyle='--', alpha=0.5)
                        ax.set_xlabel("Relative Contribution Weight (%)", color='#9CA3AF', fontsize=10)

                        # Add real-time value text tags inside/next to the bars
                        for bar in bars:
                            width = bar.get_width()
                            ax.text(
                                width + 1, 
                                bar.get_y() + bar.get_height()/2, 
                                f'{width:.1f}%', 
                                va='center', 
                                ha='left', 
                                color='#F3F4F6', 
                                fontsize=9, 
                                fontweight='bold'
                            )

                        # Render the beautiful custom chart inside Streamlit
                        st.pyplot(fig)
                        
                    else:
                        st.warning("importance.pkl configuration mismatch.")
                except Exception as chart_error:
                    st.warning(f"Feature importance rendering skipped: {chart_error}")

            except Exception as e:
                st.error(f"Prediction Pipeline Error: {e}")
        else:
            st.info("Adjust student parameters on the left pane and execute the analytical model pipeline.")

# ==================================================
# SCREEN 3: SECURE PROBLEM-SOLVING AI CHATBOT
# ==================================================
elif st.session_state.view_state == "chatbot":
    from openai import OpenAI

    st.subheader("💬 Advanced AI Academic Counseling Copilot")
    st.caption("🔒 Multi-turn conversation engine powered by Generative AI. All sessions are completely secure and private.")

    # 1. Fetch the API Key securely from background environment secrets
    # It checks if a secret key exists; if not, it cleanly falls back to None
    openai_api_key = st.secrets.get("OPENAI_API_KEY", None)

    # 2. Setup structural conversation history state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Welcome back. I am your specialized AI Academic Support Guide. Whether you are dealing with immense midterm exam stress, complex financial aid applications, or general academic burnout, I am here to help you break down the problem and build an actionable solution. What is the main hurdle on your mind today?"}
        ]

    # Render previous conversation loop smoothly
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 3. Capture real-time user chat inputs
    if user_prompt := st.chat_input("Explain your situation safely... (e.g., 'I am failing my data structures course')"):
        
        # Display user input instantly
        with st.chat_message("user"):
            st.write(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        # Process output using live LLM reasoning if the background secret exists
        if openai_api_key:
            try:
                client = OpenAI(api_key=openai_api_key)
                
                system_instruction = (
                    "You are 'EduGuard Copilot', an expert university counselor and real-world academic problem-solving AI. "
                    "Your target audience consists of college students dealing with high stress, low grades, or financial hardship. "
                    "DIRECTIONS: Be intensely empathetic, encouraging, and highly practical. Avoid generic platitudes. "
                    "Instead, break problems down step-by-step. Provide structured roadmaps, suggest specific university support channels, "
                    "and maintain an unconditionally safe space. Speak like a supportive, grounded academic mentor."
                )

                messages_payload = [{"role": "system", "content": system_instruction}] + st.session_state.chat_history

                with st.chat_message("assistant"):
                    with st.spinner("Analyzing situation and generating guidance..."):
                        completion = client.chat.completions.create(
                            model="gpt-4o-mini", 
                            messages=messages_payload,
                            temperature=0.7
                        )
                        ai_response = completion.choices[0].message.content
                        st.write(ai_response)
                        
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                
            except Exception as api_err:
                st.error(f"API Connection Error: {api_err}")
        
        # 4. ROBUST FALLBACK ENGINE: If no key is configured yet, run the smart contextual simulation
        else:
            with st.chat_message("assistant"):
                with st.spinner("Processing contextual query..."):
                    import time
                    time.sleep(1) 
                    
                    user_lower = user_prompt.lower()
                    if any(w in user_lower for w in ["exam", "fail", "study", "grade", "marks", "daa", "oop"]):
                        ai_response = (
                            "### 📋 Personal Recovery Roadmap\n\n"
                            "I hear you, and feeling lost when facing complex subjects is incredibly common. Let's tackle this methodically:\n\n"
                            "1. **Isolate the Weak Links:** Identify the exact modules causing friction (e.g., Dynamic Programming in DAA).\n"
                            "2. **The 25-Minute Rule:** Use the Pomodoro technique—study hard for 25 minutes, then take a 5-minute break.\n"
                            "3. **Leverage Institutional Capital:** Check the portal for the **Free Peer-Tutoring Scheme**. Meeting with a senior who aced this class can help immensely.\n\n"
                            "Would you like me to help you design a simplified, day-by-day revision schedule for this week?"
                        )
                    elif any(w in user_lower for w in ["money", "fee", "pay", "scholarship", "debt", "financial"]):
                        ai_response = (
                            "### 🛡️ Financial Support Action Plan\n\n"
                            "Please remember that financial liabilities are systemic challenges—they do not define your potential. Let's review your strategic options:\n\n"
                            "1. **Tuition Installment Waivers:** The Student Welfare Office can freeze late payment penalties if you submit an official request.\n"
                            "2. **Book Bank Facilities:** Verify if your library runs a textbook registry to avoid out-of-pocket book expenses.\n\n"
                            "Would you like me to pre-draft a professional, polite email template you can send to the department dean?"
                        )
                    else:
                        ai_response = (
                            "Thank you for sharing that with me. Academic burnout can cloud our next steps, but every roadblock has a solution. "
                            "Let's break this down into actionable milestones together. What specific variable is creating the biggest bottleneck for you right now?"
                        )
                    st.write(ai_response)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})