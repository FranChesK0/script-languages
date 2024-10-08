from typing import Dict, List

import requests

type Post = Dict[str, str | int]


def fetch_all_posts(url: str) -> List[Post]:
    resp = requests.get(url)

    if resp.status_code != 200:
        raise ConnectionError

    return resp.json()
