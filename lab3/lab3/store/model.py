from typing import Dict, NamedTuple


class Post(NamedTuple):
    id: int
    user_id: int
    title: str
    body: str

    def __repr__(self) -> str:
        return f"Post<{self.id}>:\n\t- user_id={self.user_id}\n\t- title={self.title}\n\t- body:\n{self.body}\n"

    def __str__(self) -> str:
        return self.__repr__()


def to_model(value: Dict[str, str | int]) -> Post:
    return Post(
        id=int(value["id"]),
        user_id=int(value["userId"]),
        title=str(value["title"]),
        body=str(value["body"]),
    )
