SELECT DISTINCT
    id as class_id,
    school_id,
    short_name as class_short_name,
    title as class_title,
    sort_order,
    created_at as class_created_at,
    STRFTIME(created_at, '%Y%m%d') AS class_created_date_id,
    updated_at as class_updated_at,
    STRFTIME(updated_at, '%Y%m%d') AS class_updated_date_id
FROM {{ source('dbt_databaddies_project', 'raw_school_gradelevels') }}
