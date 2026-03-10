{{ config(
    materialized='table',
    cluster_by=['category', 'supplier']
) }}

select
    product_id,
    product_name,
    category,
    price,
    supplier,
    base_return_rate
from {{ ref('stg_products') }}