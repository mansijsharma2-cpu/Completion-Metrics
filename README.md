# Online Course Completion Analysis

**Subject:** Data Science Mini Project  
**Student Name:** Mansij Sharma  
**Roll No:** 124712  
**Batch:** 2026  
**Section:** B2  

---

## 📌 1. Project Overview & Context

Online education platforms (Coursera, edX, Udemy, etc.) experience wide variations in student engagement and course completion. While millions of learners register for courses annually, typical completion rates in open online courses can drop as low as 10%–40%, while concise, focused courses can maintain completion rates upwards of 75%.

### 🎯 Problem Statement
> *"Online learning platforms need to understand which courses have higher completion rates."*

### 📋 Objectives & Methodology
1. **Analyze Enrollment & Completion Status:** Process student enrollment records to monitor completed modules, active learners, and drop-off points.
2. **Calculate Completion Percentages:** Determine exact completion rates aggregated by individual course, broad subject category, and difficulty level.
3. **Identify High vs. Low Completion Outliers:** Pinpoint which courses achieve superior learner retention versus those that suffer severe dropout.
4. **Identify Retention Drivers:** Measure how course length (number of modules), study hours, and quiz performance influence completion.
5. **Generate an Actionable Deliverable:** Produce an executive analytics report and an interactive visualization dashboard for academic presentation and platform decision-making.

---

## 📊 2. Key Findings & Insights

From our analysis of **2,000 student enrollments** across **10 distinct courses** spanning **7 domains**:

### 🏆 Top 3 Highest Completion Courses
| Rank | Course ID | Course Name | Category | Level | Modules | Completion Rate |
| :---: | :---: | :--- | :--- | :--- | :---: | :---: |
| **#1** | `WEB101` | **Modern HTML, CSS & Responsive Design** | Web Development | Beginner | 7 | **77.4%** |
| **#2** | `BIZ101` | **Product Management Essentials** | Business | Beginner | 6 | **76.7%** |
| **#3** | `CS101` | **Python for Beginners** | Computer Science | Beginner | 8 | **75.5%** |

### ⚠️ Bottom 3 Lowest Completion Courses
| Rank | Course ID | Course Name | Category | Level | Modules | Completion Rate |
| :---: | :---: | :--- | :--- | :--- | :---: | :---: |
| **#8** | `CS202` | **Data Structures & Algorithms** | Computer Science | Intermediate | 16 | **46.0%** |
| **#9** | `AI301` | **Deep Learning & Neural Networks** | Artificial Intelligence | Advanced | 18 | **34.3%** |
| **#10** | `WEB202` | **Full-Stack Web Development Bootcamp** | Web Development | Advanced | 22 | **33.7%** |

### 🔍 Root Cause Takeaways
- **Curriculum Length Penalty ($r = -0.985$):** Course length is the strongest predictor of completion. Compact courses (6–9 modules) average **75.4%** completion, while lengthy bootcamps (16–22 modules) drop to **38.0%**.
- **Difficulty Tier Step-Down:** Beginner courses finish at **76.5%**, Intermediate at **57.7%**, and Advanced courses finish at only **34.0%**.
- **Early Churn Gate:** Over 80% of dropouts occur within the first 2 modules, demonstrating that the initial onboarding experience determines learner retention.

---

## 📂 3. Project Directory Structure

```text
online_course_completion_analysis/
├── data/
│   ├── course_enrollments.csv      # Primary dataset (2,000 records)
│   ├── course_summary.csv          # Course-level metrics & rankings
│   ├── category_summary.csv        # Category-level benchmarks
│   └── level_summary.csv           # Difficulty level performance
├── src/
│   ├── generate_dataset.py         # Reproducible synthetic data generator
│   ├── analysis.py                 # Core analysis & charting pipeline
│   ├── generate_report.py          # HTML & Markdown report builder
│   └── build_notebook.py           # Jupyter Notebook generator
├── notebooks/
│   └── online_course_completion_analysis.ipynb # Interactive analysis notebook
├── reports/
│   ├── analytics_report.html       # Standalone interactive HTML report
│   ├── analytics_report.md         # Formatted executive markdown report
│   └── figures/                    # High-res charts (300 DPI)
│       ├── 01_course_completion_rates.png
│       ├── 02_category_completion_rates.png
│       ├── 03_completion_status_distribution.png
│       ├── 04_completion_by_level.png
│       ├── 05_course_length_vs_completion.png
│       └── 06_correlation_heatmap.png
├── dashboard/
│   └── index.html                  # Responsive modern web dashboard with Chart.js
├── requirements.txt                # Python library dependencies
└── README.md                       # Complete project documentation
```

---

## 🚀 4. How to Run the Project

### Prerequisites
- Python 3.10+ (tested with Python 3.14)
- Web browser (Chrome, Edge, Firefox, or Safari)

### 1. Install Dependencies
```bash
py -m pip install -r requirements.txt
```

### 2. Generate Dataset & Run Analysis Pipeline
```bash
# Generate synthetic dataset (if needed)
py src/generate_dataset.py

# Run full data pipeline & generate charts
py src/analysis.py

# Generate HTML & Markdown reports
py src/generate_report.py
```

### 3. Open the Interactive Web Dashboard
Simply double-click or open `dashboard/index.html` in any web browser.  
No web server setup is required! You can filter courses by category or level, view dynamic charts, and search the course ranking table.

### 4. View the Interactive Analytics Report
Open `reports/analytics_report.html` in your browser to view the complete formatted executive report with embedded figures and tables.

### 5. Run the Jupyter Notebook
Open the notebook in VS Code, JupyterLab, or Jupyter Notebook:
```bash
jupyter notebook notebooks/online_course_completion_analysis.ipynb
```

---

## 💡 5. Strategic Recommendations for Educational Platforms

1. **Decompose Long Bootcamps into Micro-Credentials:**  
   Split 20+ module courses into a sequence of 3-to-4 smaller, bite-sized courses awarding milestone badges.
2. **Automated Early Nudges (First 14 Days):**  
   Implement targeted nudges and peer mentor connections for learners struggling in modules 1–3 to prevent early churn.
3. **Formative Practice Quizzes:**  
   Provide retryable quizzes with instant explanations before graded barriers to maintain learner confidence and motivation.

---
Check Out My Website :   ( https://e3ba0c549d4c45.app.lhr.life/ )
 Mansij Sharma's Data Science Mini Project (Roll No: 124712, Batch: 2026, Section: B2).*
