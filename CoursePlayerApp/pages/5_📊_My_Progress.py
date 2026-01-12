"""
CoursePlayerApp - My Progress

Detailed progress analytics and visualizations.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="My Progress - GAI-Observe Academy",
    page_icon="📊",
    layout="wide"
)

# Authentication check
if not st.session_state.get("authenticated"):
    st.warning("⚠️ Please log in to access this page")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

tier = st.session_state.get("tier", "basic")

# Header
st.title("📊 My Progress")
st.markdown("---")

# Course selector and export
col1, col2 = st.columns([3, 1])

with col1:
    course = st.selectbox("Select Course", ["All Courses", "NLP with Transformers", "ML Fundamentals"])

with col2:
    if tier in ["intermediate", "advanced"]:
        st.download_button(
            label="📥 Export CSV",
            data=b"course,module,progress\nAI-03,Module 1,100",
            file_name="progress.csv",
            mime="text/csv"
        )
    else:
        st.button("📥 Export CSV", disabled=True, help="Export available in Intermediate tier")

st.markdown("---")

# Overall progress
st.subheader("Overall Progress: 67%")
st.progress(0.67)

st.markdown("---")

# Time spent chart
st.subheader("⏱️ Time Spent (Last 30 Days)")

if tier in ["intermediate", "advanced"]:
    # Mock data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    hours = [2.5, 1.5, 3.0, 0.5, 2.0, 3.5, 1.0] * 4 + [2.5, 1.5]
    
    df = pd.DataFrame({
        'Date': dates,
        'Hours': hours[:30]
    })
    
    fig = px.line(df, x='Date', y='Hours', title='Daily Learning Time')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("🔒 Time tracking is available in Intermediate tier ($247)")

st.markdown("---")

# Quiz performance
st.subheader("📝 Quiz Performance")

quiz_data = pd.DataFrame({
    'Quiz': ['Module 1 Quiz', 'Module 2 Quiz', 'Module 3 Quiz'],
    'Score': [85, 90, 75]
})

fig2 = px.bar(quiz_data, x='Quiz', y='Score', title='Quiz Scores', color='Score', color_continuous_scale='RdYlGn')
fig2.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Passing: 70%")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Activity heatmap (Advanced tier only)
if tier == "advanced":
    st.subheader("🔥 Activity Heatmap")
    
    # Mock heatmap data
    import numpy as np
    
    weeks = 12
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    data = np.random.randint(0, 5, size=(len(days), weeks))
    
    fig3 = go.Figure(data=go.Heatmap(
        z=data,
        x=[f'Week {i+1}' for i in range(weeks)],
        y=days,
        colorscale='Greens'
    ))
    fig3.update_layout(title='Learning Activity Heatmap (GitHub-style)')
    st.plotly_chart(fig3, use_container_width=True)
elif tier == "intermediate":
    st.info("🔒 Activity heatmap is available in Advanced tier ($497)")

st.markdown("---")

# Module breakdown
st.subheader("📚 Module Breakdown")

module_progress = pd.DataFrame({
    'Module': ['Module 1', 'Module 2', 'Module 3', 'Module 4'],
    'Videos': [100, 100, 80, 0],
    'Labs': [100, 100, 50, 0],
    'Quizzes': [85, 90, 75, 0]
})

st.dataframe(module_progress, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("**Note**: This is a placeholder implementation. See documentation for full implementation details.")
