-- quiz_tracks: one row per track with artists, year, broad genres and album.
-- This is the table the quiz agent reads from.

with
    stg_albums as (select * from {{ ref('stg_albums') }}),
    stg_artists as (select * from {{ ref('stg_artists') }}),
    stg_tracks as (select * from {{ ref('stg_tracks') }}),
    stg_track_artists as (select * from {{ ref('stg_track_artists') }}),
    genre_mapping as (select * from {{ ref('genre_mapping') }}),

    -- 1. One row per artist and sub-genre.
    -- artist_genre is stored as text like "['dance pop', 'pop']",
    -- so parse_list turns it into a real list before unnesting.
    -- Hyphens are replaced so "hip-hop" matches the keyword "hip hop".
    artist_genres as (
        select
            a.artist_id,
            g.sub_genre,
            lower(replace(g.sub_genre, '-', ' ')) as genre_normalized
        from stg_artists a,
            unnest({{ parse_list('a.artist_genre') }}) as g(sub_genre)
        -- Artists without any genre are left out here.
        where a.artist_genre <> 'Missing genre'
    ),

    -- 2. Map each sub-genre to a main genre using the seed.
    -- A sub-genre can match several keywords (e.g. "pop rock" matches
    -- both "pop" and "rock"), so we keep the match with the lowest
    -- priority number, and the longest keyword if priorities are equal.
    -- Sub-genres with no match become 'other'.
    artist_genres_mapped as (
        select
            ag.artist_id,
            ag.sub_genre,
            coalesce(m.main_genre, 'other') as main_genre
        from artist_genres ag
        left join genre_mapping m
            on contains(ag.genre_normalized, m.genre_keyword)
        qualify row_number() over (
            partition by ag.artist_id, ag.sub_genre
            order by m.priority asc nulls last, length(m.genre_keyword) desc
        ) = 1
    ),

    -- 3. Back to one row per artist, with a list of main genres.
    -- 'other' is only kept when the artist has no real main genre.
    artist_main_genres as (
        select
            artist_id,
            coalesce(
                list(distinct main_genre) filter (where main_genre <> 'other'),
                ['other']
            ) as main_genres
        from artist_genres_mapped
        group by artist_id
    ), 

-- 4. Join tracks with their artists, genres and album,
-- then collapse to one row per track.
-- Tracks without a matching artist are dropped by the inner joins.
    quiz_tracks_raw as(
        select
            t.track_id,
            t.track_name,
            t.release_year,
            t.track_popularity,
            -- A track can have several artists: combine their names.
            string_agg(distinct ar.artist_name, ', ') as artist_names,
            -- The most popular artist on the track.
            max(ar.artist_popularity) as artist_popularity,
            -- Main genres from the seed, merged across all artists on the track.
            list_distinct(flatten(list(amg.main_genres))) as genres,
            -- dataset.csv has at most one album per track after staging.
            coalesce(any_value(al.album), 'Missing album') as album
        from stg_tracks t
        join stg_track_artists ta on t.track_id = ta.track_id
        join stg_artists ar on ta.artist_id = ar.artist_id
        left join artist_main_genres amg on ar.artist_id = amg.artist_id
        left join stg_albums al on t.track_id = al.track_id
        group by t.track_id, t.track_name, t.release_year, t.track_popularity
    )


select count(*)
from quiz_tracks_raw
where {{ is_latin_text('track_name') }}
  and {{ is_latin_text('artist_names') }}
  and (album is null or {{ is_latin_text('album') }})
  and (
    (artist_popularity > 50 and track_popularity > 20)
    or 
    (track_popularity > 50 and artist_popularity > 20)
  )

-- total rows 233,688k 
--   and artist_popularity > 50 and track_popularity > 20
--   or track_popularity > 50 and artist_popularity > 20

-- total 83k 
--  and artist_popularity > 60 and track_popularity > 40
--   or track_popularity > 60 and artist_popularity > 40
