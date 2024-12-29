SELECT DISTINCT
    id AS teacher_id,
    last_name,
    first_name,
    middle_name,
    CONCAT_WS(' ', first_name, middle_name, last_name) AS full_name,
    created_at AS employment_date,
    STRFTIME(created_at, '%Y%m%d') AS employment_date_id,
    updated_at AS updated_employment_date,
    STRFTIME(updated_at, '%Y%m%d') AS updated_employment_date_id
FROM {{ source('dbt_databaddies_project', 'raw_teachers') }}