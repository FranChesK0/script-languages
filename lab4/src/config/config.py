import dataclasses
from typing import Final


@dataclasses.dataclass(frozen=True)
class Config:
    API_URL: Final[str] = "https://jsonplaceholder.typicode.com/posts"
    DATABASE_FILE_PATH: Final[str] = "./db/posts.db"

    def __new__(cls) -> "Config":
        if not hasattr(cls, "_instance"):
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance


config = Config()
