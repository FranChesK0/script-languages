import sys

from PyQt5.QtWidgets import QApplication

from .main_window import MainWindow


def run() -> None:
    """Run the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


__all__ = ["run"]
