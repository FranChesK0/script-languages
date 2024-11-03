from typing import Dict, NamedTuple


class Post(NamedTuple):
    id: int
    user_id: int
    title: str
    body: str

    def __repr__(self) -> str:
        return f"<Post:{self.id=},{self.user_id=},{self.title=},{self.body=}>"

    def __str__(self) -> str:
        return self.__repr__()


def to_model(value: Dict[str, str | int]) -> Post:
    return Post(
        id=int(value["id"]),
        user_id=int(value["user_id"]),
        title=str(value["title"]),
        body=str(value["body"]),
    )
