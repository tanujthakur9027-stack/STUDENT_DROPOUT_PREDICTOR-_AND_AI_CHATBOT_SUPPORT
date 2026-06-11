import streamlit as st
import pandas as pd
import pickle
import os

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="AI Dropout Prediction & Counseling System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 2. CUSTOM THEME GRAPHICS & INTERFACE DESIGN (CSS)
# --------------------------------------------------
st.markdown("""
<style>
    /* Global dark app background canvas style matching Hugging Face Spaces */
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }
    
    /* Elegant Landing Portal Card Frame */
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
    
    /* Shimmering Gradient Header Typography */
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
    
    /* Categorized Metrics Input Section Dividers */
    .column-header {
        font-size: 18px;
        font-weight: 600;
        color: #93C5FD;
        margin-bottom: 15px;
        border-bottom: 1px solid #1F2937;
        padding-bottom: 6px;
    }
    
    /* Core Call-to-Action Theme Accent Buttons */
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
# 3. SECURE ASSET LOADING SUBROUTINES
# --------------------------------------------------
@st.cache_resource
def load_ai_assets():
    required_files = ["dropout_model.pkl", "features.pkl", "importance.pkl"]
    for file in required_files:
        if not os.path.exists(file):
            st.error(f"⚠️ Critical Background Asset Missing: {file}")
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
        st.error(f"❌ Structural Failure Loading Model Assets: {e}")
        return None, None, None

model, features, importance = load_ai_assets()

if model is None:
    st.stop()

# --------------------------------------------------
# 4. PERSISTENT SYSTEM NAVIGATION BLOCK (Fixed)
# --------------------------------------------------
# Explicitly list your workflow views to map indexes
modes = ["Welcome Portal Cover", "Counselor Dashboard & Risk Evaluator", "Student Safe-Space Chatbot"]

if "view_state" not in st.session_state:
    st.session_state.view_state = "Welcome Portal Cover"

# Define a clean callback utility for the entry button
def enter_dashboard_callback():
    st.session_state.view_state = "Counselor Dashboard & Risk Evaluator"

# Determine the dynamic index of the sidebar based on session state
try:
    default_sidebar_index = modes.index(st.session_state.view_state)
except ValueError:
    default_sidebar_index = 0

st.sidebar.header("⚙️ System Control Center")

# Force the radio menu to reflect state updates dynamically using the index parameter
app_mode = st.sidebar.radio(
    "Navigate Workspace",
    modes,
    index=default_sidebar_index
)

# Update session state if the user manually clicks the sidebar menu options
if app_mode != st.session_state.view_state:
    st.session_state.view_state = app_mode

# ==================================================
# SCREEN 1: WELCOME PORTAL COVER (Fixed)
# ==================================================
if st.session_state.view_state == "Welcome Portal Cover":
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
        # Using the on_click callback guarantees the state locks before the page updates
        if st.button("ENTER DASHBOARD SYSTEM", use_container_width=True, on_click=enter_dashboard_callback):
            st.rerun()

# ==================================================
# SCREEN 2: COUNSELOR DASHBOARD & RISK EVALUATOR
# ==================================================
elif st.session_state.view_state == "Counselor Dashboard & Risk Evaluator":
    st.markdown("<div style='background: linear-gradient(90deg, #A7F3D0 0%, #93C5FD 100%); height: 16px; border-radius: 4px; margin-bottom: 5px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 13px;'>Fill in the precise academic and behavioral metrics below for analysis</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1], gap="large")
    st.markdown("<div style='background: linear-gradient(90deg, #A7F3D0 0%, #93C5FD 100%); height: 16px; border-radius: 4px; margin-bottom: 5px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 13px;'>Fill in the precise academic and behavioral metrics below for analysis</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1], gap="large")

    with col1:
        input_data = {}
        sub_col_left, sub_col_right = st.columns(2, gap="medium")
        
        with sub_col_left:
            st.markdown('<div class="column-header">Academic Metrics</div>', unsafe_allow_html=True)
            if "Age at enrollment" in features:
                input_data["Age at enrollment"] = st.slider("Age at Enrollment", min_value=15, max_value=60, value=20)
            if "Attendance_Rate" in features:
                input_data["Attendance_Rate"] = st.slider("Class Attendance Rate (%)", min_value=0, max_value=100, value=85)
            if "Curricular_units_1st_sem_grade" in features:
                input_data["Curricular_units_1st_sem_grade"] = st.slider("1st Semester Grade Average (0-20 scale)", min_value=0, max_value=20, value=14)

        with sub_col_right:
            st.markdown('<div class="column-header">Financial & Support Status</div>', unsafe_allow_html=True)
            if "Scholarship holder" in features:
                s_choice = st.radio("Scholarship Holder", ["No", "Yes"], horizontal=True, key="scholarship_radio")
                input_data["Scholarship holder"] = 1 if s_choice == "Yes" else 0
            if "Debtor" in features:
                d_choice = st.radio("Is Institutional Debtor", ["No", "Yes"], horizontal=True, key="debtor_radio")
                input_data["Debtor"] = 1 if d_choice == "Yes" else 0
            if "Gender" in features:
                g_choice = st.radio("Demographic: Gender", ["Female", "Male"], horizontal=True, key="gender_radio")
                input_data["Gender"] = 1 if g_choice == "Male" else 0

        # Fill potential training parameter array gaps automatically
        for feat in features:
            if feat not in input_data:
                input_data[feat] = 0.0

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

                if risk_probability < 35:
                    m2.success("🟢 STABLE")
                    st.success("Evaluation Signature: Low attrition risk markers. Maintain baseline institutional visibility.")
                elif risk_probability < 70:
                    m2.warning("🟡 MONITOR")
                    st.warning("Evaluation Signature: Early warning telemetry active. Flag for soft checkpoint outreach.")
                else:
                    m2.error("🔴 CRITICAL")
                    st.error("Evaluation Signature: Multi-vector threat signature match. Initiate prioritized emergency intervention.")
                    st.info("### 🤖 AI Counselor Recommendations\n- Review financial obligations.\n- Coordinate urgent advisor-led 1-on-1 counseling window.")

                # Custom XAI Matplotlib Dark Bar Chart Rendering
                st.markdown("---")
                st.markdown("### 📊 Personalized Feature Impact Analysis")
                try:
                    if isinstance(importance, dict):
                        import matplotlib.pyplot as plt
                        dynamic_importance = {feat: abs(input_data.get(feat, 0)) * importance[feat] for feat in features if feat in importance}
                        sorted_features = sorted(dynamic_importance.items(), key=lambda x: x[1], reverse=False)
                        feats, impacts = zip(*sorted_features) if sorted_features else ([], [])
                        total_impact = sum(impacts) if sum(impacts) > 0 else 1
                        percentages = [(val / total_impact) * 100 for val in impacts]

                        fig, ax = plt.subplots(figsize=(7, 3.5))
                        fig.patch.set_facecolor('#111827')
                        ax.set_facecolor('#111827')
                        colors = ['#3B82F6' if p < 30 else '#6366F1' if p < 60 else '#10B981' for p in percentages]
                        bars = ax.barh(feats, percentages, color=colors, edgecolor='none', height=0.5)

                        ax.tick_params(colors='#9CA3AF', labelsize=10)
                        ax.spines['top'].set_visible(False)
                        ax.spines['right'].set_visible(False)
                        ax.spines['left'].set_color('#1F2937')
                        ax.spines['bottom'].set_color('#1F2937')
                        ax.set_xlabel("Relative Contribution Weight (%)", color='#9CA3AF', fontsize=10)

                        for bar in bars:
                            width = bar.get_width()
                            ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', va='center', ha='left', color='#F3F4F6', fontsize=9, fontweight='bold')
                        st.pyplot(fig)
                except Exception as chart_error:
                    st.warning(f"Feature importance rendering skipped: {chart_error}")

            except Exception as e:
                st.error(f"Prediction Pipeline Error: {e}")
        else:
            st.info("Adjust student parameters on the left pane and execute the analytical model pipeline.")

# ==================================================
# SCREEN 3: STABILIZED DATASET-DRIVEN CHATBOT (RAG)
# ==================================================
elif st.session_state.view_state == "Student Safe-Space Chatbot":
    st.subheader("💬 Advanced Dataset-Driven Counseling Copilot")
    st.caption("🔒 Armed with a real-world institutional QA knowledge base to answer any student query dynamically.")

    # 1. Initialize structural session conversation arrays if missing
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Welcome back. I am your specialized AI Academic Support Guide. Tell me about any administrative hurdles, financial strain, or exam anxiety you are experiencing."}
        ]

    # 2. Safely render the message vault on screen
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # 3. Load and cache the TF-IDF search engine subroutines
    @st.cache_resource
    def initialize_semantic_search():
        if not os.path.exists("counseling_data.csv"):
            return None, None, None
        
        df_qa = pd.read_csv("counseling_data.csv")
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(df_qa['Questions'].astype(str))
        return df_qa, vectorizer, tfidf_matrix

    df_qa, vectorizer, tfidf_matrix = initialize_semantic_search()

    # 4. Handle live conversational user input captures cleanly
    if user_prompt := st.chat_input("Ask anything safely..."):
        # Append user text to persistent state arrays instantly
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        
        # Display the user's text on screen immediately
        with st.chat_message("user"):
            st.write(user_prompt)

        # Generate the predictive data frame response block
        with st.chat_message("assistant"):
            with st.spinner("Searching counseling database..."):
                if df_qa is not None and vectorizer is not None:
                    from sklearn.metrics.pairwise import cosine_similarity
                    
                    # Mathematical Vectorization matching pipeline
                    query_vector = vectorizer.transform([user_prompt])
                    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
                    best_match_idx = similarity_scores.argmax()
                    highest_score = similarity_scores[best_match_idx]
                    
                    # Threshold verification matching logic
                    if highest_score > 0.15:
                        ai_response = f"### 🛡️ Verified Counseling Framework\n\n{df_qa['Answers'].iloc[best_match_idx]}"
                    else:
                        ai_response = "### 🤝 Adaptive System Guidance\n\nI couldn't find an exact matching scenario within our knowledge metrics, but you don't have to navigate this pressure alone. Would you like me to flag this secure session to request a priority, confidential meeting with campus student services?"
                else:
                    ai_response = "⚠️ **Database Notice:** Local file asset `counseling_data.csv` was not detected. Please execute `python fetch_chatbot_data.py` in your terminal first."
                
                st.write(ai_response)
        
        # Store response and refresh the page smoothly to preserve conversation tracking
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        st.rerun()