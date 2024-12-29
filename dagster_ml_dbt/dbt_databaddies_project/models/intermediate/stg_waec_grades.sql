SELECT DISTINCT
    exam_number,
    CAST(CAST(exam_year AS INTEGER) AS VARCHAR) AS exam_year,
    subjects AS courses,
    subject_grade AS waec_grade
FROM {{ source('dbt_databaddies_project', 'raw_waec_result_checker_2019') }}

UNION ALL

SELECT DISTINCT
    exam_number,
    CAST(CAST(exam_year AS INTEGER) AS VARCHAR) AS exam_year,
    subjects AS courses,
    subject_grade AS waec_grade
FROM {{ source('dbt_databaddies_project', 'raw_waec_result_checker_2020') }}

UNION ALL

SELECT DISTINCT
    exam_number,
    CAST(CAST(exam_year AS INTEGER) AS VARCHAR) AS exam_year,
    subjects AS courses,
    subject_grade AS waec_grade
FROM {{ source('dbt_databaddies_project', 'raw_waec_result_checker_2021') }}
