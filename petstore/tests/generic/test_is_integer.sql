{% test is_integer(model, column_name, pk_column_name) %}

with validation as (
    select
        {{ pk_column_name }} as id,
        {{ column_name }} as int_field
    from {{ model }}
),
validation_errors as (
    select
        id,
        int_field
    from validation
    where (int_field is not null and TRY_CAST(int_field AS integer) is null)
    or    TRY_CAST(TRY_CAST(int_field AS integer) AS numeric) <> TRY_CAST(int_field as numeric)
)
select *
from validation_errors

{% endtest %}
