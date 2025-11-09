import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------
st.set_page_config(
    page_title="Teacher & Toilet Influence on Retention",
    layout="wide",
    page_icon="📈"
)

st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom right, #f0f7ff, #e6f0ff);
    }
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f7faff;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        color: #0b3d91;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0b3d91 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Teacher & Functional Toilet Availability and Retention Dashboard")
st.markdown("#### Explore how school infrastructure and teacher availability affect student retention.")

# ----------------------------------
# LOAD DATA
# ----------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("df_main.csv")  # Replace with your CSV file path
    num_cols = [
        'total_tch', 'male', 'female', 'trained_comp',
        'total_boys_func_toilet', 'total_girls_func_toilet',
        'func_boys_cwsn_friendly', 'func_girls_cwsn_friendly',
        'total_class_rooms', 'library_availability',
        'electricity_availability', 'playground_available'
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Derived columns
    df['total_func_toilet'] = df['total_boys_func_toilet'].fillna(0) + df['total_girls_func_toilet'].fillna(0)
    df['cwsn_toilet'] = df['func_boys_cwsn_friendly'].fillna(0) + df['func_girls_cwsn_friendly'].fillna(0)
    df['facility_index'] = df[['total_class_rooms','library_availability','electricity_availability','playground_available']].mean(axis=1)
    return df

df = load_data()

# ----------------------------------
# FILTERS
# ----------------------------------
st.sidebar.header("🔍 Filters")

state = st.sidebar.selectbox("Select State", ["All"] + sorted(df['state'].dropna().unique().tolist()))
district = st.sidebar.selectbox("Select District", ["All"] + sorted(df['district'].dropna().unique().tolist()))
rural_urban = st.sidebar.multiselect("Select Rural/Urban", df['rural_urban'].dropna().unique().tolist(), default=df['rural_urban'].dropna().unique().tolist())

filtered_df = df.copy()
if state != "All":
    filtered_df = filtered_df[filtered_df['state'] == state]
if district != "All":
    filtered_df = filtered_df[filtered_df['district'] == district]
filtered_df = filtered_df[filtered_df['rural_urban'].isin(rural_urban)]

# ----------------------------------
# METRIC SUMMARY
# ----------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("👩‍🏫 Avg Teachers", f"{filtered_df['total_tch'].mean():.1f}")
col2.metric("🚻 Avg Functional Toilets", f"{filtered_df['total_func_toilet'].mean():.1f}")
col3.metric("🎓 Trained Teachers (%)", f"{filtered_df['trained_comp'].mean():.1f}")
col4.metric("🏫 Facility Index", f"{filtered_df['facility_index'].mean():.2f}")

st.markdown("---")

# ----------------------------------
# 7 TABS
# ----------------------------------
tabs = st.tabs([
    "Total Teachers",
    "Functional Toilets",
    "Trained Teachers",
    "Teacher Gender",
    "CWSN Toilets",
    "Facility Index",
    "Urban vs Rural"
])

# TAB 1: Teachers
with tabs[0]:
    st.subheader("1️⃣ Total Teachers vs Retention")
    agg = filtered_df.groupby('rural_urban')['total_tch'].mean().reset_index()
    fig = px.bar(agg, x='rural_urban', y='total_tch', text='total_tch',
                 color='rural_urban', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    **Insights:**
    - Rural schools have significantly fewer teachers on average.
    - More teachers lead to better student attention and lower dropout rates.
    
    **Recommendation:** Deploy additional teachers to rural schools for balanced staffing.
    """)

# TAB 2: Toilets
with tabs[1]:
    st.subheader("2️⃣ Functional Toilets and Retention")
    agg = filtered_df.groupby('rural_urban')['total_func_toilet'].mean().reset_index()
    fig = px.bar(agg, x='rural_urban', y='total_func_toilet', text='total_func_toilet',
                 color='rural_urban', color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Insights:**
    - Urban schools generally have more functional toilets than rural ones.
    - Proper toilet facilities encourage better attendance and retention.
    
    **Recommendation:** Invest in functional toilets, especially for girls in rural areas.
    """)

# TAB 3: Trained Teachers
with tabs[2]:
    st.subheader("3️⃣ Trained Teachers vs Retention")
    agg = filtered_df.groupby('rural_urban')['trained_comp'].mean().reset_index()
    fig = px.bar(agg, x='rural_urban', y='trained_comp', text='trained_comp',
                 color='rural_urban', color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Insights:**
    - Teacher training levels are higher in urban schools.
    - Well-trained teachers improve learning and student satisfaction.
    
    **Recommendation:** Launch regular upskilling programs for rural teachers.
    """)

# TAB 4: Gender
with tabs[3]:
    st.subheader("4️⃣ Gender Distribution of Teachers")
    agg = filtered_df.groupby('rural_urban')[['male','female']].sum().reset_index()
    gender_df = agg.melt(id_vars='rural_urban', var_name='Gender', value_name='Count')
    fig = px.bar(gender_df, x='Gender', y='Count', color='rural_urban', barmode='group',
                 color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Insights:**
    - Female teacher representation is much lower in rural areas.
    - Female teachers improve gender inclusivity and retention of girl students.
    
    **Recommendation:** Provide incentives for female teachers to work in rural schools.
    """)

# TAB 5: CWSN Toilets
with tabs[4]:
    st.subheader("5️⃣ CWSN Friendly Toilets and Retention")
    agg = filtered_df.groupby('rural_urban')['cwsn_toilet'].mean().reset_index()
    fig = px.bar(agg, x='rural_urban', y='cwsn_toilet', text='cwsn_toilet',
                 color='rural_urban', color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Insights:**
    - Inclusive infrastructure is lacking in many rural schools.
    - CWSN-friendly toilets help children with disabilities stay enrolled longer.
    
    **Recommendation:** Prioritize accessible toilet infrastructure for inclusivity.
    """)

# TAB 6: Facility Index
with tabs[5]:
    st.subheader("6️⃣ Facility Index and Retention")
    agg = filtered_df.groupby('rural_urban')['facility_index'].mean().reset_index()
    fig = px.bar(agg, x='rural_urban', y='facility_index', text='facility_index',
                 color='rural_urban', color_discrete_sequence=px.colors.qualitative.T10)
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Insights:**
    - Facility availability is higher in urban schools.
    - Schools with good classrooms, libraries, and electricity show higher retention.
    
    **Recommendation:** Focus on holistic facility upgrades in rural schools.
    """)

# TAB 7: Urban vs Rural Comparison
with tabs[6]:
    st.subheader("7️⃣ Urban vs Rural Overview")
    agg = filtered_df.groupby('rural_urban')[['total_tch','total_func_toilet']].mean().reset_index()
    fig = px.line(agg.melt(id_vars='rural_urban'), x='rural_urban', y='value',
                  color='variable', markers=True, text='value')
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Insights:**
    - Urban areas lead in both staff and sanitation infrastructure.
    - Balanced improvement in both aspects can boost rural retention.
    
    **Recommendation:** Jointly address staffing and sanitation gaps in rural schools.
    """)
st.markdown("""
<footer>
    <hr>
    <p>Made with ❤️ and purpose by <b>The Role Players</b><br>
    Empowering Education through Data</p>
</footer>
""", unsafe_allow_html=True)