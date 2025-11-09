import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(page_title="School Infrastructure vs Enrollment", layout="wide", page_icon="🏫")

st.title("🏫 School Infrastructure vs Enrollment / Dropout Analysis")
st.markdown("Explore how school infrastructure affects student enrolment and retention.")

# --------------------------
# LOAD DATA (Optimized)
# --------------------------
@st.cache_data(show_spinner=True)
def load_data(path="df_main.csv", nrows=200000):
    # 🔹 Only load a sample (optional: remove nrows if full data fits memory)
    df = pd.read_csv(path, nrows=nrows)
    df['rural_urban'] = df['rural_urban'].astype(str).str.strip()

    # ✅ Convert only required columns
    cols = [
        'total_class_rooms','classrooms_in_good_condition','classrooms_needs_minor_repair',
        'classrooms_needs_major_repair','total_boys_func_toilet','total_girls_func_toilet',
        'func_boys_cwsn_friendly','func_girls_cwsn_friendly','library_availability',
        'electricity_availability','playground_available','total_tch','male','female',
        'transgender','pucca_building_blocks','no_building_blocks'
    ]
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # Derived columns
    df['total_func_toilet'] = df['total_boys_func_toilet'].fillna(0) + df['total_girls_func_toilet'].fillna(0)
    df['cwsn_toilet'] = df['func_boys_cwsn_friendly'].fillna(0) + df['func_girls_cwsn_friendly'].fillna(0)
    df['facility_index'] = df[['total_class_rooms','library_availability','electricity_availability','playground_available']].mean(axis=1)
    df['total_gender'] = df[['male','female','transgender']].sum(axis=1)

    return df

with st.spinner("Loading data..."):
    df = load_data()

# --------------------------
# FILTERS
# --------------------------
st.sidebar.header("Filters")
state = st.sidebar.selectbox("State", ["All"] + sorted(df['state'].dropna().unique()))
district = st.sidebar.selectbox("District", ["All"] + sorted(df['district'].dropna().unique()))
rural_urban = st.sidebar.multiselect("Rural/Urban", df['rural_urban'].unique(), default=df['rural_urban'].unique())

filtered_df = df.copy()
if state != "All":
    filtered_df = filtered_df[filtered_df['state']==state]
if district != "All":
    filtered_df = filtered_df[filtered_df['district']==district]
filtered_df = filtered_df[filtered_df['rural_urban'].isin(rural_urban)]

# --------------------------
# PRE-COMPUTE AGGREGATES
# --------------------------
@st.cache_data
def preprocess_grouped(df):
    grouped = df.groupby('rural_urban').agg({
        'classrooms_in_good_condition':'mean',
        'classrooms_needs_minor_repair':'mean',
        'classrooms_needs_major_repair':'mean',
        'total_func_toilet':'mean',
        'cwsn_toilet':'mean',
        'facility_index':'mean',
        'pucca_building_blocks':'mean',
        'no_building_blocks':'mean',
        'total_tch':'mean',
        'total_gender':'mean'
    }).reset_index()
    return grouped

grouped_df = preprocess_grouped(filtered_df)

# --------------------------
# METRICS
# --------------------------
col1,  col3, col4 = st.columns(3)
col1.metric("🏫 Avg Good Classrooms", f"{filtered_df['classrooms_in_good_condition'].mean():.1f}")
col3.metric("🚻 totol Functional Toilets", f"{filtered_df['total_func_toilet'].mean():.1f}")
col4.metric("📊 Avg Facility Index", f"{filtered_df['facility_index'].mean():.2f}")
st.markdown("---")

# --------------------------
# TABS
# --------------------------
tabs = st.tabs([
    "Classrooms Condition","Functional Toilets","CWSN Toilets",
    "Facility Index","Building Type","Rural vs Urban","Correlation Heatmap"
])

# 1️⃣ Classrooms Condition
with tabs[0]:
    fig = px.bar(grouped_df, x='rural_urban',
                 y=['classrooms_in_good_condition','classrooms_needs_minor_repair','classrooms_needs_major_repair'],
                 barmode='group', text_auto=True, color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

# 2️⃣ Functional Toilets
with tabs[1]:
    fig = px.bar(grouped_df, x='rural_urban', y='total_func_toilet', color='rural_urban',
                 text='total_func_toilet', color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig, use_container_width=True)

# 3️⃣ CWSN Toilets
with tabs[2]:
    fig = px.bar(grouped_df, x='rural_urban', y='cwsn_toilet', color='rural_urban',
                 text='cwsn_toilet', color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig, use_container_width=True)

# 4️⃣ Facility Index
with tabs[3]:
    fig = px.bar(grouped_df, x='rural_urban', y='facility_index', color='rural_urban',
                 text='facility_index', color_discrete_sequence=px.colors.qualitative.T10)
    st.plotly_chart(fig, use_container_width=True)

# 5️⃣ Building Type
with tabs[4]:
    fig = px.bar(grouped_df, x='rural_urban', y=['pucca_building_blocks','no_building_blocks'],
                 barmode='group', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# 6️⃣ Rural vs Urban (FAST MODE)
with tabs[5]:
    fig = px.box(filtered_df.sample(min(5000, len(filtered_df))), x='rural_urban',
                 y='facility_index', color='rural_urban',
                 points="outliers", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

# 7️⃣ Correlation Heatmap
with tabs[6]:
    corr_cols = ['classrooms_in_good_condition','classrooms_needs_minor_repair','classrooms_needs_major_repair',
                 'total_func_toilet','cwsn_toilet','facility_index','total_tch','total_gender']
    corr_df = filtered_df[corr_cols].corr()
    fig = px.imshow(corr_df, text_auto=True, color_continuous_scale='Blues', width=700, height=700)
    st.plotly_chart(fig, use_container_width=True)
st.markdown("""
<footer>
    <hr>
    <p>Made with ❤️ and purpose by <b>The Role Players</b><br>
    Empowering Education through Data</p>
</footer>
""", unsafe_allow_html=True)