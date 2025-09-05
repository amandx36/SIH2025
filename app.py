import joblib
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Stress Level Detection", layout="centered")

# === load model ===
model = joblib.load("models/best_stress_model__DecisionTree.joblib")

# === features (X) ===
FEATURES = [
    "Age", "Gender", "University", "Department", "Academic Year",
    "Current CGPA", "Anxiety Value", "Stress Value", "Depression Value"
]

# === critical keywords that force Level 3 ===
CRITICAL_WORDS = [
    "suicide", "kill myself", "end my life", "worthless", 
    "hopeless", "die", "cut", "self harm"
]

st.title("🧠 Stress Level Detection")

# --- Inputs ---
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

# === Questionnaire style instead of raw sliders ===
anxiety_map = {"Never": 0, "Sometimes": 1, "Often": 2, "Almost every day": 3}
anxiety = st.radio("How often do you feel anxious in a week?", list(anxiety_map.keys()))
anxiety_val = anxiety_map[anxiety]

stress_map = {"Rarely": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}
stress = st.radio("How often do you feel stressed at work/school?", list(stress_map.keys()))
stress_val = stress_map[stress]

depression_map = {"Never": 0, "Sometimes": 1, "Often": 2, "Every day": 3}
depression = st.radio("How often do you feel sad or hopeless?", list(depression_map.keys()))
depression_val = depression_map[depression]

# === Critical text box ===
user_text = st.text_area("💬 Share your thoughts or feelings (optional)")
critical_flag = any(word in user_text.lower() for word in CRITICAL_WORDS)

# --- Build numeric row ---
input_data = pd.DataFrame([[
    age, gender_val, university_val, department_val, academic_year_val,
    cgpa, anxiety_val, stress_val, depression_val
]], columns=FEATURES)

st.write("### Input Preview (numeric encoding)")
st.dataframe(input_data)

# --- Prediction ---
import streamlit.components.v1 as components

# --- Prediction ---
if st.button("🔍 Predict Stress Level"):
    try:
        if critical_flag:
            decoded_label = "🚨 Critical Condition: High Stress (Level 3)"
            
            # TOP ALERT BANNER
            st.markdown(
                """
                <div style="background-color:#ff4d4d; padding:15px; border-radius:8px; text-align:center; font-size:20px; color:white; font-weight:bold;">
                   "🚨 Critical condition detected! Immediate counselor support required. 🚨 Connecting to the counselor for immediate help."
                </div>
                """,
                unsafe_allow_html=True
            )

            # Play warning sound
            components.html(
                """
                <audio autoplay>
                  <source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg" type="audio/ogg">
                </audio>
                """,
                height=0,
            )

        else:
            pred = model.predict(input_data)[0]
            stress_map = {
                0: "Low Stress (Level 1) 🟢",
                1: "Medium Stress (Level 2) 🟡",
                2: "High Stress (Level 3) 🔴"
            }
            decoded_label = stress_map.get(pred, f"Unknown Level ({pred})")

            if pred == 2:
                # TOP ALERT BANNER
                st.markdown(
                    f"""
                    <div style="background-color:#ff4d4d; padding:15px; border-radius:8px; text-align:center; font-size:20px; color:white; font-weight:bold;">
                        🚨 Predicted Stress Level: {decoded_label} 🚨
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Play warning sound
                components.html(
                    """
                    <audio autoplay>
                      <source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg" type="audio/ogg">
                    </audio>
                    """,
                    height=0,
                )

            elif pred == 1:
                st.warning(f"Predicted Stress Level: **{decoded_label}**")
            else:
                st.success(f"Predicted Stress Level: **{decoded_label}**")

    except Exception as e:
        st.error(f"⚠️ Prediction failed: {e}")
