SELECT DISTINCT
    student_course_id,
    total_minutes,
    minutes_present,
    created_at as attendance_created_at,
    STRFTIME(created_at, '%Y%m%d') AS attendance_created_date_id,
    updated_at as attendance_updated_at,
    STRFTIME(updated_at, '%Y%m%d') AS attendance_updated_date_id
FROM {{ source('dbt_databaddies_project', 'raw_attendance_day') }}