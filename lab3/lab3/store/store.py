import sqlite3
from typing import Any, List, Tuple

from .model import Post


class Store:
    def __init__(self, file_name: str) -> None:
        self.__file_name = file_name

    def create_db(self) -> None:
        conn, cursor = self.__connect()
        cursor.execute(
            "CREATE TABLE posts ("
            "   id INT NOT NULL,"
            "   user_id INT NOT NULL,"
            "   title VARCHAR NOT NULL,"
            "   body VARCHAR NOT NULL,"
            "   CONSTRAINT pk_posts_id PRIMARY KEY (id)"
            ");"
        )
        conn.commit()
        conn.close()

    def insert_post(self, post: Post) -> None:
        conn, cursor = self.__connect()
        cursor.execute(
            "INSERT INTO posts (id, user_id, title, body) VALUES (?, ?, ?, ?)",
            (post.id, post.user_id, post.title, post.body),
        )
        conn.commit()
        conn.close()

    def get_user_posts(self, user_id: int) -> List[Post]:
        conn, cursor = self.__connect()
        posts = cursor.execute(
            "SELECT * FROM posts WHERE user_id = ?",
            (user_id,),
        ).fetchall()
        conn.close()
        return list(map(self.__to_post, posts))

    def __connect(self) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
        conn = sqlite3.connect(self.__file_name)
        return conn, conn.cursor()

    @staticmethod
    def __to_post(post: Any) -> Post:
        return Post(*post)
