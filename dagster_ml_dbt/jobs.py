from dagster import (
    define_asset_job,
    AssetSelection,
)
from dagster_ml_dbt.assets.dbt_assets import my_dbt_assets
from dagster_ml_dbt.assets.ml_assets import (fetch_sat_data, 
                            preprocess_sat_data, 
                            split_train_test, 
                            train_rf_model_asset, 
                            predict_and_generate_recommendations, 
                            write_recommendations_to_motherduck)

# Define job to run Airbyte sync and dbt build
airbyte_dbt_sync_job = define_asset_job(
    "airbyte_mysql_to_motherduck_to_dbt",
    AssetSelection.assets(my_dbt_assets)
    .upstream()
    .required_multi_asset_neighbors(),  # all Airbyte assets linked to the same connection
    )


# Define the job for SAT data assets
sat_ml_pipeline = define_asset_job(
    "sat_ml_pipeline_job",
    AssetSelection.assets(fetch_sat_data, 
                        preprocess_sat_data, 
                        split_train_test,
                        train_rf_model_asset,
                        predict_and_generate_recommendations,
                        write_recommendations_to_motherduck)
    .upstream()
    )