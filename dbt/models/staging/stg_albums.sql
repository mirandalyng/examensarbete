with stg_albums as (select * from {{ source('raw', 'dataset') }})

select
    track_id,
    max(nullif(trim(regexp_replace(album_name, '\s+', ' ', 'g')), '')) as album
from stg_albums
where track_id is not null
  and nullif(trim(album_name), '') is not null
group by track_id