# ================================
# Infrastructure Quality Scoring Dashboard
# ================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px

# Load trained model
model = pickle.load(open("infra_score_model.pkl", "rb"))

# Streamlit page setup
st.set_page_config(page_title="Infrastructure Quality Scoring", layout="wide")

# Sidebar Inputs
st.sidebar.title("🏫 School Infrastructure Inputs")

building_status = st.sidebar.selectbox("Building Status", ["Pucca", "Partly Pucca", "Kuchcha", "Dilapidated"])
boundary_wall = st.sidebar.selectbox("Boundary Wall Available", ["Yes", "No"])
electricity_availability = st.sidebar.selectbox("Electricity Available", ["Yes", "No"])
tap_fun_yn = st.sidebar.selectbox("Functional Tap Water", ["Yes", "No"])
internet = st.sidebar.selectbox("Internet Facility", ["Yes", "No"])
playground_available = st.sidebar.selectbox("Playground Available", ["Yes", "No"])
comp_lab_cond = st.sidebar.selectbox("Computer Lab Condition", ["Good", "Average", "Poor", "Not Available"])
library_availability = st.sidebar.selectbox("Library Available", ["Yes", "No"])
total_boys_func_toilet = st.sidebar.slider("Total Functional  Toilets", 0, 50, 5)
classrooms_in_good_condition = st.sidebar.slider("Classrooms in Good Condition", 0, 100, 20)

# Encode categorical features similar to model
def encode_feature(val, mapping):
    return mapping.get(val, 0)

building_map = {"Pucca": 3, "Partly Pucca": 2, "Kuchcha": 1, "Dilapidated": 0}
yes_no_map = {"Yes": 1, "No": 0}
lab_map = {"Good": 3, "Average": 2, "Poor": 1, "Not Available": 0}

# Prepare input data
input_data = pd.DataFrame({
    'building_status': [encode_feature(building_status, building_map)],
    'boundary_wall': [encode_feature(boundary_wall, yes_no_map)],
    'electricity_availability': [encode_feature(electricity_availability, yes_no_map)],
    'tap_fun_yn': [encode_feature(tap_fun_yn, yes_no_map)],
    'internet': [encode_feature(internet, yes_no_map)],
    'playground_available': [encode_feature(playground_available, yes_no_map)],
    'comp_lab_cond': [encode_feature(comp_lab_cond, lab_map)],
    'library_availability': [encode_feature(library_availability, yes_no_map)],
    'total_boys_func_toilet': [total_boys_func_toilet],
    'classrooms_in_good_condition': [classrooms_in_good_condition]
})

# Main title
st.title("🏫 School Infrastructure Quality Scoring")
st.markdown("Predicts the **Infrastructure Quality Score (0–100)** for a school based on its facilities and resources.")

# Prediction button
if st.button("🔍 Predict Infrastructure Score"):
    prediction = model.predict(input_data)[0]
    score = (round(prediction))*10

    st.subheader(f"🏆 Predicted Infrastructure Score: **{score}**")

    # Display status indicator
    if score >= 80:
        st.success("Excellent Infrastructure Quality 💚")
    elif score >= 60:
        st.info("Good Infrastructure Quality 💙")
    elif score >= 40:
        st.warning("Average Infrastructure Quality 💛")
    else:
        st.error("Poor Infrastructure Quality ❤️")

# Divider
st.markdown("---")
st.subheader("📊 Example Insights (Sample Visualization)")

# Sample district-wise infrastructure performance
sample_data = pd.DataFrame({
    "District": ["A", "B", "C", "D", "E"],
    "Average Infra Score": [85, 74, 60, 45, 30]
})

fig = px.bar(
    sample_data,
    x="District",
    y="Average Infra Score",
    title="Average Infrastructure Quality by District",
    color="Average Infra Score",
    color_continuous_scale="Blues",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
# st.caption("Developed by Neeraj  • Streamlit + XGBoost + Python")
st.markdown("""
<footer>
    <hr>
    <p>Made with ❤️ and purpose by <b>The Role Players</b><br>
    Empowering Education through Data</p>
</footer>
""", unsafe_allow_html=True)