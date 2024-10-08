import dataclasses


@dataclasses.dataclass(frozen=True)
class Config:
    API_URL: str = "https://jsonplaceholder.typicode.com/posts"
    DATABASE_FILE_PATH: str = "./db/posts.db"

    def __new__(cls) -> "Config":
        if not hasattr(cls, "_instance"):
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance


CONFIG: Config = Config()
