SELECT 
    student_id,
    waec_registration_number
FROM {{ source('dbt_databaddies_project', 'raw_student_waec_reg_numbers') }}