import sys
from collections.abc import Callable

import PyQt5.QtSql as sql
import PyQt5.QtCore as core
import PyQt5.QtWidgets as widgets


class MainApp(widgets.QMainWindow):
    def __init__(self, database_path: str) -> None:
        super().__init__()

        self.setWindowTitle("Posts")
        self.setGeometry(300, 300, 800, 600)

        self.main_widget = widgets.QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.search_box = widgets.QLineEdit(self)
        self.search_box.setPlaceholderText("Find by title")
        self.search_box.textChanged.connect(self.filter_posts)

        self.add_button = widgets.QPushButton("Add", self)
        self.add_button.clicked.connect(self.add_post_callback)
        self.delete_button = widgets.QPushButton("Delete", self)
        self.delete_button.clicked.connect(self.delete_post_callback)

        button_layout = widgets.QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)

        layout = widgets.QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.search_box)

        self.table = widgets.QTableView(self)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        self.main_widget.setLayout(layout)

        self.db = sql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(database_path)
        if not self.db.open():
            raise ConnectionError("Could not to connect to database")

        self.model = sql.QSqlTableModel(self)
        self.model.setTable("posts")
        self.model.select()

        self.table.setModel(self.model)
        self.table.verticalHeader().setVisible(False)

    def load_posts(self) -> None:
        self.model.select()

    def filter_posts(self) -> None:
        filter_text = self.search_box.text()
        self.model.setFilter(f"title LIKE '%{filter_text}%'")
        self.model.select()

    def add_post_callback(self) -> None:
        AddDialog(self.add_post).show()

    def delete_post_callback(self) -> None:
        index = self.table.currentIndex()
        if index.isValid():
            record_id = self.model.index(index.row(), 0).data()
            reply = widgets.QMessageBox.question(
                self,
                "Delete",
                "Are you shure to delete post?",
                widgets.QMessageBox.Yes | widgets.QMessageBox.No,
                widgets.QMessageBox.No,
            )
            if reply == widgets.QMessageBox.Yes:
                query = sql.QSqlQuery()
                query.prepare("DELETE FROM posts WHERE id = ?")
                query.addBindValue(record_id)
                if query.exec_():
                    self.load_posts()
                else:
                    widgets.QMessageBox.warning(
                        self, "Error", "Could not delete post from database."
                    )
        else:
            widgets.QMessageBox.warning(self, "Error", "Choose post to delete")

    def add_post(
        self, dialog_window: widgets.QWidget, user_id: str, title: str, body: str
    ) -> None:
        query = sql.QSqlQuery()
        query.prepare("INSERT INTO posts (user_id, title, body) VALUES (?, ?, ?)")
        query.addBindValue(user_id)
        query.addBindValue(title)
        query.addBindValue(body)

        if query.exec_():
            self.load_posts()
            dialog_window.close()
        else:
            widgets.QMessageBox(self, "Error", "Could not add post to database.")


class AddDialog(widgets.QWidget):
    def __init__(
        self, add_post: Callable[[widgets.QWidget, str, str, str], None]
    ) -> None:
        super().__init__()

        self.setWindowTitle("Add post")
        self.setGeometry(400, 400, 300, 200)

        user_id_input = widgets.QLineEdit(self)
        title_input = widgets.QLineEdit(self)
        body_input = widgets.QLineEdit(self)

        add_button = widgets.QPushButton("Add", self)
        add_button.clicked.connect(
            lambda: add_post(
                self, user_id_input.text(), title_input.text(), body_input.text()
            )
        )

        layout = widgets.QFormLayout()
        layout.addRow("User ID:", user_id_input)
        layout.addRow("Title:", title_input)
        layout.addRow("Body:", body_input)
        layout.addWidget(add_button)

        self.setLayout(layout)


if __name__ == "__main__":
    app = widgets.QApplication(sys.argv)
    window = MainApp("posts.db")
    window.show()
    sys.exit(app.exec_())
