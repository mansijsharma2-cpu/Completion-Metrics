import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Ensure output directory exists
os.makedirs("images", exist_ok=True)

# ----------------------------------------------------------------------
# 1. SYNTHETIC DATASET GENERATION
# ----------------------------------------------------------------------
courses_info = [
    {"name": "Python for Beginners", "category": "Programming", "modules": 10, "completion_tendency": 0.72},
    {"name": "Java Programming Fundamentals", "category": "Programming", "modules": 12, "completion_tendency": 0.58},
    {"name": "Data Science with Python", "category": "Data Science", "modules": 14, "completion_tendency": 0.52},
    {"name": "Machine Learning & Deep Learning", "category": "Data Science", "modules": 16, "completion_tendency": 0.38},
    {"name": "Full-Stack Web Development", "category": "Web Development", "modules": 15, "completion_tendency": 0.45},
    {"name": "Frontend with React & UI Design", "category": "Web Development", "modules": 10, "completion_tendency": 0.65},
    {"name": "Digital Marketing Strategies", "category": "Business & Marketing", "modules": 8, "completion_tendency": 0.78},
    {"name": "Product Management Essentials", "category": "Business & Marketing", "modules": 8, "completion_tendency": 0.68},
]

student_first_names = [
    "Aarav", "Ananya", "Rohan", "Pooja", "Rahul", "Sneha", "Vikram", "Neha",
    "Aditya", "Ishita", "Siddharth", "Kavya", "Arjun", "Tanvi", "Karan", "Riya",
    "Alex", "Emma", "Liam", "Olivia", "Noah", "Ava", "Lucas", "Mia",
    "David", "Sophia", "Ethan", "Zoe", "Daniel", "Chloe", "Ryan", "Grace"
]

student_last_names = [
    "Sharma", "Patel", "Verma", "Gupta", "Mehta", "Reddy", "Nair", "Singh",
    "Iyer", "Kumar", "Chopra", "Joshi", "Smith", "Johnson", "Brown", "Taylor",
    "Miller", "Wilson", "Davis", "Martinez", "Anderson", "Thomas", "White", "Harris"
]

# Generate 600 student enrollment records
num_records = 600
data = []

start_date = pd.to_datetime("2024-01-01")
end_date = pd.to_datetime("2024-06-30")
date_range_days = (end_date - start_date).days

# Course popularity distribution (some courses get more enrollments)
course_weights = [0.18, 0.12, 0.16, 0.11, 0.14, 0.10, 0.10, 0.09]

chosen_courses = np.random.choice(courses_info, size=num_records, p=course_weights)

for i in range(num_records):
    c_info = chosen_courses[i]
    total_mod = c_info["modules"]
    tendency = c_info["completion_tendency"]
    
    # Decide if student completes the course
    is_completed = np.random.rand() < tendency
    if is_completed:
        completed_mod = total_mod
        status = "Completed"
    else:
        # Student dropped off before finishing (between 0 and total_mod - 1)
        # Beta distribution skewed towards either early drop or almost done
        drop_fraction = np.random.beta(a=1.5, b=1.8)
        completed_mod = int(drop_fraction * total_mod)
        if completed_mod >= total_mod:
            completed_mod = total_mod - 1
        status = "Incomplete"
        
    comp_pct = round((completed_mod / total_mod) * 100, 2)
    enroll_days = np.random.randint(0, date_range_days)
    enroll_date = (start_date + pd.Timedelta(days=enroll_days)).strftime("%Y-%m-%d")
    
    first_name = random.choice(student_first_names)
    last_name = random.choice(student_last_names)
    
    data.append({
        "Student ID": f"STU{1001 + i}",
        "Student Name": f"{first_name} {last_name}",
        "Course Name": c_info["name"],
        "Course Category": c_info["category"],
        "Enrollment Date": enroll_date,
        "Total Modules": total_mod,
        "Completed Modules": completed_mod,
        "Completion Status": status,
        "Completion Percentage": comp_pct
    })

raw_df = pd.DataFrame(data)

# Introduce a few realistic imperfections for the data cleaning tutorial
# Add 5 duplicate rows
duplicates = raw_df.sample(n=5, random_state=42)
raw_df = pd.concat([raw_df, duplicates], ignore_index=True)

# Add 6 missing values in Completed Modules & Completion Percentage
raw_df.loc[12, "Completed Modules"] = np.nan
raw_df.loc[12, "Completion Percentage"] = np.nan
raw_df.loc[45, "Completed Modules"] = np.nan
raw_df.loc[45, "Completion Percentage"] = np.nan
raw_df.loc[88, "Completion Status"] = np.nan

# Save raw dataset
raw_df.to_csv("online_course_data.csv", index=False)
print("Raw dataset created: online_course_data.csv, total rows:", len(raw_df))

# ----------------------------------------------------------------------
# 2. DATA CLEANING & PREPROCESSING
# ----------------------------------------------------------------------
df = raw_df.copy()

