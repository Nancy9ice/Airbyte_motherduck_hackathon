from setuptools import find_packages, setup

setup(
    name="dagster_ml_dbt",
    packages=find_packages(include=["assets", "dbt_databaddies_project"], exclude=["dagster_ml_dbt_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
    ],
    extras_require={
        "dev": ["dagster-webserver", "pytest"],
    },
)
