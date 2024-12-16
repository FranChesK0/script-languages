import queue
import asyncio
import threading
from collections.abc import Callable, AsyncGenerator

from PyQt5.QtWidgets import QProgressBar

from core import settings
from store import PostRepository
from schemas import PostAddSchema
from http_client import JPHTTPClient

posts_queue = queue.Queue()


class FetchProgressBar(QProgressBar):
    """
    A progress bar that fetches posts from the JSONPlaceholder API and adds them to the database.
    """

    def __init__(self, finished_func: Callable[[], None]) -> None:
        super().__init__()

        self.finished_func = finished_func

    async def posts_generator(
        self,
        time_sleep: float = 0,
    ) -> AsyncGenerator[PostAddSchema, None]:
        """
        Generate posts from the JSONPlaceholder API.

        Args:
            time_sleep (float, optional): The amount of time to sleep after adding the post. Defaults to 0.

        Yields:
            PostAddSchema: The post to add to the database.
        """
        async with JPHTTPClient(settings.BASE_URL) as jp_client:
            posts = await jp_client.fetch_posts()
        self.setRange(0, len(posts))
        self.setValue(0)
        for post in posts:
            yield post
            await asyncio.sleep(time_sleep)

    async def posts_handler(self, post: PostAddSchema, time_sleep: float = 0) -> None:
        """
        Add a post to the database.

        Args:
            post (PostAddSchema): The post to add to the database.
            time_sleep (float, optional): The amount of time to sleep after adding the post. Defaults to 0.
        """
        await PostRepository.lazy_add(post)
        self.setValue(self.value() + 1)
        await asyncio.sleep(time_sleep)

    async def posts_producer(self) -> None:
        """Produce posts and add them to the queue."""
        async for post in self.posts_generator(0.05):
            posts_queue.put(post)

    async def posts_consumer(self) -> None:
        """Consume posts from the queue and add them to the database."""
        while True:
            try:
                post: PostAddSchema = posts_queue.get(timeout=0.5)
                await self.posts_handler(post, 0.05)
                posts_queue.task_done()
            except queue.Empty:
                break

    def get_posts_producer_thread(self) -> threading.Thread:
        """Get the posts producer thread."""

        def producer_sync() -> None:
            try:
                loop = asyncio.get_running_loop()
                loop.run_until_complete(self.posts_producer())
            except RuntimeError:
                asyncio.run(self.posts_producer())

        return threading.Thread(target=producer_sync, name="posts_producer", daemon=True)

    def get_posts_consumer_thread(self) -> threading.Thread:
        """Get the posts consumer thread."""

        def consumer_sync() -> None:
            try:
                loop = asyncio.get_running_loop()
                loop.run_until_complete(self.posts_consumer())
            except RuntimeError:
                asyncio.run(self.posts_consumer())
            finally:
                self.finished_func()

        return threading.Thread(target=consumer_sync, name="posts_consumer", daemon=True)
