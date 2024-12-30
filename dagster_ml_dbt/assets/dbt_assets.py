from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
import os

# Paths to dbt project
DBT_PROJECT_DIR = 'dagster_ml_dbt/dbt_databaddies_project'

# Define the dbt CLI resource
dbt_resource = DbtCliResource(
    project_dir=(os.fspath(DBT_PROJECT_DIR)),
    profiles_dir=(os.fspath(DBT_PROJECT_DIR))
)

# Define the dbt project assets
@dbt_assets(manifest=f"{DBT_PROJECT_DIR}/target/manifest.json")
def my_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()