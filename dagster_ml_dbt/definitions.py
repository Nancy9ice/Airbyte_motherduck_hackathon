# repository.py
from dagster import Definitions, repository
from dagster_ml_dbt.assets.airbyte_instance import airbyte_assets
from dagster_ml_dbt.assets.motherduck_dbt import my_dbt_assets, dbt_resource
from dagster_ml_dbt.motherduck_constants import motherduck
from dagster_ml_dbt.airbyte_constants import airbyte_instance
from dagster_ml_dbt.jobs import airbyte_dbt_sync_job
from dagster import (
    ScheduleDefinition,
    Definitions,
)

# Define the Dagster definitions
defs = Definitions(
    assets=airbyte_assets + [my_dbt_assets],
    schedules=[
        ScheduleDefinition(
            job=airbyte_dbt_sync_job,  # Schedule for Airbyte job
            cron_schedule="@daily",  # Runs the Airbyte sync daily at 12am
        ),
    ],
    jobs=[airbyte_dbt_sync_job],  # Include the defined jobs
    resources={"airbyte": airbyte_instance, "dbt": dbt_resource, "duckdb": motherduck},  # Define required resources
)
