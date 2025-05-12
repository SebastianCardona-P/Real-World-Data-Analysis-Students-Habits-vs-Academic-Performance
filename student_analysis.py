import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
import os

def load_data(file_path: str) -> pd.DataFrame:
    """Load and return the CSV dataset."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty.")

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset by handling missing values and invalid entries."""
    df = df.copy()
    df = df.dropna()
    numerical_cols = ['age', 'study_hours_per_day', 'social_media_hours', 'netflix_hours',
                     'attendance_percentage', 'sleep_hours', 'exercise_frequency', 'mental_health_rating', 'exam_score']
    for col in numerical_cols:
        df = df[df[col] >= 0]
    df['age'] = df['age'].clip(15, 30)
    df['study_hours_per_day'] = df['study_hours_per_day'].clip(0, 24)
    df['social_media_hours'] = df['social_media_hours'].clip(0, 24)
    df['netflix_hours'] = df['netflix_hours'].clip(0, 24)
    df['sleep_hours'] = df['sleep_hours'].clip(0, 24)
    df['attendance_percentage'] = df['attendance_percentage'].clip(0, 100)
    df['exam_score'] = df['exam_score'].clip(0, 100)
    return df

def plot_pie_chart(data: pd.Series, title: str, filename: str) -> None:
    """Generate and save a pie chart for a categorical variable."""
    counts = data.value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.savefig(filename)
    plt.close()

def plot_histogram(data: pd.Series, title: str, filename: str, bins: int = 30) -> None:
    """Generate and save a histogram with kernel density estimate."""
    plt.figure(figsize=(10, 6))
    sns.histplot(data, bins=bins, kde=True, stat='density')
    plt.title(title)
    plt.xlabel(data.name)
    plt.ylabel('Density')
    plt.savefig(filename)
    plt.close()

def plot_scatter(x: pd.Series, y: pd.Series, title: str, filename: str) -> None:
    """Generate and save a scatter plot for two variables."""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x, y=y)
    plt.title(title)
    plt.xlabel(x.name)
    plt.ylabel(y.name)
    plt.savefig(filename)
    plt.close()

def plot_boxplot(df: pd.DataFrame, x_col: str, y_col: str, title: str, filename: str) -> None:
    """Generate and save a box plot for comparing a numerical variable across categories."""
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=x_col, y=y_col, data=df)
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.savefig(filename)
    plt.close()

def test_normality(data: pd.Series) -> tuple:
    """Perform Shapiro-Wilk test for normality."""
    stat, p_value = stats.shapiro(data)
    return stat, p_value

def calculate_correlation(x: pd.Series, y: pd.Series) -> float:
    """Calculate Pearson correlation coefficient."""
    return stats.pearsonr(x, y)[0]

def analyze_and_visualize(file_path: str, output_dir: str = 'plots') -> dict:
    """Main function to analyze and visualize the dataset."""
    os.makedirs(output_dir, exist_ok=True)

    df = load_data(file_path)
    df = clean_data(df)

    results = {
        'normality_tests': {},
        'correlations': {},
        'summary_stats': {}
    }

    # Categorical variables for pie charts
    categorical_vars = {
        'gender': 'Gender Distribution',
        'part_time_job': 'Part-Time Job Distribution',
        'diet_quality': 'Diet Quality Distribution',
        'parental_education_level': 'Parental Education Level Distribution',
        'internet_quality': 'Internet Quality Distribution',
        'extracurricular_participation': 'Extracurricular Participation Distribution'
    }

    for col, title in categorical_vars.items():
        plot_pie_chart(df[col], title, f"{output_dir}/{col}_pie.png")

    # Numerical variables for histograms and normality tests
    numerical_vars = [
        'age', 'study_hours_per_day', 'social_media_hours', 'netflix_hours',
        'attendance_percentage', 'sleep_hours', 'exercise_frequency',
        'mental_health_rating', 'exam_score'
    ]

    for col in numerical_vars:
        plot_histogram(df[col], f'Distribution of {col}', f"{output_dir}/{col}_hist.png")
        stat, p_value = test_normality(df[col])
        results['normality_tests'][col] = {'stat': stat, 'p_value': p_value}
        results['summary_stats'][col] = df[col].describe().to_dict()

    # Relationships for scatter plots
    relationships = [
        ('sleep_hours', 'study_hours_per_day', 'Sleep vs Study Hours'),
        ('study_hours_per_day', 'exam_score', 'Study Hours vs Exam Score'),
        ('social_media_hours', 'exam_score', 'Social Media Hours vs Exam Score'),
        ('netflix_hours', 'exam_score', 'Netflix Hours vs Exam Score'),
        ('mental_health_rating', 'exam_score', 'Mental Health vs Exam Score')
    ]

    for x_col, y_col, title in relationships:
        plot_scatter(df[x_col], df[y_col], title, f"{output_dir}/{x_col}_vs_{y_col}_scatter.png")
        corr = calculate_correlation(df[x_col], df[y_col])
        results['correlations'][f"{x_col}_vs_{y_col}"] = corr

    # New visualizations for hypotheses
    # Part-time job vs. study hours and exam scores
    plot_boxplot(df, 'part_time_job', 'study_hours_per_day', 'Part-Time Job vs Study Hours', f"{output_dir}/part_time_job_vs_study_hours_box.png")
    plot_boxplot(df, 'part_time_job', 'exam_score', 'Part-Time Job vs Exam Score', f"{output_dir}/part_time_job_vs_exam_score_box.png")

    # Parental education vs. exam scores
    plot_boxplot(df, 'parental_education_level', 'exam_score', 'Parental Education vs Exam Score', f"{output_dir}/parental_education_vs_exam_score_box.png")

    # Internet quality vs. exam scores
    plot_boxplot(df, 'internet_quality', 'exam_score', 'Internet Quality vs Exam Score', f"{output_dir}/internet_quality_vs_exam_score_box.png")

    # Extracurricular participation vs. mental health and study hours
    plot_boxplot(df, 'extracurricular_participation', 'mental_health_rating', 'Extracurricular Participation vs Mental Health', f"{output_dir}/extracurricular_vs_mental_health_box.png")
    plot_boxplot(df, 'extracurricular_participation', 'study_hours_per_day', 'Extracurricular Participation vs Study Hours', f"{output_dir}/extracurricular_vs_study_hours_box.png")

    return results

if __name__ == '__main__':
    results = analyze_and_visualize('student_habits_performance.csv')
    print("Analysis Results:")
    print("Normality Tests:")
    for col, test in results['normality_tests'].items():
        print(f"{col}: Statistic={test['stat']:.4f}, p-value={test['p_value']:.4f}")
    print("\nCorrelations:")
    for rel, corr in results['correlations'].items():
        print(f"{rel}: Correlation={corr:.4f}")
    print("\nSummary Statistics:")
    for col, stats in results['summary_stats'].items():
        print(f"{col}: {stats}")