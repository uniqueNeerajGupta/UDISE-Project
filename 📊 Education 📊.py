import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(page_title="Socioeconomic Impact on Enrolment", layout="wide", page_icon="📊")
st.markdown("""
<style>
.main {background: linear-gradient(to bottom right, #f7f9ff, #e6f0ff);}
.stTabs [data-baseweb="tab-list"] {justify-content: center; gap: 20px;}
.stTabs [data-baseweb="tab"] {background-color: #f7faff; border-radius: 10px; padding: 10px 20px; font-weight:600; color:#0b3d91;}
.stTabs [aria-selected="true"] {background-color:#0b3d91 !important; color:white !important;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Household Income, Parental Education & Employment vs Enrolment/Dropout")
st.markdown("Explore socio-economic factors affecting student enrolment and retention using school proxies.")

# --------------------------
# LOAD DATA
# --------------------------
@st.cache_data
def load_data(path="df_main.csv"):
    df = pd.read_csv(path)
    df['rural_urban'] = df['rural_urban'].astype(str).str.strip()
    
    # Numeric columns
    numeric_cols = ['total_tch','male','female','transgender','total_class_rooms',
                    'library_availability','electricity_availability','playground_available']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Derived columns
    df['total_gender'] = df[['male','female','transgender']].sum(axis=1)
    df['facility_index'] = df[['total_class_rooms','library_availability','electricity_availability','playground_available']].mean(axis=1)
    
    return df

df = load_data()

# --------------------------
# FILTERS
# --------------------------
st.sidebar.header("Filters")
state = st.sidebar.selectbox("State", ["All"] + sorted(df['state'].dropna().unique().tolist()))
district = st.sidebar.selectbox("District", ["All"] + sorted(df['district'].dropna().unique().tolist()))
rural_urban = st.sidebar.multiselect("Rural/Urban", df['rural_urban'].dropna().unique().tolist(), default=df['rural_urban'].dropna().unique().tolist())

filtered_df = df.copy()
if state != "All":
    filtered_df = filtered_df[filtered_df['state']==state]
if district != "All":
    filtered_df = filtered_df[filtered_df['district']==district]
filtered_df = filtered_df[filtered_df['rural_urban'].isin(rural_urban)]

# --------------------------
# METRICS
# --------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏫 Total Teachers", f"{filtered_df['total_tch'].sum():.0f}")
col2.metric("👩‍🏫 Female Teachers", f"{filtered_df['female'].sum():.0f}")
col3.metric("🏫 Total Students (Proxy)", f"{filtered_df['total_gender'].sum():.0f}")
col4.metric("🏫 Facility Index", f"{filtered_df['facility_index'].mean():.2f}")
st.markdown("---")

# --------------------------
# PRE-COMPUTE AGGREGATES
# --------------------------
@st.cache_data
def preprocess_grouped(df):
    grouped_rural = df.groupby('rural_urban').agg({
        'total_gender':'sum',
        'total_tch':'mean',
        'facility_index':'mean'
    }).reset_index()
    
    grouped_school = df.groupby('school_type').agg({'total_gender':'sum'}).reset_index()
    grouped_class = df.groupby('highclass').agg({'total_gender':'sum'}).reset_index()
    return grouped_rural, grouped_school, grouped_class

grouped_rural, grouped_school, grouped_class = preprocess_grouped(filtered_df)

# --------------------------
# TABS
# --------------------------
tabs = st.tabs([
    "Enrolment vs Teachers","Facility Index","School Type","Highclass/Lowclass","Rural vs Urban","Correlation Heatmap","Socioeconomic Proxy"
])

# --------------------------
# Tab 1: Enrolment vs Teachers
# --------------------------
with tabs[0]:
    st.subheader("1️⃣ Student Enrolment vs Teachers (Aggregated)")
    agg = filtered_df.groupby('rural_urban').agg({'total_tch':'mean','total_gender':'sum'}).reset_index()
    fig = px.scatter(agg, x='total_tch', y='total_gender', color='rural_urban', size='total_gender',
                     labels={'total_tch':'Average Teachers','total_gender':'Total Students'}, hover_data=['rural_urban'])
    st.plotly_chart(fig, use_container_width=True)
    st.info("More teachers correlate with higher student enrolment, especially in rural schools.")

# --------------------------
# Tab 2: Facility Index
# --------------------------
with tabs[1]:
    st.subheader("2️⃣ Facility Index vs Enrolment (Aggregated)")
    agg = filtered_df.groupby('rural_urban').agg({'facility_index':'mean','total_gender':'sum'}).reset_index()
    fig = px.scatter(agg, x='facility_index', y='total_gender', color='rural_urban', size='total_gender',
                     labels={'facility_index':'Facility Index','total_gender':'Total Students'}, hover_data=['rural_urban'])
    st.plotly_chart(fig, use_container_width=True)
    st.info("Better school facilities correlate with higher enrolment and lower dropout rates.")

# --------------------------
# Tab 3: School Type
# --------------------------
with tabs[2]:
    st.subheader("3️⃣ Enrolment by School Type")
    agg = filtered_df.groupby('school_type').agg({'total_gender':'sum'}).reset_index()
    fig = px.bar(agg, x='school_type', y='total_gender', text='total_gender', color='school_type')
    st.plotly_chart(fig, use_container_width=True)
    st.info("Private/residential schools have higher enrolment compared to government schools.")

# --------------------------
# Tab 4: Highclass / Lowclass
# --------------------------
with tabs[3]:
    st.subheader("4️⃣ Highclass vs Lowclass vs Enrollment")
    agg = filtered_df.groupby('highclass').agg({'total_gender':'sum'}).reset_index()
    fig = px.bar(agg, x='highclass', y='total_gender', text='total_gender', color='highclass')
    st.plotly_chart(fig, use_container_width=True)
    st.info("Upper classes may have higher dropout risk in rural areas; proxy for household education and employment influence.")

# --------------------------
# Tab 5: Rural vs Urban
# --------------------------
with tabs[4]:
    st.subheader("5️⃣ Rural vs Urban Enrolment")
    agg = filtered_df.groupby('rural_urban').agg({'total_gender':'sum'}).reset_index()
    fig = px.bar(agg, x='rural_urban', y='total_gender', text='total_gender', color='rural_urban')
    st.plotly_chart(fig, use_container_width=True)
    st.info("Urban schools tend to have higher enrolment due to better household income and parental education levels.")

# --------------------------
# Tab 6: Correlation Heatmap
# --------------------------
with tabs[5]:
    st.subheader("6️⃣ Correlation Heatmap (Proxy Socioeconomic)")
    cols = ['total_gender','total_tch','facility_index','total_class_rooms']
    corr = filtered_df[cols].corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)
    st.info("Higher teacher numbers and better facilities positively correlate with student enrolment.")

# --------------------------
# Tab 7: Socioeconomic Proxy
# --------------------------
with tabs[6]:
    st.subheader("7️⃣ Socioeconomic Proxy Analysis")
    agg = filtered_df.groupby(['rural_urban','school_type']).agg({'total_gender':'sum','total_tch':'mean','facility_index':'mean'}).reset_index()
    fig = px.scatter(agg, x='facility_index', y='total_tch', size='total_gender', color='rural_urban',
                     hover_data=['school_type'], labels={'facility_index':'Facility Index','total_tch':'Average Teachers'})
    st.plotly_chart(fig, use_container_width=True)
    st.info("Facility index & teachers act as proxy for household income and parental education, affecting enrolment & retention.")
st.markdown("""
<footer>
    <hr>
    <p>Made with ❤️ and purpose by <b>The Role Players</b><br>
    Empowering Education through Data</p>
</footer>
""", unsafe_allow_html=True)