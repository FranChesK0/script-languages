from loguru import logger

from schemas import PostAddSchema

from .base import HTTPClient


class JPHTTPClient(HTTPClient):
    """
    A class representing a JSONPlaceholder HTTP client.

    Args:
        base_url (str): The base URL of the JSONPlaceholder API.

    Methods:
        fetch_posts: Fetches posts from the JSONPlaceholder API.
    """

    def __init__(self, base_url: str) -> None:
        super().__init__(base_url)

    async def fetch_posts(self) -> list[PostAddSchema]:
        """
        Fetches posts from the JSONPlaceholder API.

        Returns:
            A list of PostAddSchema objects representing the fetched posts.
        """
        logger.info(f"Fetching posts from {self._session._base_url}/posts.")
        async with self._session.get("/posts") as response:
            result = await response.json()
        logger.info(f"Fetched {len(result)} posts.")
        return [
            PostAddSchema(user_id=post["userId"], title=post["title"], body=post["body"])
            for post in result
        ]
