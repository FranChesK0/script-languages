import asyncio

from loguru import logger
from aiohttp import ClientSession


class HTTPClient:
    """
    Base class for HTTP clients.

    Args:
        base_url (str): The base URL of the HTTP client.
        headers (dict[str, Any] | None, optional): Additional headers to include in requests.
    """

    def __init__(self, base_url: str, headers: dict[str, str] | None = None) -> None:
        self._session = ClientSession(base_url=base_url, headers=headers)

    def __del__(self) -> None:
        logger.info(f"Closing session for {self._session._base_url}.")
        asyncio.ensure_future(self._session.close())
