from typing import Any, Dict, List

import requests

type Post = Dict[str, str | int]


def fetch_all_posts(url: str) -> List[Post]:
    resp = requests.get(url)
    if resp.status_code != 200:
        raise ConnectionError
    return [_to_post(d) for d in resp.json()]


def _to_post(d: Dict[Any, Any]) -> Post:
    return {
        "id": int(d["id"]),
        "user_id": int(d["user_id"]),
        "title": str(d["title"]),
        "body": str(d["body"]),
    }
