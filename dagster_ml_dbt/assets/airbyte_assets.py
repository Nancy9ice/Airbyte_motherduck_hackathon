from dagster_airbyte import build_airbyte_assets


# Build Airbyte assets
airbyte_assets_1 = build_airbyte_assets(
    connection_id="b9e8f94e-ebba-4335-abed-c8785d3627cd",
    destination_tables=[
        "raw_attendance_day", "raw_calendar_events", "raw_courses",
        "raw_discipline_referrals", "raw_eligibility", "raw_eligibility_activities",
        "raw_marking_periods", "raw_parent", "raw_portal_polls",
        "raw_school_gradelevels", "raw_schools", "raw_student_assessment_grades", 
        "raw_student_sat_reg_numbers", "raw_student_waec_reg_numbers",
        "raw_students", "raw_students_courses", "raw_teachers"
    ],
    asset_key_prefix=["dbt_databaddies_project"],
)


airbyte_assets_2 = build_airbyte_assets(
    connection_id="1c21bf15-064a-439e-bb9c-a758fbbfb481",
    destination_tables=[
        "raw_sat_result_checker_2019", "raw_sat_result_checker_2020", "raw_sat_result_checker_2021"
    ],
    asset_key_prefix=["dbt_databaddies_project"],
)

airbyte_assets_3 = build_airbyte_assets(
    connection_id="63b47f56-b424-49b4-a886-961457d5765e",
    destination_tables=[
        "raw_waec_result_checker_2019", "raw_waec_result_checker_2020", "raw_waec_result_checker_2021"
    ],
    asset_key_prefix=["dbt_databaddies_project"],
)

airbyte_assets = airbyte_assets_1 + airbyte_assets_2 + airbyte_assets_3
