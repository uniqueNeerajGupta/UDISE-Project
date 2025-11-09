import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title=" Analysis", layout="wide")
st.title("🏫 Which States Show Consistent Improvement Over the Last 3 Years?")
st.markdown("---")

# ---------------------------------
# LOAD DATA
# ---------------------------------
df = pd.read_parquet("preprocessed_prompt2.parquet")


# prompt1_tab, prompt2_tab , prompt3_tab , prompt4_tab, prompt5_tab = st.tabs([
#     "📈Prompt 1: State Improvement Trends",
#     "🎓Prompt 2: Dropout Influencing Factors",
#     "🏫Prompt 3: Infrastructure vs Performance"
#     ,"👩‍🏫Prompt 4: Teacher Quality " ,
#     "📊Prompt 5: Resource Allocation Efficiency",
#  ])
promt1_tab, prompt2_tab = st.tabs([
    "📈Prompt 1: State Improvement Trends",
    "🎓Prompt 2: Dropout Influencing Factors"])
with promt1_tab:
    st.header("Analysis: State-wise Improvement in School Facilities & Teacher Quality")
# KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total States + Union ", df["state"].nunique())
    col2.metric("Years Covered", df["year"].nunique())
    col3.metric("Avg Facility Index", f"{df['facility_index'].mean():.2f}")
    col4.metric("Avg Teacher Quality index ", f"{df['teacher_quality_index'].mean():.2f}")

# PREPROCESS
    trend = df.groupby(["state", "year"])[["facility_index", "teacher_quality_index"]].mean().reset_index()
    trend["facility_change"] = trend.groupby("state")["facility_index"].diff()
    trend["teacher_change"] = trend.groupby("state")["teacher_quality_index"].diff()
    avg_improvement = trend.groupby("state")[["facility_change", "teacher_change"]].mean().reset_index()

# ---------------------------------
# TABS LAYOUT
# ---------------------------------
    tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Trends Overview",
    "🔥 Heatmaps & Correlations",
    "🏆 Top Performers",
    "🧠 Insights & Policy"
      ])

# ==============================================================
# TAB 1 – TRENDS OVERVIEW
# ==============================================================
    with tab1:
         st.subheader("📈 Facility & Teacher Quality Trends")

         top_states = trend["state"].unique()[:5]
         colA, colB = st.columns(2)

    with colA:
        fig1 = px.line(
           
            trend[trend["state"].isin(top_states)],
            x="year", y="facility_index", color="state",
            markers=True, line_shape="spline",
            title="Facility Index Improvement (Top 5 States)"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with colB:
        fig2 = px.line(
            trend[trend["state"].isin(top_states)],
            x="year", y="teacher_quality_index", color="state",
            markers=True, line_shape="spline",
            title="Teacher Quality Index Improvement (Top 5 States)"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 📅 National Average Improvement")
    year_trend = trend.groupby("year")[["facility_index", "teacher_quality_index"]].mean().reset_index()
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=year_trend["year"], y=year_trend["facility_index"],
        mode="lines+markers", name="Facility Index",
        line=dict(color="royalblue", width=3)
    ))
    fig3.add_trace(go.Scatter(
        x=year_trend["year"], y=year_trend["teacher_quality_index"],
        mode="lines+markers", name="Teacher Quality Index",
        line=dict(color="darkorange", width=3)
    ))
    fig3.update_layout(
        template="plotly_white",
        xaxis_title="Year", yaxis_title="Average Index Value",
        title="National Average Improvement per Year"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ==============================================================
# TAB 2 – HEATMAPS & CORRELATIONS
# ==============================================================
    with tab2:
     import seaborn as sns
     import matplotlib.pyplot as plt

     st.subheader("🔥 Heatmap of Facility & Teacher Index Change")

     corr_df = avg_improvement.set_index("state")[["facility_change", "teacher_change"]]
     fig, ax = plt.subplots(figsize=(6, 4))
     sns.heatmap(corr_df.corr(), annot=True, cmap="YlGnBu", ax=ax)
     ax.set_title("Correlation between Facility & Teacher Quality Change")
     st.pyplot(fig)

     st.subheader("🌡️ State-wise Facility & Teacher Change")
     fig2, ax2 = plt.subplots(figsize=(10, 6))
     sns.heatmap(
        corr_df, annot=True, cmap="coolwarm", fmt=".2f",
        linewidths=0.5, ax=ax2
     )
     ax2.set_title("Facility & Teacher Quality Change Across States")
     st.pyplot(fig2)

# ==============================================================
# TAB 3 – TOP PERFORMERS
# ==============================================================
    with tab3:
     st.subheader("🏆 Top 10 Improving States (Overall)")
     top_states = avg_improvement.sort_values(by="facility_change", ascending=False).head(10)
     st.dataframe(top_states.style.highlight_max(axis=0, color="lightgreen"), use_container_width=True)

     st.markdown("### 🗺️ Select a State to View Trend")
     selected_state = st.selectbox("Choose a State", df["state"].unique())
     state_data = trend[trend["state"] == selected_state]

    fig4 = px.line(
        state_data, x="year", y=["facility_index", "teacher_quality_index"],
        markers=True, title=f"{selected_state} – Facility vs Teacher Quality Trend"
    )
    st.plotly_chart(fig4, use_container_width=True)

# ==============================================================
# TAB 4 – INSIGHTS & POLICY
# ==============================================================
    with tab4:
     st.subheader("🧠 Key Insights")
     st.write("""
     1. States with higher access to electricity, toilets, and libraries show consistent facility growth.  
     2. National average improvement indicates steady progress year over year.  
     3. States improving both teacher quality and facilities tend to have lower dropout rates.  
     4. Variability across states suggests uneven policy implementation.  
     5. Balanced investment in human & physical resources yields best results.  
     """)

    st.subheader("💡 Modelling Approach")
    st.write("""
    - Data preprocessed and saved as **Parquet** for speed.  
    - Built **Facility** and **Teacher Quality Indices** using weighted indicators.  
    - Aggregated by state & year to observe multi-year trends.  
    - Used `groupby()` and `diff()` to track year-to-year changes.  
    """)

    st.subheader("📜 Policy Recommendations")
    st.write("""
    1. Increase investment in libraries and laboratories in low-performing states.  
    2. Focus equally on **teacher training** and **infrastructure quality**.  
    3. Regular audits to ensure electricity and toilet facilities remain functional.  
    4. Develop **digital dashboards** to monitor improvement at district level.  
    """)

#     st.markdown("---")
#     st.caption("✨ Developed by Neeraj Gupta | Data Science & Analytics Enthusiast")


# # ---------------------------------
# PROMPT 2 TAB
# ---------------------------------
st.markdown("""
<footer>
    <hr>
    <p>Made with ❤️ and purpose by <b>The Role Players</b><br>
    Empowering Education through Data</p>
</footer>
""", unsafe_allow_html=True)