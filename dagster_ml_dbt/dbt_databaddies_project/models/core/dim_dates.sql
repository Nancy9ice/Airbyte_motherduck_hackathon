WITH date_dim AS (
    {{ dbt_date.get_date_dimension('2010-01-01', '2025-01-31') }}
)

SELECT * FROM date_dim