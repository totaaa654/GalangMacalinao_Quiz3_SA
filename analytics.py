import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.switch_backend("Agg")
sns.set_theme(style="whitegrid", context="notebook")

DATA_FILE = "dataset.csv"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

output_file = os.path.join(OUTPUT_DIR, "student_dashboard.png")


# Load dataset
df = pd.read_csv(DATA_FILE)

if df.empty:
    raise ValueError("Dataset is empty.")

# Clean column names
df.columns = [col.strip() for col in df.columns]

# Check required columns
required_cols = [
    "GPA",
    "Gender",
    "GradeClass",
    "StudyTimeWeekly"
]

missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

# Fill missing values safely
if df["GPA"].isna().any():
    df["GPA"] = df["GPA"].fillna(df["GPA"].median())

if df["StudyTimeWeekly"].isna().any():
    df["StudyTimeWeekly"] = df["StudyTimeWeekly"].fillna(df["StudyTimeWeekly"].median())

for col in ["Gender", "GradeClass"]:
    if df[col].isna().any():
        df[col] = df[col].fillna("Unknown")

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle("Student Performance Analysis Dashboard", fontsize=18, fontweight="bold")

# 1. Histogram of GPA
sns.histplot(
    df["GPA"],
    bins=15,
    kde=True,
    ax=axes[0, 0],
    color="#4C78A8",
    edgecolor="black",
    linewidth=0.5
)
axes[0, 0].set_title("Histogram of YUP IT WORKS", fontweight="bold")
axes[0, 0].set_xlabel("GPA")
axes[0, 0].set_ylabel("Frequency")

# 2. Bar Chart of Average GPA by Gender
gender_gpa = df.groupby("Gender", dropna=False)["GPA"].mean().sort_values(ascending=False)
sns.barplot(
    x=gender_gpa.index.astype(str),
    y=gender_gpa.values,
    ax=axes[0, 1],
    color="#72B7B2"
)
axes[0, 1].set_title("Average GPA by Gender", fontweight="bold")
axes[0, 1].set_xlabel("Gender")
axes[0, 1].set_ylabel("Average GPA")

# 3. Pie Chart of GradeClass Distribution
grade_counts = df["GradeClass"].value_counts().sort_index()
axes[1, 0].pie(
    grade_counts.values,
    labels=grade_counts.index.astype(str),
    autopct="%1.1f%%",
    startangle=90
)
axes[1, 0].set_title("GradeClass Distribution", fontweight="bold")

# 4. Bar Chart of Average Study Time by GradeClass
studytime_by_grade = df.groupby("GradeClass", dropna=False)["StudyTimeWeekly"].mean().sort_index()
sns.barplot(
    x=studytime_by_grade.index.astype(str),
    y=studytime_by_grade.values,
    ax=axes[1, 1],
    color="#A0CBE8"
)
axes[1, 1].set_title("Average Study Time by GradeClass", fontweight="bold")
axes[1, 1].set_xlabel("GradeClass")
axes[1, 1].set_ylabel("Average Study Time Weekly")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(output_file, dpi=300, bbox_inches="tight")
plt.close()

print(f"SAVED FILE: {output_file}")
print("DONE RUNNING ONCE ✅")