# A. Checking duplicates
initial_count = len(df)
df = df.drop_duplicates()
cleaned_count = len(df)
print(f"Duplicates removed: {initial_count - cleaned_count}")

# B. Handling Missing Values
print("\nMissing values before cleaning:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# For rows where Completed Modules is NaN, impute with 0 or calculate from status
for idx in df[df["Completed Modules"].isnull()].index:
    # default to 0 completed modules if missing
    df.loc[idx, "Completed Modules"] = 0
    df.loc[idx, "Completion Percentage"] = 0.0
    df.loc[idx, "Completion Status"] = "Incomplete"

# For rows where Completion Status is NaN, derive from Completed Modules vs Total Modules
for idx in df[df["Completion Status"].isnull()].index:
    if df.loc[idx, "Completed Modules"] == df.loc[idx, "Total Modules"]:
        df.loc[idx, "Completion Status"] = "Completed"
    else:
        df.loc[idx, "Completion Status"] = "Incomplete"

# Ensure data types
df["Completed Modules"] = df["Completed Modules"].astype(int)
df["Enrollment Date"] = pd.to_datetime(df["Enrollment Date"])
df["Completion Percentage"] = ((df["Completed Modules"] / df["Total Modules"]) * 100).round(2)

# Save cleaned dataset
df.to_csv("cleaned_online_course_data.csv", index=False)
print("\nCleaned dataset saved. Remaining null values:")
print(df.isnull().sum().sum())

# ----------------------------------------------------------------------
# 3. STATISTICAL & AGGREGATE CALCULATIONS
# ----------------------------------------------------------------------
total_enrollments = len(df)
total_completed = (df["Completion Status"] == "Completed").sum()
total_incomplete = (df["Completion Status"] == "Incomplete").sum()
overall_completion_rate = round((total_completed / total_enrollments) * 100, 2)
avg_completion_pct = round(df["Completion Percentage"].mean(), 2)

print(f"\n--- OVERALL METRICS ---")
print(f"Total Enrollments: {total_enrollments}")
print(f"Total Completed: {total_completed}")
print(f"Total Incomplete: {total_incomplete}")
print(f"Overall Completion Rate: {overall_completion_rate}%")
print(f"Average Student Completion Percentage: {avg_completion_pct}%")

# Course-wise Performance
course_summary = df.groupby(["Course Name", "Course Category"]).agg(
    Total_Enrollments=("Student ID", "count"),
    Total_Modules=("Total Modules", "first"),
    Avg_Completed_Modules=("Completed Modules", "mean"),
    Completed_Count=("Completion Status", lambda x: (x == "Completed").sum()),
    Incomplete_Count=("Completion Status", lambda x: (x == "Incomplete").sum()),
    Avg_Completion_Pct=("Completion Percentage", "mean")
).reset_index()

course_summary["Course_Completion_Rate_%"] = (
    (course_summary["Completed_Count"] / course_summary["Total_Enrollments"]) * 100
).round(2)
course_summary["Avg_Completed_Modules"] = course_summary["Avg_Completed_Modules"].round(2)
course_summary["Avg_Completion_Pct"] = course_summary["Avg_Completion_Pct"].round(2)

# Sort by completion rate descending
course_summary = course_summary.sort_values(by="Course_Completion_Rate_%", ascending=False)
course_summary.to_csv("course_summary_report.csv", index=False)

print("\n--- COURSE PERFORMANCE SUMMARY ---")
print(course_summary.to_string(index=False))

# Category-wise Performance
cat_summary = df.groupby("Course Category").agg(
    Total_Enrollments=("Student ID", "count"),
    Completed_Count=("Completion Status", lambda x: (x == "Completed").sum()),
    Incomplete_Count=("Completion Status", lambda x: (x == "Incomplete").sum()),
    Avg_Completion_Pct=("Completion Percentage", "mean")
).reset_index()

cat_summary["Category_Completion_Rate_%"] = (
    (cat_summary["Completed_Count"] / cat_summary["Total_Enrollments"]) * 100
).round(2)
cat_summary["Avg_Completion_Pct"] = cat_summary["Avg_Completion_Pct"].round(2)
cat_summary = cat_summary.sort_values(by="Category_Completion_Rate_%", ascending=False)

print("\n--- CATEGORY PERFORMANCE SUMMARY ---")
print(cat_summary.to_string(index=False))

# Highest and Lowest
highest_course = course_summary.iloc[0]
lowest_course = course_summary.iloc[-1]
print(f"\nHighest Completion Rate: {highest_course['Course Name']} ({highest_course['Course_Completion_Rate_%']}%)")
print(f"Lowest Completion Rate: {lowest_course['Course Name']} ({lowest_course['Course_Completion_Rate_%']}%)")

# ----------------------------------------------------------------------
# 4. VISUALIZATIONS GENERATION
# ----------------------------------------------------------------------
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"font.size": 11, "font.family": "sans-serif"})

