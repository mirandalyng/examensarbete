with stg_artists as (select * from {{ source('raw', 'artists') }})

select
    id as artist_id,
    NULLIF(TRIM(name), '') as artist_name,
    coalesce(nullif(trim(genres), '[]'), 'Missing genre') as artist_genre, 
    popularity as artist_popularity
from stg_artists
where artist_id is not null and artist_name is not null


