SELECT DISTINCT
    parent_id,
    last_name,
    first_name,
    middle_name,
    CONCAT(last_name, ' ', middle_name, ' ', first_name) AS full_name,
    education_level,
    created_at as parent_registered_at,
    STRFTIME(created_at, '%Y%m%d') AS registration_date_id,
    updated_at as parent_updated_at,
    STRFTIME(updated_at, '%Y%m%d') AS updated_date_id
FROM {{ source('dbt_databaddies_project', 'raw_parent') }}