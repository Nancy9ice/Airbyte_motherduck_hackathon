from dotenv import load_dotenv
import os
from dagster_duckdb import DuckDBResource
from dagster import EnvVar

# Load environment variables from .env file
load_dotenv()

motherduck = DuckDBResource(
        database="md:Airbyte_Motherduck_Hackathon?motherduck_token={{env_var('MOTHERDUCK_TOKEN')}}"
        )