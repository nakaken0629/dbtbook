with source as (

    select * from {{ source('petstore', 'species_master') }}

),

renamed as (

    select
        species_id,
        species_name

    from source

)

select * from renamed
