SELECT DISTINCT
    id as calendar_event_id,
    CAST(syear AS INT) as session_year,
    school_id,
    school_date as event_date,
    title as event_name,
    description as event_description,
    created_at as event_created_at,
    STRFTIME(created_at, '%Y%m%d') AS event_created_date_id,
    updated_at as event_updated_at,
    STRFTIME(updated_at, '%Y%m%d') AS event_updated_date_id
FROM {{ source('dbt_databaddies_project', 'raw_calendar_events') }}


