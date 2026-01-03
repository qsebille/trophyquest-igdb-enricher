import psycopg
from psycopg.rows import dict_row

from igdb_fetcher.postgres.url import get_connection_url


def select_unmapped_games():
    with psycopg.connect(get_connection_url(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT g.id, g.title FROM app.game g LEFT JOIN app.igdb_candidate c ON c.game_id = g.id WHERE c.candidate_id IS NULL LIMIT 20;"
            )
            rows = cur.fetchall()
            return rows
