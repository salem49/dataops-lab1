-- The six quality rules from TP1 and TP2. The first rule that matches wins.
select
    *,
    case
        when customer_id is null                         then 'missing_customer_id'
        when order_date is null                          then 'invalid_date'
        when quantity is null or quantity <= 0           then 'invalid_quantity'
        -- Rules 4, 5 and 6 go here.
          when unit_price is null or unit_price not between 0.01 and 1000
            then 'invalid_unit_price'

        -- Règle 5 : une ligne par order_id, garder la première
        when row_number() over (partition by order_id order by _row_number) > 1
            then 'duplicate_order_id'

        -- Règle 6 : seulement les cinq pays de la boutique
        when country not in ('France', 'Germany', 'Italy', 'Morocco', 'Tunisia')
            then 'unknown_country'
    end as reject_reason
from {{ ref('stg_orders') }}



