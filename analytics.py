import os
import time
import platform
import subprocess

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.switch_backend("Agg")
sns.set_theme(style="whitegrid", context="notebook")

DATA_FILE = "dataset.csv"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_FILE)

if df.empty:
    raise ValueError("Dataset is empty.")

# Clean column names
df.columns = [col.strip() for col in df.columns]

# Check required columns
required_cols = ["GPA", "Gender", "GradeClass", "StudyTimeWeekly"]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

# Gender labels
df["Gender"] = df["Gender"].replace({
    0: "Male", 1: "Female",
    "0": "Male", "1": "Female"
})

# Fill missing values
df["GPA"] = df["GPA"].fillna(df["GPA"].median())
df["StudyTimeWeekly"] = df["StudyTimeWeekly"].fillna(df["StudyTimeWeekly"].median())

for col in ["Gender", "GradeClass"]:
    df[col] = df[col].fillna("Unknown")

saved_files = []

def save_plot(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    saved_files.append(path)

# =========================
# 1. Histogram of GPA
# =========================
plt.figure(figsize=(8, 5))
sns.histplot(df["GPA"], bins=15, kde=True, edgecolor="black")
plt.title("Histogram of GPA", fontweight="bold")
plt.xlabel("GPA")
plt.ylabel("Frequency")
save_plot("01_histogram_gpa.png")

# =========================
# 2. Average GPA by Gender
# =========================
gender_gpa = df.groupby("Gender")["GPA"].mean().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
sns.barplot(x=gender_gpa.index, y=gender_gpa.values)
plt.title("Average GPA by Gender", fontweight="bold")
plt.xlabel("Gender")
plt.ylabel("Average GPA")
save_plot("02_avg_gpa_by_gender.png")

# =========================
# 3. GradeClass Distribution
# =========================
grade_counts = df["GradeClass"].value_counts().sort_index()

plt.figure(figsize=(7, 7))
plt.pie(
    grade_counts.values,
    labels=grade_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("GradeClass Distribution", fontweight="bold")
save_plot("03_gradeclass_distribution.png")

# =========================
# 4. Study Time by GradeClass
# =========================
studytime_by_grade = df.groupby("GradeClass")["StudyTimeWeekly"].mean().sort_index()

plt.figure(figsize=(8, 5))
sns.barplot(x=studytime_by_grade.index, y=studytime_by_grade.values)
plt.title("Average Study Time by GradeClass", fontweight="bold")
plt.xlabel("GradeClass")
plt.ylabel("Average Study Time Weekly")
save_plot("04_avg_studytime_by_gradeclass.png")

# =========================
# 5. FULL DASHBOARD (4-IN-1)
# =========================
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle("Student Performance Dashboard", fontsize=18, fontweight="bold")

# Histogram
sns.histplot(df["GPA"], bins=15, kde=True, ax=axes[0, 0], edgecolor="black")
axes[0, 0].set_title("Histogram of GPA")

# GPA by Gender
sns.barplot(x=gender_gpa.index, y=gender_gpa.values, ax=axes[0, 1])
axes[0, 1].set_title("Average GPA by Gender")

# Pie Chart
axes[1, 0].pie(
    grade_counts.values,
    labels=grade_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[1, 0].set_title("GradeClass Distribution")

# Study Time
sns.barplot(x=studytime_by_grade.index, y=studytime_by_grade.values, ax=axes[1, 1])
axes[1, 1].set_title("Average Study Time by GradeClass")

plt.tight_layout(rect=[0, 0, 1, 0.95])

dashboard_path = os.path.join(OUTPUT_DIR, "05_full_dashboard.png")
plt.savefig(dashboard_path, dpi=300, bbox_inches="tight")
plt.close()

saved_files.append(dashboard_path)

# =========================
# PRINT RESULTS
# =========================
print("\n🎉 ANALYSIS COMPLETE!")
print("📂 Generated files:")
for f in saved_files:
    print(f" - {f}")

# =========================
# AUTO OPEN (OPTIONAL)
# =========================
try:
    if os.environ.get("AUTO_OPEN_OUTPUTS", "0") == "1":
        path = os.path.abspath(OUTPUT_DIR)
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
except Exception as e:
    print(f"Auto-open failed: {e}")

# =========================
# WAIT BEFORE EXIT
# =========================
try:
    input("\nPress ENTER to exit...")
except:
    print("No input available. Closing in 10 seconds...")
    time.sleep(10)