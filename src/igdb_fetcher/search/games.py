import datetime
import os
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from requests import post

from igdb_fetcher.search.constants import *
from igdb_fetcher.search.image import get_image_url
from igdb_fetcher.search.score import compute_candidate_score
from igdb_fetcher.search.token import get_igdb_token


def search_games(name: str, limit: int) -> list[dict[str, Any]]:
    token = get_igdb_token()
    client_id = os.environ["TWITCH_CLIENT_ID"]

    url = f"{IGDB_BASE}/games"
    query = f'''
        search "{name}";
        fields id, name, genres.name, themes.name, collections.name,
            videos.video_id,
            websites.url, websites.type.id,
            cover.image_id, screenshots.image_id,
            artworks.image_id, artworks.artwork_type.id,
            involved_companies.developer, involved_companies.publisher, involved_companies.company.name,
            first_release_date, summary;
        where version_parent = null & parent_game = null & platforms = ({PS4_PLATFORM_ID},{PS5_PLATFORM_ID});
        limit {limit};
        '''

    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    response = post(url, headers=headers, data=query, timeout=15)

    if not response.ok:
        raise RuntimeError(f"IGDB error {response.status_code}: {response.text}\nQuery:\n{query}")

    igdb_games: list[dict[str, Any]] = response.json()

    for game in igdb_games:
        candidate_name = game.get("name", "")
        game["score"] = compute_candidate_score(name, candidate_name)
        image_id = game.get("cover", {}).get("image_id")

        game["cover_url"] = get_image_url(image_id) if image_id else None
        game.pop("cover", None)

        for artwork in game.get("artworks", []):
            url = get_image_url(artwork.get("image_id"), "t_720p")
            if artwork.get("artwork_type", {}).get("id", "") == 3: game["key_art_with_logo"] = url
            if artwork.get("artwork_type", {}).get("id", "") == 2: game["key_art_without_logo"] = url
        game.pop("artworks", None)

        screenshots = []
        for screenshot in game.get("screenshots", []):
            url = get_image_url(screenshot.get("image_id"), "t_720p")
            screenshots.append(url)
        game["screenshots"] = screenshots

        for website in game.get("websites", []):
            website_type = website.get("type", {}).get("id", "")
            if website_type == PLAYSTATION_WEBSITE_TYPE:
                game["psn_website"] = website.get("url", "")
            if website_type == OFFICIAL_WEBSITE_TYPE:
                game["official_website"] = website.get("url", "")
            if website_type == COMMUNITY_WIKI_WEBSITE_TYPE:
                game["community_wiki_website"] = website.get("url", "")
        game.pop("websites", None)

        youtube_ids = []
        for video in game.get("videos", []):
            if video.get("video_id", ""):
                youtube_ids.append(video.get("video_id"))
        game["youtube_ids"] = youtube_ids
        game.pop("videos", None)

        developers = []
        publishers = []
        for involved_company in game.get("involved_companies", []):
            company_name = involved_company.get("company", {}).get("name", "")
            company_id = involved_company.get("company", {}).get("id", "")
            company = {"id": company_id, "name": company_name}
            if involved_company.get("developer", False): developers.append(company)
            if involved_company.get("publisher", False): publishers.append(company)
        game["developers"] = developers
        game["publishers"] = publishers
        game.pop("involved_companies", None)

        release_datetime = datetime.fromtimestamp(game.get("first_release_date", 0), tz=ZoneInfo("Europe/Paris"))
        release_date = release_datetime.strftime("%Y-%m-%d")
        game["release_date"] = release_date
        game.pop("first_release_date", None)

    igdb_games.sort(key=lambda x: x.get("score", 0), reverse=True)
    filtered_games = [g for g in igdb_games if g.get("score", 0) >= 50]

    return filtered_games
