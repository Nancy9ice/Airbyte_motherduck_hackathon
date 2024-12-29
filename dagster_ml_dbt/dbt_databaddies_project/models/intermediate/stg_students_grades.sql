SELECT DISTINCT
    student_course_id,
    marking_period_id,
    points as scores
FROM {{ source('dbt_databaddies_project', 'raw_student_assessment_grades') }}