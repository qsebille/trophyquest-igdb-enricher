import json

from dotenv import load_dotenv

from igdb_fetcher.client.games import search_games


def main():
    load_dotenv()
    candidates = search_games("Dragon age: The Veilguard", limit=20)
    print(json.dumps(candidates, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
