# schedules.py
from dagster import ScheduleDefinition
from dagster_ml_dbt.jobs import airbyte_dbt_sync_job

# Define your schedules separately
daily_airbyte_dbt_schedule = ScheduleDefinition(
    job=airbyte_dbt_sync_job,  # Airbyte sync job
    cron_schedule="@daily",  # Runs the Airbyte sync daily at 12am
)
