import os
import re

import unicodedata
from requests import post

from igdb_fetcher.client.constants import *
from igdb_fetcher.client.token import get_igdb_token


def _normalize_game_name(name: str) -> str:
    s = name.lower()

    # Unicode normalization
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))

    # Alphanumeric normalization
    s = re.compile(r"[^a-z0-9]+").sub(" ", s)

    # Trim + collapse whitespace
    s = re.compile(r"\s+").sub(" ", s).strip()
    return s


def post_search_games_query(game_title):
    token = get_igdb_token()
    client_id = os.environ["TWITCH_CLIENT_ID"]

    url = f"{IGDB_BASE}/games"
    query = f'''
        search "{_normalize_game_name(game_title)}";
        fields id, name, genres.name, themes.name, collections.name,
            videos.video_id,
            websites.url, websites.type.id,
            cover.image_id, screenshots.image_id,
            artworks.image_id, artworks.artwork_type.id,
            involved_companies.developer, involved_companies.publisher,
            involved_companies.company.name, involved_companies.company.country,
            first_release_date, summary;
        where version_parent = null & platforms = ({PS3_PLATFORM_ID}, {PS4_PLATFORM_ID}, {PS5_PLATFORM_ID});
        limit 5;
        '''

    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    response = post(url, headers=headers, data=query, timeout=15)

    if not response.ok:
        raise RuntimeError(f"IGDB error {response.status_code}: {response.text}\nQuery:\n{query}")

    return response.json()
