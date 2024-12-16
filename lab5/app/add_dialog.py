import asyncio
from typing import Any
from collections.abc import Callable, Coroutine

import PyQt5.QtWidgets as widgets

from store import PostRepository
from schemas import PostAddSchema


class AddDialog(widgets.QWidget):
    """Dialog widget for adding a post."""

    def __init__(self, update_function: Callable[[], Coroutine[Any, Any, None]]) -> None:
        super().__init__()
        self.update_function = update_function

        self.setWindowTitle("Add post")
        self.setGeometry(400, 400, 300, 200)

        self.user_id_input = widgets.QLineEdit(self)
        self.title_input = widgets.QLineEdit(self)
        self.body_input = widgets.QLineEdit(self)

        add_button = widgets.QPushButton("Add", self)
        add_button.clicked.connect(self.add_post_callback)

        layout = widgets.QFormLayout()
        layout.addRow("User ID:", self.user_id_input)
        layout.addRow("Title:", self.title_input)
        layout.addRow("Body:", self.body_input)
        layout.addWidget(add_button)

        self.setLayout(layout)

    async def add_post(self) -> None:
        """Add a post to the database."""
        post = PostAddSchema(
            user_id=int(self.user_id_input.text()),
            title=self.title_input.text(),
            body=self.body_input.text(),
        )
        await PostRepository.add_one(post)
        await self.update_function()

    def add_post_callback(self) -> None:
        """Callback function for the add button."""
        try:
            loop = asyncio.get_running_loop()
            loop.run_until_complete(self.add_post())
        except RuntimeError:
            asyncio.run(self.add_post())
        finally:
            self.user_id_input.clear()
            self.title_input.clear()
            self.body_input.clear()
            self.close()
