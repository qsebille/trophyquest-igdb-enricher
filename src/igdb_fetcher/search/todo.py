import os
from typing import Any

from requests import post

from igdb_fetcher.search.constants import IGDB_BASE
from igdb_fetcher.search.token import get_igdb_token


def fetch_artwork_types(limit: int) -> list[dict[str, Any]]:
    url = f"{IGDB_BASE}/website_types"
    query = f'''
        fields type;
        limit {limit};
    '''
    headers = {
        "Client-ID": os.environ["TWITCH_CLIENT_ID"],
        "Authorization": f"Bearer {get_igdb_token()}",
        "Accept": "application/json",
    }
    response = post(url, headers=headers, data=query, timeout=15)

    if not response.ok:
        raise RuntimeError(f"IGDB error {response.status_code}: {response.text}\nQuery:\n{query}")

    return response.json()
