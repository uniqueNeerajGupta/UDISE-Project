import streamlit as st
import numpy as np
import pickle

# ===============================
# 🎯 Load Models
# ===============================
with open('xgb_dropout_model.pkl', 'rb') as f:
    xgb_reg = pickle.load(f)

with open('xgb_retention_model.pkl', 'rb') as f:
    xgb_cls = pickle.load(f)

# ===============================
# ⚙️ Streamlit Page Config
# ===============================
st.set_page_config(
    page_title="🎓 EduPredict Dashboard",
    page_icon="📊",
    layout="wide",
)

# ===============================
# 🎓 Header
# ===============================
st.markdown("""
<h1 style='text-align:center; color:#2E86C1;'>🎓 EduPredict Dashboard</h1>
<p style='text-align:center; font-size:18px;'>
Smart predictions on school <b>Dropout Rates</b> and <b>Retention Levels</b> based on infrastructure and demographics.
</p>
""", unsafe_allow_html=True)

st.divider()

# ===============================
# 🏫 Section 1: Infrastructure Inputs
# ===============================
st.subheader("🏫 School Infrastructure Details")

col1, col2, col3 = st.columns(3)

with col1:
    electricity = st.selectbox("⚡ Electricity Availability", ["Yes", "No"])
    total_class_rooms = st.number_input("🏫 Total Classrooms", 1, 50, 10)
    total_tch = st.number_input("👨‍🏫 Total Teachers", 1, 100, 20)
    trained_comp = st.number_input("💻 Computer-Trained Teachers", 0, 100, 5)

with col2:
    furniture = st.selectbox("🪑 Furniture Availability", ["Yes", "No"])
    total_girls_func_toilet = st.number_input("🚺 Functional Girls Toilets", 0, 50, 2)
    library = st.selectbox("📚 Library Availability", ["Yes", "No"])
    internet = st.selectbox("🌐 Internet Availability", ["Yes", "No"])

with col3:
    building_status = st.selectbox("🏗️ Building Type", ["Pucca", "Semi Pucca", "Kuchcha"])
    playground = st.selectbox("⚽ Playground Available", ["Yes", "No"])

st.divider()

# ===============================
# 👩‍🏫 Section 2: Demographic Inputs
# ===============================
st.subheader("👩‍🏫 Demographic & School Information")

col4, col5, col6 = st.columns(3)

with col4:
    rural_urban = st.selectbox("🏙️ Area Type", ["Rural", "Urban"])
    school_category = st.selectbox("🏫 School Category", ["Primary", "Upper Primary", "Secondary", "Higher Secondary"])

with col5:
    management = st.selectbox("🏢 Management Type", ["Govt", "Private", "Aided"])
    female_teachers = st.number_input("👩 Total Female Teachers", 0, 100, 10)

with col6:
    availability_ramps = st.selectbox("♿ Ramps Available", ["Yes", "No"])
    medical_checkups = st.selectbox("🩺 Medical Checkups", ["Yes", "No"])

# ===============================
# 🔢 Data Preprocessing
# ===============================
def encode_binary(x):
    return 1 if x.lower() in ["yes", "pucca"] else 0

# Dropout model features
X_reg_input = np.array([[
    encode_binary(electricity),
    total_class_rooms,
    total_tch,
    trained_comp,
    encode_binary(furniture),
    total_girls_func_toilet,
    encode_binary(library),
    encode_binary(internet),
    encode_binary(building_status),
    encode_binary(playground)
]])

# Retention model features
X_cls_input = np.array([[
    1 if rural_urban.lower() == "urban" else 0,
    ["Primary", "Upper Primary", "Secondary", "Higher Secondary"].index(school_category),
    ["Govt", "Private", "Aided"].index(management),
    female_teachers,
    total_tch,
    trained_comp,
    encode_binary(library),
    encode_binary(availability_ramps),
    encode_binary(medical_checkups),
    encode_binary(electricity)
]])

# ===============================
# 🔮 Prediction
# ===============================
st.markdown("### 🧠 Run Predictions")
if st.button("🚀 Predict Outcomes"):
    dropout_pred = xgb_reg.predict(X_reg_input)[0]
    retention_pred = xgb_cls.predict(X_cls_input)[0]
    retention_label = "High Retention 🟢" if retention_pred == 1 else "Low Retention 🔴"

    # ===============================
    # 📊 Display Results
    # ===============================
    st.success("✅ Prediction Complete!")

    colA, colB = st.columns(2)
    with colA:
        st.metric(label="📉 Predicted Dropout Rate", value=f"{dropout_pred*10:.2f}%")
    with colB:
        st.metric(label="🏫 Retention Category", value=retention_label)

    st.progress(min(dropout_pred, 1.0))
    st.divider()

    if retention_pred == 1:
        st.success("🌟 Great infrastructure and teaching staff are contributing to **high retention**.")
    else:
        st.warning("⚠️ Improvements needed in **facilities or teacher support** to improve retention.")

# ===============================
# 🧾 Footer
# ===============================
# st.markdown("""
# ---
# <p style='text-align:center;'>
# Built with ❤️ by <b>Neeraj</b> | TCET Datathon 2025 🚀
# </p>
# """, unsafe_allow_html=True)
st.markdown("""
<footer>
    <hr>
    <p>Made with ❤️ and purpose by <b>The Role Players</b><br>
    Empowering Education through Data</p>
</footer>
""", unsafe_allow_html=True)