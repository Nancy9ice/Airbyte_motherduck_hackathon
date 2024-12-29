SELECT DISTINCT
    id as school_id,
    CAST(syear AS INT) as session_year,
    title as school_name,
    address as school_address,
    city,
    state,
    zipcode,
    phone,
    principal,
    www_address as website_url,
    school_number as school_phone_number,
    short_name,
    reporting_gp_scale,
    grading_scale,
    sort_order,
    created_at as school_created_at,
    STRFTIME(created_at, '%Y%m%d') AS school_created_date_id,
    updated_at as school_updated_at,
    STRFTIME(updated_at, '%Y%m%d') AS school_updated_date_id
FROM {{ source('dbt_databaddies_project', 'raw_schools') }}