SELECT DISTINCT
    course_id,
    subject_id,
    school_id,
    grade_level as class_id,
    teacher_id,
    title as course_title,
    short_name as course_short_name,
    CASE 
        WHEN department IS NULL THEN 'General'
    ELSE department
    END AS course_department,
    (credit_hours * 16 * 60) as total_teaching_hours_period,
    description as course_description,
    created_at as course_created_at,
    STRFTIME(created_at, '%Y%m%d') AS course_created_date_id,
    updated_at as course_updated_at,
    STRFTIME(updated_at, '%Y%m%d') AS course_updated_date_id
FROM {{ source('dbt_databaddies_project', 'raw_courses') }}

