{{ config(
    materialized='table',
    cluster_by=['country', 'marketing_channel']
) }}

select
    customer_id,
    signup_timestamp,
    country,
    marketing_channel,
    device_type,
    repeat_propensity,
    value_score
from {{ ref('stg_customers') }}