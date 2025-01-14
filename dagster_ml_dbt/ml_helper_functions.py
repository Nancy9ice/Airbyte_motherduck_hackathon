import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt
import numpy as np

def clean_and_preprocess_data(sat_data):
    # Drop irrelevant columns
    columns_to_drop = ['profile_image', 'registration_number', 'disciplinary_teacher']
    sat_data_cleaned = sat_data.drop(columns=columns_to_drop, errors='ignore')

    # Fill missing values
    sat_data_cleaned['sat_score'].fillna(0, inplace=True)
    sat_data_cleaned['sat_performance'].fillna('Unknown', inplace=True)

    # Calculate attendance rate
    sat_data_cleaned['attendance_rate'] = (
        sat_data_cleaned['average_student_minutes_attendance'] /
        sat_data_cleaned['average_expected_student_attendance']
    )

    # Encode categorical variables
    categorical_cols = [
        'student_class', 'student_status', 'health_condition', 'department', 'gender',
        'student_parent', 'parent_education', 'student_activity_status',
        'student_extracurricular_activity', 'student_school_performance',
        'student_offence', 'disciplinary_action_taken', 'sat_performance'
    ]
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        sat_data_cleaned[col] = le.fit_transform(sat_data_cleaned[col])
        label_encoders[col] = le

    # Create new features
    sat_data_cleaned['parent_education_effect'] = (
        sat_data_cleaned['parent_education'] * sat_data_cleaned['average_student_score']
    )
    sat_data_cleaned['activity_attendance_interaction'] = (
        sat_data_cleaned['student_activity_status'] * sat_data_cleaned['attendance_rate']
    )
    sat_data_cleaned['health_score_effect'] = (
        sat_data_cleaned['health_condition'] * sat_data_cleaned['average_student_score']
    )
    sat_data_cleaned['attendance_efficiency'] = (
        sat_data_cleaned['attendance_rate'] / sat_data_cleaned['average_expected_student_attendance']
    )
    sat_data_cleaned['discipline_score'] = (
        sat_data_cleaned['student_offence'] + sat_data_cleaned['disciplinary_action_taken']
    )

    return sat_data_cleaned, label_encoders

def train_rf_model(X_train, y_train):
    rf_model = RandomForestRegressor(random_state=42, n_estimators=300, max_depth=15)
    rf_model.fit(X_train, y_train)
    y_pred_train = rf_model.predict(X_train)
    train_rmse = sqrt(mean_squared_error(y_train, y_pred_train))
    train_r2 = r2_score(y_train, y_pred_train)
    return rf_model, train_rmse, train_r2

def generate_recommendations(test_data, predicted_scores, label_encoders):
    """
    Generate personalized recommendations based on predicted SAT scores and feature values.

    Args:
        test_data (pd.DataFrame): Test data with feature values.
        predicted_scores (array): Predicted SAT scores.
        label_encoders (dict): LabelEncoders used for encoding categorical variables.

    Returns:
        pd.DataFrame: DataFrame with recommendations for each student.
    """
    # Ensure test_data and predicted_scores have the same length
    if len(test_data) != len(predicted_scores):
        raise ValueError("Mismatch between test_data rows and predicted_scores size.")

    recommendations = []
    for index, row in test_data.iterrows():
        score = predicted_scores[index]
        rec = {
            "Student Name": row["student_name"],
            "Predicted SAT Score": score
        }

        # Determine outcome and base recommendation
        if score < 900:
            rec["Outcome"] = "Fail"
            rec["Recommendation"] = "Focus on improving attendance, health, and extracurricular participation."

            # Attendance suggestion
            if row["attendance_rate"] < 0.75:
                rec["Recommendation"] += " Ensure regular attendance to improve learning outcomes."

            # Health suggestion
            health_label_encoded = label_encoders["health_condition"].transform(["Very Good Condition"])[0]
            if row["health_condition"] < health_label_encoded:
                rec["Recommendation"] += " Work on improving health conditions through proper nutrition and rest."

            # Activity suggestion
            if row["student_activity_status"] == 0:  
                rec["Recommendation"] += " Participate in extracurricular activities to boost cognitive skills."
        else:
            rec["Outcome"] = "Pass"
            rec["Recommendation"] = "Maintain good attendance, focus on academics, and stay consistent."

            # Attendance suggestion
            if row["attendance_rate"] >= 0.9:
                rec["Recommendation"] += " Excellent attendance; keep it up!"

            # Activity suggestion
            if row["student_activity_status"] == 1:  
                rec["Recommendation"] += " Continue participating in extracurricular activities."

        recommendations.append(rec)

    # Convert the recommendations list to a DataFrame
    return pd.DataFrame(recommendations)

def write_predictions_to_db(conn, predictions_df, schema_name="exposure", table_name="sat_recommendations"):
    try:
        full_table_name = f"{schema_name}.{table_name}"
        conn.execute(f"DROP TABLE IF EXISTS {full_table_name};")
        conn.register("temp_table", predictions_df)
        conn.execute(f"CREATE TABLE {full_table_name} AS SELECT * FROM temp_table;")
        print(f"Data successfully written to {full_table_name}")
    except Exception as e:
        print(f"Error writing predictions to the database: {e}")