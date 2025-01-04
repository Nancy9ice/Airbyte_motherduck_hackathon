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
    sc.student_course_id,
    ROUND(AVG(ts.total_scores), 1) AS average_student_score  -- Calculate average scores across terms
FROM 
    total_scores AS ts
LEFT JOIN 
    {{ ref('stg_students_courses') }} AS sc 
ON 
    ts.student_course_id = sc.student_course_id
GROUP BY 
    sc.student_course_id-- Group by student_id and course_id to get the average score
ORDER BY sc.student_course_id
)

SELECT
    students_courses.student_course_id,
    students.student_id,
    courses.course_id,
    students.full_name AS student_name,
    students.department,
    students.gender,
    students.health_condition,
    students.student_class,
    students.student_status,
    students.bus_pickup,
    students.bus_dropoff,
    students.student_activity_status,
    students.student_extracurricular_activity,
    courses.course_title AS course,
    courses.class_title as course_class,
    courses.course_department,
    parents.full_name AS parent,
    parents.education_level AS parent_education,
    courses.teacher AS teacher,
    CASE 
        WHEN polls.rating_type IS NULL THEN 'None'
        ELSE polls.rating_type
    END AS rating_type,
    CASE 
        WHEN polls.number_of_votes IS NULL THEN 0
        ELSE polls.number_of_votes
    END AS number_of_votes,
    CASE 
        WHEN discipline.student_offence IS NULL THEN 'None'
        ELSE discipline.student_offence
    END AS student_offence,
    CASE 
        WHEN discipline.disciplinary_action_taken IS NULL THEN 'None'
        ELSE discipline.disciplinary_action_taken
    END AS disciplinary_action_taken,
    CASE 
        WHEN teacher.full_name IS NULL THEN 'None'
        ELSE teacher.full_name
    END AS disciplinary_teacher,
    students.profile_image,
    average_student_score,
    CASE 
        WHEN average_student_score >= 50 THEN 'Pass'
        WHEN average_student_score < 50 THEN 'Fail'
    END AS student_evaluation,
    waec_grades.exam_year as waec_exam_year, -- Make sure this column exists in the waec_grades table
    waec_grades.exam_number,
    waec_grades.waec_grade,
    CAST(AVG(attendance.minutes_present) AS BIGINT) AS average_student_minutes_attendance,
    CAST(AVG(attendance.total_minutes) AS BIGINT) AS average_expected_student_attendance
FROM {{ ref('dim_students') }} students
LEFT JOIN {{ ref('stg_students_courses') }} students_courses
    ON students.student_id = students_courses.student_id
LEFT JOIN {{ ref('dim_courses') }} courses
    ON courses.course_id = students_courses.course_id
LEFT JOIN {{ ref('stg_parents') }} parents
    ON parents.parent_id = students.parent_id
LEFT JOIN {{ ref('stg_disciplinary_records') }} discipline
    ON discipline.student_id = students.student_id
LEFT JOIN {{ ref('stg_teachers') }} teacher
    ON discipline.teacher_id = teacher.teacher_id
LEFT JOIN {{ ref('stg_student_polls') }} polls
    ON teacher.teacher_id = polls.related_teacher_id
LEFT JOIN school_grades
    ON school_grades.student_course_id = students_courses.student_course_id
LEFT JOIN {{ ref('stg_waec_reg_numbers') }} waec_reg
    ON waec_reg.student_id = students_courses.student_id
LEFT JOIN {{ ref('stg_waec_grades') }} waec_grades
    ON waec_reg.waec_registration_number = waec_grades.exam_number

LEFT JOIN {{ ref('stg_attendance') }} attendance
    ON students_courses.student_course_id = attendance.student_course_id
GROUP BY 
    students_courses.student_course_id,
    students.student_id,
    courses.course_id,
    students.full_name,
    students.department,
    students.gender,
    students.student_status,
    students.health_condition,
    students.student_class,
    students.bus_pickup,
    students.bus_dropoff,
    students.student_activity_status,
    students.student_extracurricular_activity,
    courses.course_title,
    courses.class_title,
    courses.course_department,
    courses.teacher,
    teacher.full_name,
    parents.full_name,
    parents.education_level,
    polls.rating_type,
    polls.number_of_votes,
    average_student_score,
    discipline.student_offence,
    discipline.disciplinary_action_taken,
    waec_grades.exam_year,
    waec_grades.exam_number,
    waec_grades.waec_grade,
    students.profile_image
