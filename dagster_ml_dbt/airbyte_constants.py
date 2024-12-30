from dotenv import load_dotenv
import os
from dagster_airbyte import AirbyteCloudResource
from dagster import EnvVar

# Load environment variables from .env file
load_dotenv()

# Define the Airbyte resource
airbyte_instance = AirbyteCloudResource(
    client_id=EnvVar("AIRBYTE_CLIENT_ID"),
    client_secret=EnvVar("AIRBYTE_CLIENT_SECRET"),
)
