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
        exc_msg = ""
        if exc_type is not None:
            exc_msg += f" type: {exc_type.__name__}"
        if exc_value is not None:
            exc_msg += f" value: {exc_value}"
        if traceback is not None:
            exc_msg += f" traceback: {traceback}"
        if exc_msg != "":
            exc_msg = f" with exception: {exc_msg}"
        logger.info(f"Closing session for {self._session._base_url}{exc_msg}.")
        if self._session is not None:
            await self._session.close()
