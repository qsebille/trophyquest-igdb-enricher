from typing import Any

from igdb_fetcher.postgres.constants import PENDING_STATUS


def format_companies(candidates: list[dict[str, Any]]):
    companies: set[tuple[int, str, int]] = set()

    for candidate in candidates:
        for company in candidate.get("developers", []) + candidate.get("publishers", []):
            company_id = company.get("id")
            company_name = company.get("name")
            country_code = company.get("country")
            if company_id is None or company_name is None or country_code is None:
                continue
            companies.add((company_id, company_name, country_code))

    return list(companies)


def format_collections(candidates: list[dict[str, Any]]):
    collections: set[tuple[int, str]] = set()

    for candidate in candidates:
        for collection in candidate.get("collections", []):
            collection_id = collection.get("id")
            collection_name = collection.get("name")
            if collection_id is None or collection_name is None:
                continue
            collections.add((collection_id, collection_name))

    return list(collections)


def format_candidates(candidates_raw: list[dict[str, Any]]):
    candidates: set[tuple[str, int, int, str]] = set()

    for candidate in candidates_raw:
        game_id = candidate.get("local_id")
        candidate_id = candidate.get("id")
        score = candidate.get("score")

        candidates.add((game_id, candidate_id, score, PENDING_STATUS))

    return list(candidates)


def format_games(candidates_raw: list[dict[str, Any]]):
    games = []

    for candidate in candidates_raw:
        game_id = candidate.get("id")
        name = candidate.get("name")
        summary = candidate.get("summary")
        release_date = candidate.get("release_date")
        genres = candidate.get("genres", [])
        themes = candidate.get("themes", [])
        screenshots = candidate.get("screenshots", [])
        collections = [c["id"] for c in candidate.get("collections", []) if c.get("id")]
        cover = candidate.get("cover")
        artwork_with_logo = candidate.get("artwork_with_logo")
        artwork_without_logo = candidate.get("artwork_without_logo")
        psn_website = candidate.get("psn_website")
        official_website = candidate.get("official_website")
        community_wiki_website = candidate.get("community_wiki_website")
        youtube_ids = candidate.get("youtube_ids", [])
        developers = [d["id"] for d in candidate.get("developers", []) if d.get("id")]
        publishers = [p["id"] for p in candidate.get("publishers", []) if p.get("id")]

        games.append(
            (game_id, name, summary, release_date, genres, themes, screenshots, collections, cover, artwork_with_logo,
             artwork_without_logo, psn_website, official_website, community_wiki_website, youtube_ids, developers,
             publishers)
        )

    return games
