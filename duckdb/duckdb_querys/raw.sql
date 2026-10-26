-- Rows and duplicates
select count(*) as rader, count(distinct track_id) as unika_id from raw.dataset;

-- unique id's
select count(*) as rader, count(distinct id) as unika_id from raw.tracks;

-- Overlap: how many of the data-set songs exists in tracks?
select
    count(distinct d.track_id) as dataset_tracks,
    count(distinct t.id) as matchade,
    round(100.0 * count(distinct t.id) / count(distinct d.track_id), 1) as pct_matchade
from raw.dataset d
left join raw.tracks t on d.track_id = t.id;

-- How many tracks with popularity higher than 40
with m as (
    select d.track_id, max(d.popularity) as pop,
           any_value(try_cast(left(t.release_date, 4) as integer)) as yr
    from raw.dataset d
    join raw.tracks t on d.track_id = t.id
    group by d.track_id
)
select (yr / 10) * 10 as artionde,
       count(*) as alla,
       count(*) filter (where pop >= 40) as pop40
from m
group by 1 order by 1;

with d as (
    select distinct track_id,
           lower(track_name) as n,
           lower(trim(regexp_replace(split_part(artists, ';', 1), '[\[\]''"]', '', 'g'))) as a
    from raw.dataset
),
t as (
    select distinct lower(name) as n,
           lower(trim(split_part(regexp_replace(artists, '[\[\]''"]', '', 'g'), ',', 1))) as a
    from raw.tracks
)
select count(distinct d.track_id) as matchade_namn_artist
from d join t using (n, a);