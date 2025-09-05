import joblib
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Stress Level Detection", layout="centered")

# === Load model ===
model = joblib.load("models/best_stress_model__DecisionTree.joblib")

# Classes mapping directly from model
label_map = {i: cls for i, cls in enumerate(model.classes_)}

# === Features (X) ===
FEATURES = [
    "Age", "Gender", "University", "Department", "Academic Year",
    "Current CGPA", "Anxiety Value", "Stress Value", "Depression Value"
]

st.title("🧠 Stress Level Detection")
st.write("Prototype demo for Hackathon 🚀")

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
anxiety = st.slider("Anxiety Value", 0, 30, 10)
stress = st.slider("Stress Value", 0, 40, 15)
depression = st.slider("Depression Value", 0, 30, 12)

# --- Build numeric row ---
input_data = pd.DataFrame([[
    age, gender_val, university_val, department_val, academic_year_val,
    cgpa, anxiety, stress, depression
]], columns=FEATURES)

st.write("### Input Preview (numeric encoding)")
st.dataframe(input_data)

# --- Prediction ---
# --- Prediction ---
if st.button("🔍 Predict Stress Level"):
    try:
        pred = model.predict(input_data)[0]

        # Manually map numeric output to human-readable labels
        stress_map = {
            0: "Low Stress (Level 1)",
            1: "Medium Stress (Level 2)",
            2: "High Stress (Level 3)"
        }

        decoded_label = stress_map.get(pred, f"Unknown Level ({pred})")

        st.success(f"Predicted Stress Level: **{decoded_label}**")
    except Exception as e:
        st.error(f"⚠️ Prediction failed: {e}")
