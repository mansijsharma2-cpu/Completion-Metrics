"""
========================================================================================
Project Title   : Online Course Completion Analysis
Domain          : Data Science / Educational Analytics / E-Learning
Author          : Data Science Student
Libraries       : Python 3, Pandas, NumPy, Matplotlib, Seaborn
========================================================================================
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure visual styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"font.size": 11, "font.family": "sans-serif"})

# Create output folder for charts
os.makedirs("images", exist_ok=True)


def load_and_inspect_data(file_path: str) -> pd.DataFrame:
    """Loads the dataset and prints basic schema inspection."""
    print("=" * 80)
    print("STEP 1: LOADING & INSPECTING DATASET")
    print("=" * 80)
    df = pd.read_csv(file_path)
    print(f"Dataset successfully loaded. Total rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print("\nDataset Sample (First 5 Rows):")
    print(df.head())
    print("\nDataset Info:")
    df.info()
    return df


def clean_and_preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans duplicate rows, imputes missing values, and ensures valid data types."""
    print("\n" + "=" * 80)
    print("STEP 2: DATA CLEANING & PREPROCESSING")
    print("=" * 80)

    # 1. Check & remove duplicates
    duplicates_count = df.duplicated().sum()
    print(f"Duplicate rows detected: {duplicates_count}")
    df_clean = df.drop_duplicates().copy()
    print(f"Rows remaining after deduplication: {len(df_clean)}")

    # 2. Check missing values
    print("\nMissing values before cleaning:")
    print(df_clean.isnull().sum())

    # 3. Handle missing values
    # Impute missing Completed Modules with 0
    df_clean["Completed Modules"] = df_clean["Completed Modules"].fillna(0).astype(int)

    # Recalculate Completion Percentage accurately
    df_clean["Completion Percentage"] = (
        (df_clean["Completed Modules"] / df_clean["Total Modules"]) * 100
    ).round(2)

    # Determine Completion Status consistently
    df_clean["Completion Status"] = np.where(
        df_clean["Completed Modules"] == df_clean["Total Modules"],
        "Completed",
        "Incomplete"
    )

    # Convert Enrollment Date to proper datetime
    df_clean["Enrollment Date"] = pd.to_datetime(df_clean["Enrollment Date"])

    print("\nMissing values after cleaning:")
    print(df_clean.isnull().sum())

    df_clean.to_csv("cleaned_online_course_data.csv", index=False)
    print("Cleaned dataset saved as 'cleaned_online_course_data.csv'.")
    return df_clean


def perform_statistical_analysis(df: pd.DataFrame):
    """Calculates overall metrics, course-wise performance, and category-wise performance."""
    print("\n" + "=" * 80)
    print("STEP 3: STATISTICAL & AGGREGATE ANALYSIS")
    print("=" * 80)

    # Global platform metrics
    total_enrolled = len(df)
    total_completed = (df["Completion Status"] == "Completed").sum()
    total_incomplete = (df["Completion Status"] == "Incomplete").sum()
    overall_completion_rate = round((total_completed / total_enrolled) * 100, 2)
    avg_progress = round(df["Completion Percentage"].mean(), 2)

    print("--- GLOBAL PLATFORM METRICS ---")
    print(f"Total Student Enrollments            : {total_enrolled}")
    print(f"Total Completed Courses              : {total_completed} ({overall_completion_rate}%)")
    print(f"Total Incomplete Courses             : {total_incomplete} ({round(100 - overall_completion_rate, 2)}%)")
    print(f"Average Student Completion Progress  : {avg_progress}%\n")

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
    course_summary = course_summary.sort_values(by="Course_Completion_Rate_%", ascending=False)

    print("--- COURSE-WISE PERFORMANCE TABLE ---")
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

    print("\n--- CATEGORY-WISE PERFORMANCE TABLE ---")
    print(cat_summary.to_string(index=False))

    # Highest & Lowest Performing Courses
    top_course = course_summary.iloc[0]
    bottom_course = course_summary.iloc[-1]
    print("\n--- KEY COURSE HIGHLIGHTS ---")
    print(f"Highest Completion Rate: {top_course['Course Name']} ({top_course['Course_Completion_Rate_%']}%)")
    print(f"Lowest Completion Rate : {bottom_course['Course Name']} ({bottom_course['Course_Completion_Rate_%']}%)")

    course_summary.to_csv("course_summary_report.csv", index=False)
    return course_summary, cat_summary, overall_completion_rate


