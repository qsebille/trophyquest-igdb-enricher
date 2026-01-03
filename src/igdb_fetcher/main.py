from dotenv import load_dotenv

from igdb_fetcher.client.candidates import get_candidates_for_games
from igdb_fetcher.postgres.format import *
from igdb_fetcher.postgres.format import format_companies
from igdb_fetcher.postgres.insert import *
from igdb_fetcher.postgres.select import select_unmapped_games


def main():
    load_dotenv()

    games = select_unmapped_games()
    candidates_raw = get_candidates_for_games(games)
    print(f"Found {len(candidates_raw)} candidates to add to Postgres:")

    collections = format_collections(candidates_raw)
    companies = format_companies(candidates_raw)
    igbd_games = format_games(candidates_raw)
    candidates = format_candidates(candidates_raw)

    inserted_collections = insert_collections_into_postgres(collections)
    inserted_companies = insert_companies_into_postgres(companies)
    inserted_igbd_games = insert_games_into_postgres(igbd_games)
    inserted_candidates = insert_candidates_into_postgres(candidates)

    print(f"Inserted {inserted_collections} igdb_collection rows into Postgres")
    print(f"Inserted {inserted_companies} igdb_company rows into Postgres")
    print(f"Updated {inserted_igbd_games} igdb_game rows into Postgres")
    print(f"Inserted {inserted_candidates} igdb_candidate rows into Postgres")


if __name__ == "__main__":
    main()
