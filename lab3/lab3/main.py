from api import fetch_all_posts
from config import CONFIG
from store import Store, to_model


def main() -> None:
    store = Store(CONFIG.DATABASE_FILE_PATH)
    store.create_db()

    posts = fetch_all_posts(CONFIG.API_URL)

    for post in posts:
        store.insert_post(to_model(post))

    print("All posts of user 1:")
    for post in store.get_user_posts(1):
        print(post)


if __name__ == "__main__":
    main()
