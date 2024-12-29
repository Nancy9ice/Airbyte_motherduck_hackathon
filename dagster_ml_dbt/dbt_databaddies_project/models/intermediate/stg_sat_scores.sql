SELECT DISTINCT
    ceeb_code,
    registration_number,
    CAST(CAST(exam_year AS INTEGER) AS VARCHAR) AS exam_year,
    sat_score
FROM {{ source('dbt_databaddies_project', 'raw_sat_result_checker_2019') }}

UNION ALL

SELECT DISTINCT
    ceeb_code,
    registration_number,
    CAST(CAST(exam_year AS INTEGER) AS VARCHAR) AS exam_year,
    sat_score
FROM {{ source('dbt_databaddies_project', 'raw_sat_result_checker_2020') }}

UNION ALL

SELECT DISTINCT
    ceeb_code,
    registration_number,
    CAST(CAST(exam_year AS INTEGER) AS VARCHAR) AS exam_year,
    sat_score
FROM {{ source('dbt_databaddies_project', 'raw_sat_result_checker_2021') }}
