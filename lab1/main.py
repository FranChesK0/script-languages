from typing import Dict, List

import requests

URL = "https://jsonplaceholder.typicode.com/"
HEADERS = {"Content-Type": "application/json; charset=UTF-8"}
type Post = Dict[str, str | int]


def post_to_string(post: Post) -> str:
    sep = "-----------------------"
    return f"{sep}\nuserId: {post["userId"]}\nid: {post["id"]}\ntitle: {post["title"]}\nbody: {post["body"]}\n"


def fetch_all_posts() -> List[Post]:
    resp = requests.get(URL + "posts")

    if resp.status_code != 200:
        raise ConnectionError

    return resp.json()


def filter_posts(posts: List[Post]) -> List[Post]:
    filtered: List[Post] = []
    for post in posts:
        if post["userId"] % 2 == 0:
            filtered.append(post)
    return filtered


def create_post(post: Post) -> Post:
    resp = requests.post(URL + "posts", data=post, params=HEADERS)

    if resp.status_code != 201:
        raise ConnectionError

    return resp.json()


def update_title(post_id: int, title: str) -> Post:
    resp = requests.put(URL + f"posts/{post_id}", json={"title": title}, params=HEADERS)

    if resp.status_code != 200:
        raise ConnectionError

    return resp.json()


def main() -> None:
    print("1. List of posts:")
    for post in filter_posts(fetch_all_posts()):
        print(post, end="\n\n")

    print("2. Creating new post")
    print("Created post:")
    post = create_post({"userId": 200, "title": "Тестовый пост", "body": "Empty body"})
    print(post, end="\n\n")

    print("3. Update title of the created post")
    print("Updated post:")
    print(update_title(45, "Обновлённый пост"))


if __name__ == "__main__":
    main()
