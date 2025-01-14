import logging
import pandas as pd
from dagster import op, asset
from dagster import asset, MaterializeResult
from dagster_ml_dbt.ml_helper_functions import clean_and_preprocess_data, train_rf_model, generate_recommendations
from dagster_duckdb import DuckDBResource


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='waec_model_run.log',
    filemode='a'
)

@asset
def fetch_sat_data(duckdb: DuckDBResource):
    logging.info("Fetching SAT data from the database.")
    query = "SELECT * FROM student_sat_data"
    with duckdb.get_connection() as conn:
        sat_data = get_data_from_db(query, conn)
        if sat_data is None or sat_data.empty:
            raise ValueError("No data retrieved from the database.")
    return sat_data


@asset
def preprocess_sat_data(fetch_sat_data: pd.DataFrame):
    logging.info("Cleaning and preprocessing SAT data.")
    sat_data_cleaned, label_encoders = clean_and_preprocess_data(fetch_sat_data)
    return {"data": sat_data_cleaned, "label_encoders": label_encoders}


@asset
def split_train_test(preprocess_sat_data):
    sat_data_cleaned = preprocess_sat_data["data"]
    features = [
        'attendance_rate', 'average_student_score', 'parent_education_effect',
        'activity_attendance_interaction', 'health_score_effect', 'attendance_efficiency',
        'discipline_score', 'student_status', 'student_class', 'department'
    ]
    target = 'sat_score'

    train_data = sat_data_cleaned[sat_data_cleaned['sat_score'] > 0].copy()
    test_data = sat_data_cleaned[sat_data_cleaned['sat_score'] == 0].copy()

    if train_data.empty or test_data.empty:
        raise ValueError("Training or test data is empty. Ensure the database contains valid data.")

    train_data['log_sat_score'] = np.log1p(train_data['sat_score'])
    X_train = train_data[features]
    y_train = train_data['log_sat_score']
    X_test = test_data[features]
    return {"X_train": X_train, "y_train": y_train, "X_test": X_test, "test_data": test_data}


@asset
def train_rf_model_asset(split_train_test):
    X_train = split_train_test["X_train"]
    y_train = split_train_test["y_train"]
    logging.info("Training the Random Forest model.")
    rf_model, train_rmse, train_r2 = train_rf_model(X_train, y_train)
    logging.info(f"Model training completed. Train RMSE: {train_rmse:.2f}, Train R2: {train_r2:.2f}")
    return rf_model


@asset
def predict_and_generate_recommendations(train_rf_model_asset, split_train_test, preprocess_sat_data):
    rf_model = train_rf_model_asset
    X_test = split_train_test["X_test"]
    test_data = split_train_test["test_data"]
    label_encoders = preprocess_sat_data["label_encoders"]

    logging.info("Predicting SAT scores and generating recommendations.")
    y_pred_log = rf_model.predict(X_test)
    y_pred = np.expm1(y_pred_log)

    recommendations_df = generate_recommendations(test_data, y_pred, label_encoders)
    return recommendations_df


@asset
def write_recommendations_to_motherduck(duckdb: DuckDBResource, predict_and_generate_recommendations: pd.DataFrame):
    logging.info("Writing recommendations to the database.")
    recommendations_df = predict_and_generate_recommendations
    with duckdb.get_connection() as conn:
        conn.execute("CREATE TABLE exposures.sat_score_recommendations AS SELECT * FROM sat_score_recommendations")
