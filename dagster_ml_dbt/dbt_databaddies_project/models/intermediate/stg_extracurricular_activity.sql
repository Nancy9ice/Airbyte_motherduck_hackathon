SELECT DISTINCT
    id as activity_id,
    school_id,
    title as activity,
    comment as activity_description,
    created_at as activity_created_at,
    STRFTIME(created_at, '%Y%m%d') AS activity_created_date_id,
    updated_at as activity_updated_at,
    STRFTIME(updated_at, '%Y%m%d') AS activity_updated_date_id
FROM {{ source('dbt_databaddies_project', 'raw_eligibility_activities') }}