with stg_track_artists as (
    select *
    from {{ source('raw', 'tracks') }}
),

exploded as (
    select
        id as track_id,
        unnest(regexp_extract_all(id_artists, '[A-Za-z0-9]{22}')) as artist_id
    from stg_track_artists
    where id is not null
)

select distinct
    track_id,
    artist_id
from exploded