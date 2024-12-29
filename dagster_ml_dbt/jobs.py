from dagster import (
    define_asset_job,
    AssetSelection,
)
from dagster_ml_dbt.assets.motherduck_dbt import my_dbt_assets
from dagster_ml_dbt.assets.airbyte_instance import airbyte_assets  # Import Airbyte assets if needed

# Define job to run Airbyte sync and dbt build
airbyte_dbt_sync_job = define_asset_job(
    "airbyte_mysql_to_motherduck_to_dbt",
    AssetSelection.assets(my_dbt_assets)
    .upstream()
    .required_multi_asset_neighbors(),  # all Airbyte assets linked to the same connection
    )