import streamlit as st

# --- Page Setup ---
st.set_page_config(page_title="THE ROLE PLAYERS | Student Retention Model", page_icon="🎓", layout="wide")

# --- Custom CSS for Elegant Blur + Animation ---
st.markdown("""
    <style>
    /* Background gradient animation */
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    body {
        background: linear-gradient(-45deg, #1e3c72, #2a5298, #355caa, #1b3b6f);
        background-size: 400% 400%;
        animation: gradientMove 12s ease infinite;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    .main-title {
        text-align: center;
        font-size: 68px;
        font-weight: 900;
        letter-spacing: 3px;
        color: #ffffff;
        text-shadow: 0 0 20px rgba(0, 191, 255, 0.6), 3px 3px 20px rgba(0, 0, 0, 0.4);
        margin-top: 60px;
        animation: fadeIn 2s ease;
    }

    .subtext {
        text-align: center;
        font-size: 22px;
        color: #d4e4ff;
        margin-top: -10px;
        letter-spacing: 1px;
        animation: fadeIn 3s ease;
    }

    .blur-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 25px;
        padding: 40px 50px;
        margin: 70px auto;
        width: 75%;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        color: #f0f4ff;
        animation: fadeIn 3s ease;
    }

    h3 {
        text-align: center;
        font-size: 32px;
        color: #00eaff;
        margin-bottom: 25px;
        text-shadow: 0 0 15px rgba(0, 234, 255, 0.5);
    }

    ul {
        list-style-type: "🚀 ";
        line-height: 1.9;
        font-size: 19px;
        transition: 0.3s;
    }

    ul li:hover {
        color: #a5f3fc;
        transform: scale(1.01);
        text-shadow: 0 0 10px rgba(173, 216, 230, 0.6);
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.4), transparent);
        margin: 2rem 0;
    }

    footer {
        text-align: center;
        margin-top: 50px;
        font-size: 16px;
        color: rgba(255,255,255,0.8);
        animation: fadeIn 4s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# --- Title Section ---
st.markdown('<h1 class="main-title">THE ROLE PLAYERS</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtext">Student Retention & Dropout Prediction Model 🎯</p>', unsafe_allow_html=True)

# --- Blur Info Card ---
st.markdown("""
<div class="blur-card">
    <h3>About the Model</h3>
    <ul>
        <li>Predicts likelihood of student <b>dropout</b> using advanced machine learning algorithms.</li>
        <li>Analyzes multiple dimensions: <b>attendance, performance, and engagement behavior</b>.</li>
        <li>Identifies <b>at-risk students</b> early to trigger timely interventions.</li>
        <li>Empowers institutions to design <b>evidence-based retention strategies</b>.</li>
        <li>Transforms educational data into <b>actionable insights</b> for student success.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<footer>
    <hr>
    <p>Made with ❤️ and purpose by <b>The Role Players</b><br>
    Empowering Education through Data</p>
</footer>
""", unsafe_allow_html=True)
