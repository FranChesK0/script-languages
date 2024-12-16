from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.

    Attributes:
        ENV (str): The environment to run the application in.
        BASE_URL (str): The base URL for the application.
        DATABASE_CONNECTION (str): The database connection string.
    """

    ENV: str = "dev"
    BASE_URL: str = "https://jsonplaceholder.typicode.com"
    DATABASE_CONNECTION: str = "sqlite+aiosqlite:///:memory:"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
