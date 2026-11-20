import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Online Course Completion Analysis",
    page_icon="🎓",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 16px;
        color: #666;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 Online Course Completion Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Data Science Mini Project | Student Retention & Course Performance Analytics</div>', unsafe_allow_html=True)

# Load Data
@st.cache_data
def get_data():
    try:
        df = pd.read_csv("cleaned_online_course_data.csv")
    except Exception:
        df = pd.read_csv("online_course_data.csv")
    df["Completed Modules"] = df["Completed Modules"].fillna(0).astype(int)
    df["Completion Percentage"] = ((df["Completed Modules"] / df["Total Modules"]) * 100).round(2)
    df["Completion Status"] = np.where(df["Completed Modules"] == df["Total Modules"], "Completed", "Incomplete")
    return df

df = get_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
categories = ["All"] + sorted(list(df["Course Category"].unique()))
selected_cat = st.sidebar.selectbox("Course Category", categories)

status_options = ["All", "Completed", "Incomplete"]
selected_status = st.sidebar.selectbox("Completion Status", status_options)

# Filter dataframe
filtered_df = df.copy()
if selected_cat != "All":
    filtered_df = filtered_df[filtered_df["Course Category"] == selected_cat]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df["Completion Status"] == selected_status]

# Top KPI Metric Cards
total_enrolled = len(filtered_df)
total_completed = (filtered_df["Completion Status"] == "Completed").sum()
completion_rate = round((total_completed / total_enrolled * 100), 2) if total_enrolled > 0 else 0
avg_progress = round(filtered_df["Completion Percentage"].mean(), 2) if total_enrolled > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Enrollments", f"{total_enrolled}")
col2.metric("Total Completed", f"{total_completed}")
col3.metric("Completion Rate", f"{completion_rate}%")
col4.metric("Avg Student Progress", f"{avg_progress}%")

st.markdown("---")

# Visualizations Row 1
c1, c2 = st.columns(2)

with c1:
    st.subheader("📊 Enrollments by Course")
    if len(filtered_df) > 0:
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        order = filtered_df["Course Name"].value_counts().index
        sns.countplot(data=filtered_df, y="Course Name", order=order, hue="Course Name", palette="viridis", legend=False, ax=ax1)
        ax1.set_xlabel("Enrolled Students")
        ax1.set_ylabel("")
        st.pyplot(fig1)
        plt.close(fig1)

with c2:
    st.subheader("🥧 Overall Completion Breakdown")
    if len(filtered_df) > 0:
        fig2, ax2 = plt.subplots(figsize=(6, 5))
        counts = filtered_df["Completion Status"].value_counts()
        colors = ["#2ecc71", "#e74c3c"] if "Completed" in counts.index and counts.index[0] == "Completed" else ["#e74c3c", "#2ecc71"]
        ax2.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=140, colors=colors)
        st.pyplot(fig2)
        plt.close(fig2)

st.markdown("---")

# Visualizations Row 2: Course-wise and Category-wise Completion Rates
c3, c4 = st.columns(2)

# Course Summary Aggregation
course_summary = df.groupby(["Course Name", "Course Category"]).agg(
    Total_Enrollments=("Student ID", "count"),
    Total_Modules=("Total Modules", "first"),
    Avg_Completed_Modules=("Completed Modules", "mean"),
    Completed_Count=("Completion Status", lambda x: (x == "Completed").sum()),
    Avg_Completion_Pct=("Completion Percentage", "mean")
).reset_index()

course_summary["Completion_Rate_%"] = (
    (course_summary["Completed_Count"] / course_summary["Total_Enrollments"]) * 100
).round(2)
course_summary = course_summary.sort_values(by="Completion_Rate_%", ascending=True)

with c3:
    st.subheader("📈 Course Completion Rates (%)")
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    colors = ["#e74c3c" if x < 50 else "#f39c12" if x < 65 else "#27ae60" for x in course_summary["Completion_Rate_%"]]
    bars = ax3.barh(course_summary["Course Name"], course_summary["Completion_Rate_%"], color=colors, edgecolor="black")
    ax3.set_xlim(0, 100)
    for b in bars:
        w = b.get_width()
        ax3.text(w + 1, b.get_y() + b.get_height() / 2, f"{w:.1f}%", va="center", fontsize=9, fontweight="bold")
    st.pyplot(fig3)
    plt.close(fig3)

with c4:
    st.subheader("🏷️ Category Completion Rates (%)")
    cat_summary = df.groupby("Course Category").agg(
        Total_Enrollments=("Student ID", "count"),
        Completed_Count=("Completion Status", lambda x: (x == "Completed").sum())
    ).reset_index()
    cat_summary["Category_Completion_Rate_%"] = (
        (cat_summary["Completed_Count"] / cat_summary["Total_Enrollments"]) * 100
    ).round(2)
    cat_summary = cat_summary.sort_values(by="Category_Completion_Rate_%", ascending=False)
    
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    ax4 = sns.barplot(data=cat_summary, x="Course Category", y="Category_Completion_Rate_%", hue="Course Category", palette="magma", legend=False, edgecolor="black")
    ax4.set_ylim(0, 100)
    for p in ax4.patches:
        h = p.get_height()
        ax4.annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2, h + 2), ha="center", fontweight="bold")
    st.pyplot(fig4)
    plt.close(fig4)

st.markdown("---")

# Data Table View
st.subheader("📋 Student Enrollment Dataset")
st.dataframe(filtered_df, use_container_width=True)

st.download_button(
    label="📥 Download Cleaned Dataset (CSV)",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="online_course_data_filtered.csv",
    mime="text/csv"
)
