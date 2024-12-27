SELECT DISTINCT
    id as offence_id,
    student_id,
    school_id,
    staff_id as teacher_id,
    entry_date as offence_recorded_date,
    STRFTIME(entry_date, '%Y%m%d') AS offence_recorded_date_id,
    referral_date as disciplinary_date,
    STRFTIME(referral_date, '%Y%m%d') AS disciplinary_date_id,
    offence as student_offence,
    action_taken as disciplinary_action_taken
FROM {{ source('dbt_databaddies_project', 'raw_discipline_referrals') }}

