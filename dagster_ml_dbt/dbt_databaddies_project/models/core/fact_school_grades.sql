SELECT
    {{ dbt_utils.generate_surrogate_key(['student_course_id', 'marking_period_id']) }} as student_grades_id,
    student_course_id,
    CASE
        WHEN marking_period_id IN (1, 2, 3) THEN 'First Term'
        WHEN marking_period_id IN (4, 5, 6) THEN 'Second Term'
        WHEN marking_period_id IN (7, 8, 9) THEN 'Third Term'
    END AS term,
    CASE
        WHEN marking_period_id IN (1, 4, 7) THEN 'Principal Test'
        WHEN marking_period_id IN (2, 5, 8) THEN 'Midterm Test'
        WHEN marking_period_id IN (3, 6, 9) THEN 'Exams'
    END AS assessment_type,
    SUM(scores) AS total_scores,  -- Sum scores for each student_course_id and term
    CASE
        WHEN marking_period_id IN (1, 4, 7) THEN 10
        WHEN marking_period_id IN (2, 5, 8) THEN 20
        WHEN marking_period_id IN (3, 6, 9) THEN 70
    END AS overall_score
FROM {{ ref ('stg_students_grades') }}
GROUP BY 
    student_course_id, 
    term,  -- Group by student_course_id and term
    marking_period_id,
    assessment_type,
    overall_score
ORDER BY student_course_id, term