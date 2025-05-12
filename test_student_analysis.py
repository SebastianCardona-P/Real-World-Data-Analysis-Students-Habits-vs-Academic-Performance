import unittest
import pandas as pd
import numpy as np
import os
from student_analysis import load_data, clean_data, test_normality, calculate_correlation, plot_pie_chart, plot_histogram, plot_scatter, plot_boxplot, analyze_and_visualize

class TestStudentAnalysis(unittest.TestCase):
    def setUp(self):
        """Set up a sample dataset for testing."""
        self.test_data = pd.DataFrame({
            'student_id': ['S1', 'S2', 'S3'],
            'age': [20, 21, -1],
            'gender': ['Male', 'Female', 'Other'],
            'study_hours_per_day': [5.0, 3.0, 25.0],
            'social_media_hours': [2.0, 1.0, 0.0],
            'netflix_hours': [1.0, 2.0, 0.0],
            'part_time_job': ['Yes', 'No', 'No'],
            'attendance_percentage': [90.0, 85.0, 100.0],
            'sleep_hours': [7.0, 8.0, 6.0],
            'diet_quality': ['Good', 'Fair', 'Poor'],
            'exercise_frequency': [3, 2, 1],
            'parental_education_level': ['Bachelor', 'Master', 'High School'],
            'internet_quality': ['Good', 'Average', 'Poor'],
            'mental_health_rating': [8, 7, 9],
            'extracurricular_participation': ['Yes', 'No', 'Yes'],
            'exam_score': [85.0, 90.0, 95.0]
        })
        self.test_file = 'test_data.csv'
        self.test_data.to_csv(self.test_file, index=False)
        self.output_dir = 'test_plots'
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        """Clean up test files and directories."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                os.remove(os.path.join(self.output_dir, file))
            os.rmdir(self.output_dir)

    def test_load_data(self):
        """Test loading CSV data."""
        df = load_data(self.test_file)
        self.assertEqual(len(df), 3)
        self.assertEqual(list(df.columns), list(self.test_data.columns))

    def test_load_data_file_not_found(self):
        """Test loading non-existent file."""
        with self.assertRaises(FileNotFoundError):
            load_data('non_existent.csv')

    def test_clean_data(self):
        """Test data cleaning function."""
        cleaned_df = clean_data(self.test_data)
        self.assertEqual(len(cleaned_df), 2)
        self.assertTrue((cleaned_df['study_hours_per_day'] <= 24).all())
        self.assertTrue((cleaned_df['age'] >= 0).all())

    def test_test_normality(self):
        """Test normality test function."""
        data = self.test_data['exam_score']
        stat, p_value = test_normality(data)
        self.assertIsInstance(stat, float)
        self.assertIsInstance(p_value, float)

    def test_calculate_correlation(self):
        """Test correlation calculation."""
        x = self.test_data['study_hours_per_day']
        y = self.test_data['exam_score']
        corr = calculate_correlation(x, y)
        self.assertIsInstance(corr, float)
        self.assertTrue(-1 <= corr <= 1)

    def test_plot_pie_chart(self):
        """Test pie chart generation."""
        filename = f"{self.output_dir}/gender_pie.png"
        plot_pie_chart(self.test_data['gender'], 'Gender Distribution', filename)
        self.assertTrue(os.path.exists(filename))

    def test_plot_histogram(self):
        """Test histogram generation."""
        filename = f"{self.output_dir}/age_hist.png"
        plot_histogram(self.test_data['age'], 'Age Distribution', filename)
        self.assertTrue(os.path.exists(filename))

    def test_plot_scatter(self):
        """Test scatter plot generation."""
        filename = f"{self.output_dir}/study_vs_exam_scatter.png"
        plot_scatter(self.test_data['study_hours_per_day'], self.test_data['exam_score'], 'Study vs Exam', filename)
        self.assertTrue(os.path.exists(filename))

    def test_plot_boxplot(self):
        """Test box plot generation."""
        filename = f"{self.output_dir}/part_time_job_vs_exam_score_box.png"
        plot_boxplot(self.test_data, 'part_time_job', 'exam_score', 'Part-Time Job vs Exam Score', filename)
        self.assertTrue(os.path.exists(filename))

    def test_analyze_and_visualize(self):
        """Test main analysis function."""
        results = analyze_and_visualize(self.test_file, self.output_dir)
        self.assertIn('normality_tests', results)
        self.assertIn('correlations', results)
        self.assertIn('summary_stats', results)
        self.assertTrue(os.path.exists(f"{self.output_dir}/gender_pie.png"))
        self.assertTrue(os.path.exists(f"{self.output_dir}/age_hist.png"))
        self.assertTrue(os.path.exists(f"{self.output_dir}/study_hours_per_day_vs_exam_score_scatter.png"))
        # Check new box plots
        self.assertTrue(os.path.exists(f"{self.output_dir}/part_time_job_vs_study_hours_box.png"))
        self.assertTrue(os.path.exists(f"{self.output_dir}/part_time_job_vs_exam_score_box.png"))
        self.assertTrue(os.path.exists(f"{self.output_dir}/parental_education_vs_exam_score_box.png"))
        self.assertTrue(os.path.exists(f"{self.output_dir}/internet_quality_vs_exam_score_box.png"))
        self.assertTrue(os.path.exists(f"{self.output_dir}/extracurricular_vs_mental_health_box.png"))
        self.assertTrue(os.path.exists(f"{self.output_dir}/extracurricular_vs_study_hours_box.png"))

if __name__ == '__main__':
    unittest.main()