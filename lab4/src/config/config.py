import dataclasses
from typing import Final


@dataclasses.dataclass(frozen=True)
class Config:
    api_url: Final[str] = "https://jsonplaceholder.typicode.com/posts"
    database_file_path: Final[str] = "./db/posts.db"

    def __new__(cls) -> "Config":
        if not hasattr(cls, "_instance"):
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance


config = Config()