# Chart 1: Student Enrollment by Course (Bar Chart)
plt.figure(figsize=(10, 6))
order = df["Course Name"].value_counts().index
ax1 = sns.countplot(data=df, y="Course Name", order=order, hue="Course Name", palette="viridis", legend=False)
plt.title("Total Student Enrollment by Course", fontsize=15, pad=15, fontweight="bold")
plt.xlabel("Number of Enrolled Students", fontsize=12)
plt.ylabel("Course Name", fontsize=12)
for p in ax1.patches:
    width = p.get_width()
    if width > 0:
        ax1.annotate(f"{int(width)}", (width + 1.5, p.get_y() + p.get_height() / 2),
                     ha="left", va="center", fontsize=10, fontweight="bold")
plt.xlim(0, max(df["Course Name"].value_counts()) * 1.15)
plt.tight_layout()
plt.savefig("images/01_enrollment_by_course.png", dpi=300)
plt.close()

# Chart 2: Course-wise Completion Rate (Bar Chart)
plt.figure(figsize=(11, 6))
sorted_courses = course_summary.sort_values(by="Course_Completion_Rate_%", ascending=True)
colors = ["#e74c3c" if x < 50 else "#f39c12" if x < 65 else "#27ae60" for x in sorted_courses["Course_Completion_Rate_%"]]
bars = plt.barh(sorted_courses["Course Name"], sorted_courses["Course_Completion_Rate_%"], color=colors, edgecolor="black", height=0.6)
plt.title("Course-wise Completion Rates (%)", fontsize=15, pad=15, fontweight="bold")
plt.xlabel("Completion Rate (%)", fontsize=12)
plt.ylabel("Course Name", fontsize=12)
plt.axvline(x=overall_completion_rate, color="blue", linestyle="--", linewidth=1.5, label=f"Average Completion Rate ({overall_completion_rate}%)")
for bar in bars:
    w = bar.get_width()
    plt.text(w + 1.2, bar.get_y() + bar.get_height() / 2, f"{w:.1f}%", ha="left", va="center", fontsize=10, fontweight="bold")
plt.xlim(0, 100)
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("images/02_course_completion_rates.png", dpi=300)
plt.close()

# Chart 3: Pie Chart of Overall Completion Status
plt.figure(figsize=(7, 7))
status_counts = df["Completion Status"].value_counts()
colors = ["#2ecc71", "#e74c3c"]
explode = (0.05, 0)
plt.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=140,
        colors=colors, explode=explode, shadow=True, textprops={"fontsize": 13, "fontweight": "bold"},
        wedgeprops={"edgecolor": "white", "linewidth": 2})
plt.title("Overall Course Completion Status Distribution", fontsize=15, pad=20, fontweight="bold")
plt.tight_layout()
plt.savefig("images/03_completion_status_pie.png", dpi=300)
plt.close()

# Chart 4: Bar Chart Comparing Completion Rates by Category
plt.figure(figsize=(9, 5))
ax4 = sns.barplot(data=cat_summary, x="Course Category", y="Category_Completion_Rate_%",
                  hue="Course Category", palette="magma", legend=False, edgecolor="black")
plt.title("Course Completion Rate by Category (%)", fontsize=15, pad=15, fontweight="bold")
plt.xlabel("Course Category", fontsize=12)
plt.ylabel("Completion Rate (%)", fontsize=12)
plt.ylim(0, 100)
for p in ax4.patches:
    h = p.get_height()
    ax4.annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2, h + 2),
                 ha="center", va="bottom", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig("images/04_category_completion_rates.png", dpi=300)
plt.close()

# Chart 5: Heatmap showing Course Performance Metrics
plt.figure(figsize=(10, 6))
heatmap_data = course_summary.set_index("Course Name")[
    ["Total_Enrollments", "Total_Modules", "Avg_Completed_Modules", "Avg_Completion_Pct", "Course_Completion_Rate_%"]
].rename(columns={
    "Total_Enrollments": "Enrollments",
    "Total_Modules": "Total Modules",
    "Avg_Completed_Modules": "Avg Done Modules",
    "Avg_Completion_Pct": "Avg Student %",
    "Course_Completion_Rate_%": "Completion Rate %"
})
# Normalize for color display while showing actual annotated values
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", cbar=True, linewidths=1, linecolor="gray")
plt.title("Course Performance Heatmap (Key Metrics Comparison)", fontsize=15, pad=15, fontweight="bold")
plt.xlabel("Metrics", fontsize=12)
plt.ylabel("Course Name", fontsize=12)
plt.tight_layout()
plt.savefig("images/05_course_performance_heatmap.png", dpi=300)
plt.close()

# Chart 6: Boxplot of Completed Modules by Category
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="Course Category", y="Completed Modules", hue="Course Category", palette="Set2", legend=False)
plt.title("Distribution of Modules Completed by Category", fontsize=15, pad=15, fontweight="bold")
plt.xlabel("Course Category", fontsize=12)
plt.ylabel("Number of Modules Completed", fontsize=12)
plt.tight_layout()
plt.savefig("images/06_modules_completed_distribution.png", dpi=300)
plt.close()

print("\nAll 6 visualization charts generated and saved in images/ successfully!")
