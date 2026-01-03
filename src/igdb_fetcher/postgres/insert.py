import psycopg

from igdb_fetcher.postgres.url import get_connection_url


def insert_companies_into_postgres(companies):
    with psycopg.connect(get_connection_url()) as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO app.igdb_company (id, name, country_code) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING",
                companies,
            )
            inserted = cur.rowcount
        conn.commit()
    return inserted


def insert_collections_into_postgres(collections):
    with psycopg.connect(get_connection_url()) as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO app.igdb_collection (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
                collections,
            )
            inserted = cur.rowcount
        conn.commit()
    return inserted


def insert_games_into_postgres(games):
    with psycopg.connect(get_connection_url()) as conn:
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO app.igdb_game
                               (id, name, summary, release_date, genres, themes, screenshots, collections, cover,
                                artwork_with_logo, artwork_without_logo, psn_website, official_website,
                                community_wiki_website, youtube_ids, developers, publishers)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                       %s) ON CONFLICT (id) DO
            UPDATE
                SET summary = EXCLUDED.summary, genres = EXCLUDED.genres, themes = EXCLUDED.themes, screenshots = EXCLUDED.screenshots, collections = EXCLUDED.collections, cover = EXCLUDED.cover, artwork_with_logo = EXCLUDED.artwork_with_logo, artwork_without_logo = EXCLUDED.artwork_without_logo, psn_website = EXCLUDED.psn_website, official_website = EXCLUDED.official_website, community_wiki_website = EXCLUDED.community_wiki_website, youtube_ids = EXCLUDED.youtube_ids, developers = EXCLUDED.developers, publishers = EXCLUDED.publishers
                            """,
                            games)
            affected = cur.rowcount
        conn.commit()
    return affected


def insert_candidates_into_postgres(candidates):
    with psycopg.connect(get_connection_url()) as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO app.igdb_candidate (game_id, candidate_id, score, status) VALUES (%s, %s, %s, %s) ON CONFLICT (game_id, candidate_id) DO NOTHING",
                candidates,
            )
            inserted = cur.rowcount
        conn.commit()
    return inserted
