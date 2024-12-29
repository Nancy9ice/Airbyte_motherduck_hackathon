SELECT DISTINCT
    student_course_id,
    student_id,
    course_id,
    grade_level_id as class_id,
    created_at,
    STRFTIME(created_at, '%Y%m%d') AS created_date_id,
    updated_at,
    STRFTIME(updated_at, '%Y%m%d') AS updated_date_id
FROM {{ source('dbt_databaddies_project', 'raw_students_courses') }}