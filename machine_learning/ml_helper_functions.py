import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from dotenv import load_dotenv
import os
import duckdb

load_dotenv()

def get_connection():
    """
    Establishes a connection to the DuckDB database.
    """
    # Retrieve the MotherDuck token from the environment variables
    motherduck_token = os.getenv("MOTHERDUCK_TOKEN")
    
    if not motherduck_token:
        raise ValueError("MOTHERDUCK_TOKEN is not set in the environment variables.")
    
    # Construct the connection string with the token
    connection_string = f"md:Airbyte_Motherduck_Hackathon?motherduck_token={motherduck_token}"
    
    # Establish and return the connection
    conn = duckdb.connect(database=connection_string)
    return conn


def clean_and_preprocess_data(raw_data):
    """
    Cleans and preprocesses the SAT data.

    Args:
        raw_data (pd.DataFrame): Raw SAT data.

    Returns:
        pd.DataFrame: Cleaned and preprocessed data.
        dict: Label encoders for categorical columns.
    """
    # Drop irrelevant columns
    columns_to_drop = ['profile_image', 'registration_number', 'disciplinary_teacher']
    cleaned_data = raw_data.drop(columns=columns_to_drop, errors='ignore')

    # Fill missing values
    cleaned_data['sat_score'] = cleaned_data['sat_score'].fillna(0)
    cleaned_data['sat_performance'] = cleaned_data['sat_performance'].fillna('Unknown')

    # Calculate attendance rate
    cleaned_data['attendance_rate'] = (
        cleaned_data['average_student_minutes_attendance'] /
        cleaned_data['average_expected_student_attendance']
    )

    # Encode categorical variables
    categorical_cols = [
        'student_status', 'health_condition', 'department', 'gender',
        'student_parent', 'parent_education', 'student_activity_status',
        'student_extracurricular_activity', 'student_school_performance',
        'student_offence', 'disciplinary_action_taken', 'sat_performance'
    ]  # student_class removed
    label_encoders = {}
    for col in categorical_cols:
        if col in cleaned_data.columns:
            le = LabelEncoder()
            cleaned_data[col] = le.fit_transform(cleaned_data[col])
            label_encoders[col] = le

    
    # Encode student_class for filtering purposes
    if 'student_class' in cleaned_data.columns:
        le = LabelEncoder()
        cleaned_data['student_class_encoded'] = le.fit_transform(cleaned_data['student_class'])
        label_encoders['student_class'] = le


    return cleaned_data, label_encoders


def feature_engineering(cleaned_data):
    """
    Creates new features for the SAT data.

    Args:
        cleaned_data (pd.DataFrame): Preprocessed SAT data.

    Returns:
        pd.DataFrame: SAT data with additional features.
    """
    numeric_columns = [
        'parent_education', 'average_student_score', 'student_activity_status',
        'attendance_rate', 'health_condition'
    ]
    for col in numeric_columns:
        if col in cleaned_data.columns:
            cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')

    # Fill missing values with 0
    cleaned_data.fillna(0, inplace=True)

    # Create new features
    cleaned_data['parent_education_effect'] = (
        cleaned_data['parent_education'] * cleaned_data['average_student_score']
    )
    cleaned_data['activity_attendance_interaction'] = (
        cleaned_data['student_activity_status'] * cleaned_data['attendance_rate']
    )
    cleaned_data['health_score_effect'] = (
        cleaned_data['health_condition'] * cleaned_data['average_student_score']
    )
    cleaned_data['attendance_efficiency'] = (
        cleaned_data['attendance_rate'] / cleaned_data['average_expected_student_attendance']
    )
    cleaned_data['discipline_score'] = (
        cleaned_data['student_offence'] + cleaned_data['disciplinary_action_taken']
    )

    return cleaned_data


def train_model(X_train, y_train):
    """
    Trains a Random Forest model.

    Args:
        X_train (pd.DataFrame): Training features.
        y_train (pd.Series): Training target (log-transformed).

    Returns:
        RandomForestRegressor: Trained model.
    """
    model = RandomForestRegressor(random_state=42, n_estimators=300, max_depth=15)
    model.fit(X_train, y_train)
    return model


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
            "Student ID": row["student_id"],
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


def write_to_db(conn, df, schema_name, table_name):
    """
    Writes a DataFrame to the database.

    Args:
        conn: Database connection.
        df (pd.DataFrame): DataFrame to write.
        schema_name (str): Schema name.
        table_name (str): Table name.
    """
    try:
        full_table_name = f"{schema_name}.{table_name}"
        conn.execute(f"DROP TABLE IF EXISTS {full_table_name};")
        conn.register("temp_table", df)
        conn.execute(f"CREATE TABLE {full_table_name} AS SELECT * FROM temp_table;")
        print(f"Data successfully written to {full_table_name}")
    except Exception as e:
        print(f"Error writing to the database: {e}")