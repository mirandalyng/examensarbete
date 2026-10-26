with stg_tracks as (select * from {{ source('raw', 'tracks') }})

select
    id as track_id,
    name as track_name,
    cast(left(release_date, 4) as int) as release_year,
    popularity as track_popularity
from stg_tracks
where track_id is not null
