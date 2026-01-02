import json

from dotenv import load_dotenv

from igdb_fetcher.search.games import search_games
from igdb_fetcher.search.todo import fetch_artwork_types


def main():
    load_dotenv()
    candidates = search_games("outer wilds", limit=20)
    artwork_types = fetch_artwork_types(20)
    print(json.dumps(candidates, indent=2, ensure_ascii=False))
    # print(json.dumps(artwork_types, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
