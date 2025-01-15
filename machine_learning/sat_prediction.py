import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import duckdb
import logging
from ml_helper_functions import (get_connection,
                                clean_and_preprocess_data,
                                feature_engineering,
                                train_model,
                                generate_recommendations,
                                write_to_db)


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:
    logging.info("Connecting to the database...")
    conn = get_connection()

    logging.info("Fetching data from the database...")
    query = "SELECT * FROM exposures.sat_performance_metrics"
    sat_data = pd.read_sql(query, conn)

    logging.info("Cleaning and preprocessing the data...")
    sat_data_cleaned, label_encoders = clean_and_preprocess_data(sat_data)

    logging.info("Performing feature engineering...")
    sat_data_cleaned = feature_engineering(sat_data_cleaned)

    # Define features and target
    features = [
        'attendance_rate', 'average_student_score', 'parent_education_effect',
        'activity_attendance_interaction', 'health_score_effect', 'attendance_efficiency',
        'discipline_score', 'student_status', 'department'
    ]
    target = 'sat_score'

    # Split data into train and test sets
    train_data = sat_data_cleaned[sat_data_cleaned['sat_score'] > 0]

    target_classes = label_encoders['student_class'].transform([
        'Senior Secondary School 3', 'Senior Secondary School 2', 'Senior Secondary School 1'
    ])
    test_data = sat_data_cleaned[
        (sat_data_cleaned['sat_score'] == 0) &
        (sat_data_cleaned['student_class_encoded'].isin(target_classes))
    ]

    logging.info(f"Rows in train_data: {len(train_data)}")
    logging.info(f"Rows in test_data: {len(test_data)}")

    if train_data.empty or test_data.empty:
        raise ValueError("Train or test data is empty. Please check the filtering logic.")

    
    train_data['log_sat_score'] = np.log1p(train_data['sat_score'])
    X_train = train_data[features]
    y_train = train_data['log_sat_score']
    X_test = test_data[features]

    logging.info("Training the model...")
    model = train_model(X_train, y_train)

    logging.info("Generating predictions...")
    y_pred_log = model.predict(X_test)
    y_pred = np.expm1(y_pred_log)

    logging.info("Generating recommendations...")
    # Reset index of test_data to ensure alignment
    test_data = test_data.reset_index(drop=True)

    # Generate recommendations
    recommendations_df = generate_recommendations(test_data, y_pred, label_encoders)

    # Preview recommendations
    print(recommendations_df.head())

    recommendations_df = pd.DataFrame(recommendations_df, columns = ['Student ID', 'Student Name', 'Predicted SAT Score', 'Outcome', 'Recommendation'])

    logging.info("Writing recommendations to the database...")
    write_to_db(conn, recommendations_df, schema_name="exposures", table_name="sat_recommendations")

    
except Exception as e:
    logging.error(f"An error occurred: {e}")