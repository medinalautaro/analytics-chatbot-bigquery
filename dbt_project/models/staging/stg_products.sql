select
    product_id,
    product_name,
    category,
    price,
    supplier,
    base_return_rate
from {{ source('raw', 'products') }}