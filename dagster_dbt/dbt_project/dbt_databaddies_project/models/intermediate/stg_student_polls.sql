SELECT DISTINCT
    id AS poll_id,
    school_id,
    CAST(syear AS INT) AS session_year,
    title AS poll_description,
    CASE 
        WHEN poll_description LIKE '%Best%' THEN 'Bad'
        WHEN poll_description LIKE '%Worst%' THEN 'Good'
    END AS rating_type,
    votes_number AS number_of_votes,
    published_date,
    STRFTIME(published_date, '%Y%m%d') AS published_date_id,
    students_teacher_id AS related_teacher_id
FROM {{ source('dbt_databaddies_project', 'raw_portal_polls') }}
