SELECT
    students.student_id,
    parent_id,
    students.full_name,
    class_short_name,
    CASE 
        WHEN classes.class_title IS NULL THEN 'Alumni'
        ELSE classes.class_title
    END as student_class,
    CASE 
        WHEN students.class_id <= 6 THEN 'Curent Student'
        WHEN students.class_id = 7 THEN '2021 Alumni'
        WHEN students.class_id = 8 THEN '2020 Alumni'
        WHEN students.class_id = 9 THEN '2019 Alumni'
    END AS student_status,
    bus_pickup,
    bus_dropoff,
    department,
    gender,
    health_condition,
    student_activity_status,
    CASE 
        WHEN student_activity_status = 'Active' THEN activity
        ELSE 'None'
    END AS student_extracurricular_activity,
    profile_image
FROM {{ ref ('stg_students') }} students
LEFT JOIN {{ ref ('stg_classes') }} classes
ON students.class_id = classes.class_id
LEFT JOIN {{ ref ('stg_student_activities') }} student_activities
ON students.student_id = student_activities.student_id
LEFT JOIN {{ ref ('stg_extracurricular_activity') }} activities
ON student_activities.activity_id = activities.activity_id
