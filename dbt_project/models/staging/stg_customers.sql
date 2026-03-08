select
    customer_id,
    cast(signup_date as timestamp) as signup_timestamp,
    country,
    coalesce(marketing_channel, 'unknown') as marketing_channel,
    coalesce(device_type, 'unknown') as device_type,
    repeat_propensity,
    value_score
from {{ source('raw', 'customers') }}