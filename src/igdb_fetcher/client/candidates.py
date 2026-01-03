import time
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from igdb_fetcher.client.constants import *
from igdb_fetcher.client.games import post_search_games_query
from igdb_fetcher.client.image import get_image_url
from igdb_fetcher.client.score import compute_candidate_score


def get_candidates_for_games(games):
    candidates = []
    for game in games:
        game_id = game.get("id")
        game_title = game.get("title")
        candidates_for_game = post_search_games_query(game_title)
        print(f"Found {len(candidates_for_game)} candidates for {game_title}")
        _format_candidates(candidates_for_game, game_title, game_id)
        time.sleep(1)
        candidates.extend(candidates_for_game)

    return candidates


def _format_candidates(candidates: list[dict[str, Any]], game_title, game_id):
    for candidate in candidates:
        candidate["local_id"] = game_id

        # Compute score
        candidate_name = candidate.get("name", "")
        candidate["score"] = compute_candidate_score(game_title, candidate_name)

        # Format genres and themes
        genres = []
        for genre in candidate.get("genres", []):
            genres.append(genre.get("name", ""))
        candidate["genres"] = genres
        themes = []
        for theme in candidate.get("themes", []):
            themes.append(theme.get("name", ""))
        candidate["themes"] = themes

        # Format images (cover, artworks, screenshots)
        cover_image = candidate.get("cover", {}).get("image_id")
        candidate["cover"] = get_image_url(cover_image) if cover_image else None

        for artwork in candidate.get("artworks", []):
            url = get_image_url(artwork.get("image_id"), "t_720p")
            if artwork.get("artwork_type", {}).get("id", "") == 3: candidate["artwork_with_logo"] = url
            if artwork.get("artwork_type", {}).get("id", "") == 2: candidate["artwork_without_logo"] = url
        candidate.pop("artworks", None)

        screenshots = []
        for screenshot in candidate.get("screenshots", []):
            url = get_image_url(screenshot.get("image_id"), "t_720p")
            screenshots.append(url)
        candidate["screenshots"] = screenshots

        # Format websites
        for website in candidate.get("websites", []):
            website_type = website.get("type", {}).get("id", "")
            if website_type == PLAYSTATION_WEBSITE_TYPE:
                candidate["psn_website"] = website.get("url", "")
            if website_type == OFFICIAL_WEBSITE_TYPE:
                candidate["official_website"] = website.get("url", "")
            if website_type == COMMUNITY_WIKI_WEBSITE_TYPE:
                candidate["community_wiki_website"] = website.get("url", "")
        candidate.pop("websites", None)

        # Format youtube video ids
        youtube_ids = []
        for video in candidate.get("videos", []):
            if video.get("video_id", ""):
                youtube_ids.append(video.get("video_id"))
        candidate["youtube_ids"] = youtube_ids
        candidate.pop("videos", None)

        # Format involved companies
        developers = []
        publishers = []
        for involved_company in candidate.get("involved_companies", []):
            company_name = involved_company.get("company", {}).get("name", "")
            company_id = involved_company.get("company", {}).get("id", "")
            company_country = involved_company.get("company", {}).get("country", "")
            company = {"id": company_id, "name": company_name, "country": company_country}
            if involved_company.get("developer", False): developers.append(company)
            if involved_company.get("publisher", False): publishers.append(company)
        candidate["developers"] = developers
        candidate["publishers"] = publishers
        candidate.pop("involved_companies", None)

        # Format release date
        release_datetime = datetime.fromtimestamp(candidate.get("first_release_date", 0), tz=ZoneInfo("Europe/Paris"))
        release_date = release_datetime.strftime("%Y-%m-%d")
        candidate["release_date"] = release_date
        candidate.pop("first_release_date", None)

    candidates.sort(key=lambda x: x.get("score", 0), reverse=True)
    filtered_candidates = [g for g in candidates if g.get("score", 0) >= 50]

    return filtered_candidates
