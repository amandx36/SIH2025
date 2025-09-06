import joblib
import streamlit as st
import numpy as np
import pandas as pd
import requests
import streamlit.components.v1 as components

# ================== PAGE CONFIG ==================
st.set_page_config(page_title="Stress Level Detection", layout="centered")

# ================== LOAD MODEL ==================
model = joblib.load("models/best_stress_model__DecisionTree.joblib")

# ================== FEATURES ==================
FEATURES = [
    "Age", "Gender", "University", "Department", "Academic Year",
    "Current CGPA", "Anxiety Value", "Stress Value", "Depression Value"
]

# ================== CRITICAL KEYWORDS ==================
CRITICAL_WORDS = [
    "suicide", "kill myself", "end my life", "worthless",
    "hopeless", "die", "cut", "self harm"
]

# ================== TELEGRAM HELPER ==================
def send_telegram_message(text: str):
    try:
        token = st.secrets["TELEGRAM_BOT_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]
    except KeyError:
        st.warning("⚠️ Telegram secrets missing. Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .streamlit/secrets.toml")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload, timeout=10)
        r.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Telegram send failed: {e}")
        return False

# ================== APP TITLE ==================
st.title("🧠 Stress Level Detection")

# ================== INPUTS ==================
age = st.slider("Age", 15, 60, 20)

gender = st.selectbox("Gender", ["Male", "Female"])
gender_val = 1 if gender == "Male" else 0   # encode

university = st.selectbox("University", ["University A", "University B", "University C", "Other"])
university_map = {"University A": 0, "University B": 1, "University C": 2, "Other": 3}
university_val = university_map[university]

department = st.selectbox("Department", ["Computer Science", "Electrical", "Mechanical", "Civil", "Other"])
dept_map = {"Computer Science": 0, "Electrical": 1, "Mechanical": 2, "Civil": 3, "Other": 4}
department_val = dept_map[department]

academic_year = st.selectbox("Academic Year", [
    "First Year or Equivalent", "Second Year or Equivalent",
    "Third Year or Equivalent", "Fourth Year or Equivalent", "Other"
])
year_map = {
    "First Year or Equivalent": 1,
    "Second Year or Equivalent": 2,
    "Third Year or Equivalent": 3,
    "Fourth Year or Equivalent": 4,
    "Other": 0
}
academic_year_val = year_map[academic_year]

cgpa = st.slider("Current CGPA", 0.0, 10.0, 7.5, step=0.1)

# Questionnaire
anxiety_map = {"Never": 0, "Sometimes": 1, "Often": 2, "Almost every day": 3}
anxiety = st.radio("How often do you feel anxious in a week?", list(anxiety_map.keys()))
anxiety_val = anxiety_map[anxiety]

stress_map = {"Rarely": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}
stress = st.radio("How often do you feel stressed at work/school?", list(stress_map.keys()))
stress_val = stress_map[stress]

depression_map = {"Never": 0, "Sometimes": 1, "Often": 2, "Every day": 3}
depression = st.radio("How often do you feel sad or hopeless?", list(depression_map.keys()))
depression_val = depression_map[depression]

# Free text
user_text = st.text_area("💬 Share your thoughts or feelings (optional)")
critical_flag = any(word in user_text.lower() for word in CRITICAL_WORDS)

# Build numeric row
input_data = pd.DataFrame([[
    age, gender_val, university_val, department_val, academic_year_val,
    cgpa, anxiety_val, stress_val, depression_val
]], columns=FEATURES)

st.write("### Input Preview (numeric encoding)")
st.dataframe(input_data)

# ================== PREDICTION ==================
if st.button("🔍 Predict Stress Level"):
    try:
        if critical_flag:
            decoded_label = "🚨 Critical Condition: High Stress (Level 3)"
            
            # Banner
            st.markdown(
                """
                <div style="background-color:#ff4d4d; padding:15px; border-radius:8px; text-align:center; font-size:20px; color:white; font-weight:bold;">
                   🚨 Critical condition detected! Immediate counselor support required. 🚨
                </div>
                """,
                unsafe_allow_html=True
            )
            # Sound
            components.html(
                """
                <audio autoplay>
                  <source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg" type="audio/ogg">
                </audio>
                """,
                height=0,
            )
            # Telegram Alert
            alert_text = (
                "🚨 <b>CRITICAL ALERT</b>\n"
                f"Age: {age}, Gender: {gender}\n"
                f"University: {university}, Dept: {department}, Year: {academic_year}\n"
                f"CGPA: {cgpa}\n"
                f"Anxiety:{anxiety} | Stress:{stress} | Depression:{depression}\n"
                f"User: {user_text[:300]}{'...' if len(user_text)>300 else ''}"
            )
            sent = send_telegram_message(alert_text)
            if sent:
                st.info("📩 Counselor alert sent on Telegram.")

        else:
            pred = model.predict(input_data)[0]
            stress_map = {
                0: "Low Stress (Level 1) 🟢",
                1: "Medium Stress (Level 2) 🟡",
                2: "High Stress (Level 3) 🔴"
            }
            decoded_label = stress_map.get(pred, f"Unknown Level ({pred})")

            if pred == 2:
                st.markdown(
                    f"""
                    <div style="background-color:#ff4d4d; padding:15px; border-radius:8px; text-align:center; font-size:20px; color:white; font-weight:bold;">
                        🚨 Predicted Stress Level: {decoded_label} 🚨
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                components.html(
                    """
                    <audio autoplay>
                      <source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg" type="audio/ogg">
                    </audio>
                    """,
                    height=0,
                )
                # Telegram Alert
                alert_text = (
                    "🚨 <b>ALERT</b>\n"
                    f"Predicted Stress Level: {decoded_label}\n"
                    f"Age: {age}, Gender: {gender}\n"
                    f"University: {university}, Dept: {department}, Year: {academic_year}\n"
                    f"CGPA: {cgpa}\n"
                    f"Anxiety:{anxiety} | Stress:{stress} | Depression:{depression}\n"
                    f"User: {user_text[:300]}{'...' if len(user_text)>300 else ''}"
                )
                sent = send_telegram_message(alert_text)
                if sent:
                    st.info("📩 Counselor alert sent on Telegram.")

            elif pred == 1:
                st.warning(f"Predicted Stress Level: **{decoded_label}**")
            else:
                st.success(f"Predicted Stress Level: **{decoded_label}**")

    except Exception as e:
        st.error(f"⚠️ Prediction failed: {e}")
