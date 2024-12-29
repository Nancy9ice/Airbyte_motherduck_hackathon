SELECT DISTINCT
    student_id,
    activity_id,
    created_at,
    CASE 
        WHEN is_active = 1 THEN 'Active'
        WHEN is_active = 0 THEN 'Not active'
    END AS student_activity_status,
    STRFTIME(created_at, '%Y%m%d') AS created_date_id,
    updated_at,
    STRFTIME(updated_at, '%Y%m%d') AS updated_date_id
FROM {{ source('dbt_databaddies_project', 'raw_eligibility') }}