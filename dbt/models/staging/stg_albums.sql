with stg_albums as (select * from {{ source('raw', 'dataset') }})

select
    track_id,
    album_name
from stg_albums
where track_id is not null