import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(page_title="Dropout & Retention Analysis", layout="wide", page_icon="🎓")

st.markdown("""
<style>
.main {background: linear-gradient(to bottom right, #f7f9ff, #e6f0ff);}
.stTabs [data-baseweb="tab-list"] {justify-content: center; gap: 20px;}
.stTabs [data-baseweb="tab"] {background-color: #f7faff; border-radius: 10px; padding: 10px 20px; font-weight:600; color:#0b3d91;}
.stTabs [aria-selected="true"] {background-color:#0b3d91 !important; color:white !important;}
</style>
""", unsafe_allow_html=True)

st.title("🎓 Dropout & Retention Analysis: Urban vs Rural, Gender, Caste")
st.markdown("Explore teacher allocation, gender, caste, and infrastructure influence on retention.")

# --------------------------
# LOAD & CLEAN DATA
# --------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("df_main.csv")  # replace with actual path
    
    df['rural_urban'] = df['rural_urban'].astype(str).str.strip()
    
    numeric_cols = ['total_tch','male','female','transgender','gen_tch','sc_tch','st_tch','obc_tch',
                    'trained_comp','post_graduate_and_above','graduate','below_graduate',
                    'total_class_rooms','library_availability','electricity_availability','playground_available']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['total_gender'] = df[['male','female','transgender']].sum(axis=1)
    df['facility_index'] = df[['total_class_rooms','library_availability','electricity_availability','playground_available']].mean(axis=1)
    
    return df

df = load_data()

# --------------------------
# SIDEBAR FILTERS
# --------------------------
st.sidebar.header("🔍 Filters")
state = st.sidebar.selectbox("State", ["All"] + sorted(df['state'].dropna().unique().tolist()))
district = st.sidebar.selectbox("District", ["All"] + sorted(df['district'].dropna().unique().tolist()))
rural_urban = st.sidebar.multiselect("Rural/Urban", df['rural_urban'].dropna().unique().tolist(), default=df['rural_urban'].dropna().unique().tolist())

filtered_df = df.copy()
if state != "All":
    filtered_df = filtered_df[filtered_df['state'] == state]
if district != "All":
    filtered_df = filtered_df[filtered_df['district'] == district]
filtered_df = filtered_df[filtered_df['rural_urban'].isin(rural_urban)]

# --------------------------
# METRICS
# --------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("👩‍🏫 Avg Teachers", f"{filtered_df['total_tch'].mean():.1f}")
col2.metric("🚻 Avg Total Gender Teachers", f"{filtered_df['total_gender'].mean():.1f}")
col3.metric("🎓 Trained Teachers (%)", f"{filtered_df['trained_comp'].mean():.1f}")
col4.metric("🏫 Facility Index", f"{filtered_df['facility_index'].mean():.2f}")

st.markdown("---")

# --------------------------
# TABS
# --------------------------
tabs = st.tabs([
    "Total Teachers", "Gender Distribution", "Caste Distribution",
    "Teacher Qualification", "Trained Teachers", "Facility Index", "Class Range"
])

# --------------------------
# TAB 1: Total Teachers
# --------------------------
with tabs[0]:
    st.subheader("1️⃣ Total Teachers / Students by Rural vs Urban")
    agg = filtered_df.groupby('rural_urban')['total_gender'].sum().reset_index()
    fig = px.bar(agg, x='rural_urban', y='total_gender', color='rural_urban', text='total_gender',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Insights:** Rural schools have fewer teachers. Female teacher % is lower in rural areas. Imbalanced allocation affects retention.
    **Recommendation:** Recruit more teachers, especially female, in rural schools.
    """)

# --------------------------
# TAB 2: Gender Distribution
# --------------------------
with tabs[1]:
    st.subheader("2️⃣ Gender Distribution")
    agg = filtered_df.groupby('rural_urban')[['male','female','transgender']].sum().reset_index()
    gender_df = agg.melt(id_vars='rural_urban', var_name='Gender', value_name='Count')
    fig = px.bar(gender_df, x='Gender', y='Count', color='rural_urban', barmode='group',
                 color_discrete_sequence=px.colors.qualitative.Safe, text='Count')
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Insights:** Male teachers dominate, rural schools have lower female representation.
    **Recommendation:** Increase female teachers in rural schools.
    """)

# --------------------------
# TAB 3: Caste Distribution
# --------------------------
with tabs[2]:
    st.subheader("3️⃣ Caste Distribution")
    agg = filtered_df.groupby('rural_urban')[['gen_tch','sc_tch','st_tch','obc_tch']].sum().reset_index()
    caste_df = agg.melt(id_vars='rural_urban', var_name='Caste', value_name='Count')
    fig = px.bar(caste_df, x='Caste', y='Count', color='rural_urban', barmode='group',
                 color_discrete_sequence=px.colors.qualitative.Prism, text='Count')
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Insights:** SC/ST underrepresented in urban areas. General category dominates both rural/urban.
    **Recommendation:** Focus on equitable caste representation for teacher recruitment.
    """)

# --------------------------
# TAB 4: Teacher Qualification
# --------------------------
with tabs[3]:
    st.subheader("4️⃣ Teacher Qualification")
    agg = filtered_df.groupby('rural_urban')[['below_graduate','graduate','post_graduate_and_above']].sum().reset_index()
    qual_df = agg.melt(id_vars='rural_urban', var_name='Qualification', value_name='Count')
    fig = px.bar(qual_df, x='Qualification', y='Count', color='rural_urban', barmode='group',
                 color_discrete_sequence=px.colors.qualitative.Set2, text='Count')
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Insights:** Rural schools have more below-graduate teachers. Graduate/post-grad concentrated in urban areas.
    **Recommendation:** Improve qualification levels in rural schools via training/education.
    """)

# --------------------------
# TAB 5: Trained Teachers
# --------------------------
with tabs[4]:
    st.subheader("5️⃣ Trained Teachers")
    agg = filtered_df.groupby('rural_urban')['trained_comp'].sum().reset_index()
    fig = px.bar(agg, x='rural_urban', y='trained_comp', color='rural_urban', text='trained_comp',
                 color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Insights:** Urban schools have more trained teachers.
    **Recommendation:** Expand teacher training in rural schools.
    """)

# --------------------------
# TAB 6: Facility Index
# --------------------------
with tabs[5]:
    st.subheader("6️⃣ Facility Index")
    agg = filtered_df.groupby('rural_urban')['facility_index'].mean().reset_index()
    fig = px.bar(agg, x='rural_urban', y='facility_index', color='rural_urban', text='facility_index',
                 color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Insights:** Facility index higher in urban schools. Rural schools lack classrooms, electricity, libraries, playgrounds.
    **Recommendation:** Improve infrastructure to reduce dropouts.
    """)

# --------------------------
# TAB 7: Class Range
# --------------------------
with tabs[6]:
    st.subheader("7️⃣ Class Range vs Total Teachers")
    agg = filtered_df.groupby(['rural_urban','highclass'])['total_tch'].sum().reset_index()
    fig = px.line(agg, x='highclass', y='total_tch', color='rural_urban', markers=True)
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Insights:** Teacher numbers drop in higher classes in rural schools, indicating dropout risk.
    **Recommendation:** Adjust teacher allocation across classes in rural schools.
    """)
st.markdown("""
<footer>
    <hr>
    <p>Made with ❤️ and purpose by <b>The Role Players</b><br>
    Empowering Education through Data</p>
</footer>
""", unsafe_allow_html=True)