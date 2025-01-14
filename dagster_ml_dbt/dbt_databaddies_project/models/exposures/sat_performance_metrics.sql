WITH total_scores as (
    SELECT 
        student_course_id,
        term,
        SUM(total_scores) as total_scores
    FROM {{ ref('fact_school_grades') }}
    GROUP BY student_course_id, term
),

school_grades AS (
SELECT 
    sc.student_id,
    ROUND(AVG(ts.total_scores), 1) AS average_student_score  -- Calculate average scores across terms
FROM 
    total_scores AS ts
LEFT JOIN 
    {{ ref('stg_students_courses') }} AS sc 
ON 
    ts.student_course_id = sc.student_course_id
GROUP BY 
    sc.student_id-- Group by student_id and course_id to get the average score
ORDER BY student_id
),

aggregated_attendance AS (
    SELECT 
        sc.student_id,
        AVG(att.minutes_present) AS avg_student_minutes_present,
        AVG(att.total_minutes) AS avg_student_total_minutes
    FROM 
        {{ ref('stg_attendance') }} att
    LEFT JOIN 
        {{ ref('stg_students_courses') }} sc
    ON 
        att.student_course_id = sc.student_course_id
    GROUP BY sc.student_id
)

SELECT DISTINCT
    students.student_id,
    students.full_name AS student_name,
    students.student_class,
    students.student_status,
    students.health_condition,
    department,
    gender,
    parents.full_name AS student_parent,
    parents.education_level AS parent_education,
    student_activity_status,
    student_extracurricular_activity,
    CAST(agg_attendance.avg_student_minutes_present AS BIGINT) AS average_student_minutes_attendance,
    CAST(agg_attendance.avg_student_total_minutes AS BIGINT) AS average_expected_student_attendance,
    sg.average_student_score,
    CASE 
        WHEN average_student_score >= 50 THEN 'Pass'
        WHEN average_student_score < 50 THEN 'Fail'
    END AS student_school_performance,
    CASE 
        WHEN discipline.student_offence IS NULL THEN 'None'
        ELSE discipline.student_offence
    END AS student_offence,
    CASE 
        WHEN disciplinary_action_taken IS NULL THEN 'None'
        ELSE disciplinary_action_taken
    END AS disciplinary_action_taken,
    CASE 
        WHEN teacher.full_name IS NULL THEN 'None'
        ELSE teacher.full_name
    END AS disciplinary_teacher,
    students.profile_image,
    sat.exam_year AS sat_exam_year,
    sat.registration_number,
    sat.sat_score,
    -- The school's threshold for sat performance is 900
    CASE 
        WHEN sat.sat_score >= 900 THEN 'Pass'
        WHEN sat.sat_score < 900 THEN 'Fail'
    END AS sat_performance
FROM {{ ref('dim_students') }} students
LEFT JOIN {{ ref('stg_parents') }} parents
    ON students.parent_id = parents.parent_id
LEFT JOIN {{ ref('stg_students_courses') }} students_courses
    ON students_courses.student_id = students.student_id
LEFT JOIN aggregated_attendance agg_attendance
    ON agg_attendance.student_id = students.student_id
LEFT JOIN school_grades sg
    ON sg.student_id = students.student_id
LEFT JOIN {{ ref('stg_sat_reg_numbers') }} sat_reg
    ON sat_reg.student_id = students.student_id
LEFT JOIN {{ ref('stg_sat_scores') }} sat
    ON sat.registration_number = sat_reg.sat_registration_number
LEFT JOIN {{ ref('stg_disciplinary_records') }} discipline
    ON discipline.student_id = students.student_id
LEFT JOIN {{ ref('stg_teachers') }} teacher
    ON discipline.teacher_id = teacher.teacher_id
