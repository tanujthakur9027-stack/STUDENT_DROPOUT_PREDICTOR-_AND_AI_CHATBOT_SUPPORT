# 🎓 EduGuard AI: Drop-out Prediction & Proactive Counseling System

An AI-driven institutional dashboard designed to detect early warning signs of student attrition using Machine Learning, coupled with an advanced Generative AI Counseling Copilot to provide immediate, empathetic problem-solving support.

---

## 👥 The Team
Developed with dedication by:
* **Tanuj Kumar Singh** (B.Tech CSE, Mangalayatan University)
* **Bhavna Agrawal**

---

## 📌 Problem Statement (PS)
Educational institutions frequently fail to identify early indicators of student dropouts because critical telemetry—such as financial status, demographic metrics, and academic performance drops—sits passively in fragmented databases. Furthermore, students experiencing academic burnout or financial distress often avoid seeking human counseling due to anxiety, stigma, or institutional friction. 

**EduGuard AI** solves this by creating a predictive early warning framework for administrators alongside an anonymous, conversational safe space for students.

---

## 🚀 Key Features

### 1. Multi-Factor Predictive ML Engine
* Powered by an optimized **Random Forest Classifier** trained on verified real-world institutional data.
* Analyzes a holistic matrix of features: Outstanding tuition balance (`Debtor`), Scholarship status, Enrollment age, Gender, and 1st-semester grades.
* Implements a balanced class-weight distribution to flag high-risk students accurately without bias.

### 2. Explainable AI (XAI) Analytics
* Transcends "black-box" models by rendering a dynamic, customized **Feature Impact Analysis** chart using Matplotlib.
* Pinpoints the precise variables causing a specific student's risk profile to spike, giving counselors immediate context.

### 3. Advanced GenAI Problem-Solving Copilot
* A sympathetic, context-aware chatbot workspace leveraging specialized system prompt guidelines.
* Integrates a robust hybrid architecture: pairs live Large Language Model orchestration with deterministic contextual simulation fallbacks to guarantee uninterrupted live hackathon demonstrations.

---

## 🛠️ Tech Stack & Architecture

* **Frontend UI:** Streamlit (Custom Styled Dark Gradient Persona)
* **Core Language:** Python 
* **Data & Machine Learning:** Pandas, NumPy, Scikit-Learn
* **Data Visualization:** Matplotlib (Customized Dark Theme Plotting)
* **Generative AI:** OpenAI API (`gpt-4o-mini`)

---

## 📂 Project Structure

```text
├── app.py              # Main multi-page Streamlit application & chatbot UI
├── train_model.py      # ML data pipeline, model training, and asset generation
├── requirements.txt    # Cloud environment installation dependencies
├── dropout_model.pkl   # Serialized trained Random Forest model asset
├── features.pkl        # Serialized feature sequence array
└── importance.pkl      # Serialized feature weight coefficients dictionary
## Link of deployed project - https://studentdropoutpredictor-andaichatbotsupport-s7jc58wm4kff5jcijz.streamlit.app/
