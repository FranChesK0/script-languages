import asyncio

import PyQt5.QtWidgets as widgets

from store import PostRepository

from .add_dialog import AddDialog
from .fetch_posts import FetchProgressBar


class MainWindow(widgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Posts")
        self.setGeometry(300, 300, 800, 600)

        self.table = widgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "User ID", "Title", "Body"])

        self.search_input = widgets.QLineEdit(self)
        self.search_input.setPlaceholderText("Search by title")
        self.search_input.textChanged.connect(self.filter_posts_callback)

        fetch_button = widgets.QPushButton("Load Posts", self)
        fetch_button.clicked.connect(self.fetch_posts_callback)

        add_button = widgets.QPushButton("Add Post", self)
        add_button.clicked.connect(self.add_post_callback)

        delete_button = widgets.QPushButton("Delete Post", self)
        delete_button.clicked.connect(self.delete_post_callback)

        button_layout = widgets.QHBoxLayout()
        button_layout.addWidget(fetch_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)

        self.progress_bar = FetchProgressBar(self.fetch_finished)

        layout = widgets.QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.search_input)
        layout.addWidget(self.table)
        layout.addWidget(self.progress_bar)

        main_widget = widgets.QWidget(self)
        self.setCentralWidget(main_widget)
        main_widget.setLayout(layout)

        asyncio.run(self.load_posts())

        self.add_dialog = AddDialog(self.load_posts)

    async def load_posts(self) -> None:
        """Load all posts from the database and display them in the table."""
        posts = await PostRepository.find_all()
        self.table.setRowCount(len(posts))

        for row, post in enumerate(posts):
            self.table.setItem(row, 0, widgets.QTableWidgetItem(str(post.id)))
            self.table.setItem(row, 1, widgets.QTableWidgetItem(str(post.user_id)))
            self.table.setItem(row, 2, widgets.QTableWidgetItem(post.title))
            self.table.setItem(row, 3, widgets.QTableWidgetItem(post.body))

    async def filter_post(self) -> None:
        """Filter posts by title and display them in the table."""
        filter_title = self.search_input.text()
        if filter_title == "":
            await self.load_posts()
            return

        posts = await PostRepository.find_by_title(filter_title)
        self.table.setRowCount(len(posts))

        for row, post in enumerate(posts):
            self.table.setItem(row, 0, widgets.QTableWidgetItem(str(post.id)))
            self.table.setItem(row, 1, widgets.QTableWidgetItem(str(post.user_id)))
            self.table.setItem(row, 2, widgets.QTableWidgetItem(post.title))
            self.table.setItem(row, 3, widgets.QTableWidgetItem(post.body))

    def fetch_finished(self) -> None:
        """Update the progress bar when the posts producer thread finishes."""
        self.progress_bar.setValue(0)
        try:
            loop = asyncio.get_running_loop()
            loop.run_until_complete(self.load_posts())
        except RuntimeError:
            asyncio.run(self.load_posts())

    async def delete_post(self, post_id: int) -> None:
        """
        Delete a post from the database.

        Args:
            post_id (int): The ID of the post to delete.
        """
        await PostRepository.delete_one(post_id)
        await self.load_posts()

    def filter_posts_callback(self) -> None:
        """Filter posts by title and display them in the table."""
        try:
            loop = asyncio.get_running_loop()
            loop.run_until_complete(self.filter_post())
        except RuntimeError:
            asyncio.run(self.filter_post())

    def add_post_callback(self) -> None:
        """Open the add post dialog and reload the posts when the dialog is closed."""
        self.add_dialog.show()

    def delete_post_callback(self) -> None:
        """Delete the selected post from the database."""
        post_id = self.table.item(self.table.currentRow(), 0)
        if post_id == None:
            widgets.QMessageBox.warning(self, "Error", "No post selected")
            return

        try:
            post_id = int(post_id.text())
        except ValueError:
            widgets.QMessageBox.warning(self, "Error", "Invalid post ID")
            return

        reply = widgets.QMessageBox.question(
            self,
            "Delete post",
            f"Are you sure you want to delete post {post_id}?",
            widgets.QMessageBox.Yes | widgets.QMessageBox.No,
            widgets.QMessageBox.No,
        )

        if reply != widgets.QMessageBox.Yes:
            return

        try:
            loop = asyncio.get_running_loop()
            loop.run_until_complete(self.delete_post(post_id))
        except RuntimeError:
            asyncio.run(self.delete_post(post_id))

    def fetch_posts_callback(self) -> None:
        """Start the posts producer and consumer threads."""
        self.progress_bar.get_posts_producer_thread().start()
        self.progress_bar.get_posts_consumer_thread().start()
