# repository.py
from dagster import Definitions, repository
from dagster_ml_dbt.assets.airbyte_assets import airbyte_assets
from dagster_ml_dbt.assets.dbt_assets import my_dbt_assets, dbt_resource
from dagster_ml_dbt.motherduck_constants import motherduck
from dagster_ml_dbt.airbyte_constants import airbyte_instance
from dagster_ml_dbt.jobs import airbyte_dbt_sync_job, sat_ml_pipeline
from dagster import (
    ScheduleDefinition,
    Definitions,
)
from assets.ml_assets import (fetch_sat_data, 
                            preprocess_sat_data, 
                            split_train_test, 
                            train_rf_model_asset, 
                            predict_and_generate_recommendations, 
                            write_recommendations_to_motherduck)

# Define the Dagster definitions
defs = Definitions(
    assets=airbyte_assets + [my_dbt_assets] + [
        fetch_sat_data,
        preprocess_sat_data,
        split_train_test,
        train_rf_model_asset,
        predict_and_generate_recommendations,
        write_recommendations_to_motherduck
    ],
    schedules=[
        ScheduleDefinition(
            job=airbyte_dbt_sync_job,  # Schedule for Airbyte job
            cron_schedule="@daily",  # Runs the Airbyte sync daily at 12am
        ),
        ScheduleDefinition(
            job=sat_ml_pipeline,  # Schedule for the SAT ML pipeline
            cron_schedule="0 1 * * *",  # Runs SAT pipeline daily at 1am
        ),
    ],
    jobs=[airbyte_dbt_sync_job, sat_ml_pipeline],  # Include the defined jobs
    resources={"airbyte": airbyte_instance, "dbt": dbt_resource, "duckdb": motherduck},  # Define required resources
)
