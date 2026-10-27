with stg_albums as (select * from {{ source('raw', 'dataset') }})

select
    track_id,
    MAX(NULLIF(TRIM(album_name), '')) as album
from stg_albums
where track_id is not null and album_name is not null
group by track_id
