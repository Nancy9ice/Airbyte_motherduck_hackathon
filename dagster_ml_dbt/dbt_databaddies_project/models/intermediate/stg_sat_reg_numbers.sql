SELECT 
    student_id,
    sat_registration_number
FROM {{ source('dbt_databaddies_project', 'raw_student_sat_reg_numbers') }}