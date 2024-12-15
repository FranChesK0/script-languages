from types import TracebackType
from typing import Self

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

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        logger.info(f"Closing session for {self._session._base_url}.")
        logger.debug(f"Exception: {exc_type}, {exc_value}, {traceback}")
        if self._session is not None:
            await self._session.close()