def generate_visualizations(df: pd.DataFrame, course_summary: pd.DataFrame, cat_summary: pd.DataFrame, overall_rate: float):
    """Generates all required visualizations and saves high-resolution PNGs."""
    print("\n" + "=" * 80)
    print("STEP 4: GENERATING PROFESSIONAL VISUALIZATIONS")
    print("=" * 80)

    # Chart 1: Student Enrollment by Course
    plt.figure(figsize=(10, 6))
    order = df["Course Name"].value_counts().index
    ax1 = sns.countplot(data=df, y="Course Name", order=order, hue="Course Name", palette="viridis", legend=False)
    plt.title("Total Student Enrollment by Course", fontsize=15, pad=15, fontweight="bold")
    plt.xlabel("Number of Enrolled Students", fontsize=12)
    plt.ylabel("Course Name", fontsize=12)
    for p in ax1.patches:
        w = p.get_width()
        if w > 0:
            ax1.annotate(f"{int(w)}", (w + 1.5, p.get_y() + p.get_height() / 2),
                         ha="left", va="center", fontsize=10, fontweight="bold")
    plt.xlim(0, max(df["Course Name"].value_counts()) * 1.15)
    plt.tight_layout()
    plt.savefig("images/01_enrollment_by_course.png", dpi=300)
    plt.close()
    print("Saved: images/01_enrollment_by_course.png")

    # Chart 2: Course-wise Completion Rates (%)
    plt.figure(figsize=(11, 6))
    sorted_courses = course_summary.sort_values(by="Course_Completion_Rate_%", ascending=True)
    colors = ["#e74c3c" if x < 50 else "#f39c12" if x < 65 else "#27ae60" for x in sorted_courses["Course_Completion_Rate_%"]]
    bars = plt.barh(sorted_courses["Course Name"], sorted_courses["Course_Completion_Rate_%"], color=colors, edgecolor="black", height=0.6)
    plt.axvline(x=overall_rate, color="blue", linestyle="--", linewidth=1.5, label=f"Platform Avg ({overall_rate}%)")
    plt.title("Course-wise Completion Rates (%)", fontsize=15, pad=15, fontweight="bold")
    plt.xlabel("Completion Rate (%)", fontsize=12)
    plt.ylabel("Course Name", fontsize=12)
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 1.2, bar.get_y() + bar.get_height() / 2, f"{w:.1f}%", ha="left", va="center", fontsize=10, fontweight="bold")
    plt.xlim(0, 100)
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig("images/02_course_completion_rates.png", dpi=300)
    plt.close()
    print("Saved: images/02_course_completion_rates.png")

    # Chart 3: Pie Chart of Overall Completion Status
    plt.figure(figsize=(7, 7))
    status_counts = df["Completion Status"].value_counts()
    plt.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=140,
            colors=["#2ecc71", "#e74c3c"], explode=(0.05, 0), shadow=True,
            textprops={"fontsize": 13, "fontweight": "bold"},
            wedgeprops={"edgecolor": "white", "linewidth": 2})
    plt.title("Overall Course Completion Status Distribution", fontsize=15, pad=20, fontweight="bold")
    plt.tight_layout()
    plt.savefig("images/03_completion_status_pie.png", dpi=300)
    plt.close()
    print("Saved: images/03_completion_status_pie.png")

    # Chart 4: Category-Wise Completion Rates Bar Chart
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
    print("Saved: images/04_category_completion_rates.png")

    # Chart 5: Course Performance Heatmap
    plt.figure(figsize=(10, 6))
    hm_data = course_summary.set_index("Course Name")[
        ["Total_Enrollments", "Total_Modules", "Avg_Completed_Modules", "Avg_Completion_Pct", "Course_Completion_Rate_%"]
    ].rename(columns={
        "Total_Enrollments": "Enrollments",
        "Total_Modules": "Total Modules",
        "Avg_Completed_Modules": "Avg Done Modules",
        "Avg_Completion_Pct": "Avg Student %",
        "Course_Completion_Rate_%": "Completion Rate %"
    })
    sns.heatmap(hm_data, annot=True, fmt=".1f", cmap="YlGnBu", cbar=True, linewidths=1, linecolor="gray")
    plt.title("Course Performance Heatmap (Key Metrics Comparison)", fontsize=15, pad=15, fontweight="bold")
    plt.xlabel("Metrics", fontsize=12)
    plt.ylabel("Course Name", fontsize=12)
    plt.tight_layout()
    plt.savefig("images/05_course_performance_heatmap.png", dpi=300)
    plt.close()
    print("Saved: images/05_course_performance_heatmap.png")

    # Chart 6: Boxplot of Completed Modules by Category
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="Course Category", y="Completed Modules", hue="Course Category", palette="Set2", legend=False)
    plt.title("Distribution of Modules Completed by Category", fontsize=15, pad=15, fontweight="bold")
    plt.xlabel("Course Category", fontsize=12)
    plt.ylabel("Number of Modules Completed", fontsize=12)
    plt.tight_layout()
    plt.savefig("images/06_modules_completed_distribution.png", dpi=300)
    plt.close()
    print("Saved: images/06_modules_completed_distribution.png")

    print("\nAll visualizations created successfully in the 'images/' folder!")


def main():
    dataset_file = "online_course_data.csv"
    if not os.path.exists(dataset_file):
        print(f"Error: Dataset {dataset_file} not found.")
        return

    df = load_and_inspect_data(dataset_file)
    df_clean = clean_and_preprocess(df)
    course_summary, cat_summary, overall_rate = perform_statistical_analysis(df_clean)
    generate_visualizations(df_clean, course_summary, cat_summary, overall_rate)
    print("\nAnalysis pipeline executed completely and successfully.")


if __name__ == "__main__":
    main()
