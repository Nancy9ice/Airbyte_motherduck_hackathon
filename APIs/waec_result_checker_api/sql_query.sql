-- Student Results
SELECT
    4123456 AS school_exam_id,
    CONCAT(4123456, LPAD(DENSE_RANK() OVER (PARTITION BY exam_year ORDER BY student_id), 3, '0')) AS exam_number,
    title AS subjects,
    waec_grade AS subject_grade,
    exam_year
FROM student_waec_grades swg
INNER JOIN students_courses sc
    ON swg.student_course_id = sc.student_course_id
LEFT JOIN courses c
    ON c.course_id = sc.course_id