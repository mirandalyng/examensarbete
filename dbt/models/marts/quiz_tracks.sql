with
    stg_albums as (select * from {{ ref('stg_albums') }}),
    stg_artists as (select * from {{ ref('stg_artists') }}),
    stg_tracks as (select * from {{ ref('stg_tracks') }}),
    stg_track_artists as (select * from {{ ref('stg_track_artists') }}),
    genre_mapping as (select * from {{ ref('genre_mapping') }}),

    -- 1. en rad per artist och sub-genre
    artist_genres as (
        select
            a.artist_id,
            g.sub_genre,
            lower(replace(g.sub_genre, '-', ' ')) as genre_normalized
        from stg_artists a,
            unnest(a.artist_genre) as g(sub_genre)
    ),

    -- 2. slå upp main_genre i seeden, en träff per sub-genre
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

    -- 3. tillbaka till en rad per artist
    artist_main_genres as (
        select
            artist_id,
            list(distinct main_genre) as main_genres
        from artist_genres_mapped
        group by artist_id
    )

select
    t.track_id,
    t.track_name,
    t.track_popularity,
    ar.artist_name,
    ar.artist_popularity,
    amg.main_genres,
    ar.artist_genre as sub_genres,
    al.album
from stg_tracks t
left join stg_track_artists ta on t.track_id = ta.track_id
left join stg_artists ar on ta.artist_id = ar.artist_id
left join artist_main_genres amg on ar.artist_id = amg.artist_id
left join stg_albums al on t.track_id = al.track_id