import sys

import pandas as pd
import PyQt5.QtWidgets as widgets
import seaborn as sns
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure


class MainWindow(widgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.data: pd.DataFrame | None = None

        self.setWindowTitle("Visualizer")
        self.setGeometry(100, 100, 800, 600)

        load_button = widgets.QPushButton("Load CSV file", self)
        load_button.clicked.connect(self.load_csv)

        self.status_label = widgets.QLabel("Data is not loaded")

        self.plot_type = widgets.QComboBox(self)
        self.plot_type.addItems(["Linear", "Hist", "Pie"])

        draw_button = widgets.QPushButton("Draw plot", self)
        draw_button.clicked.connect(self.draw_plot)

        self.new_data_input = widgets.QLineEdit(self)
        self.new_data_input.setPlaceholderText("Input new values...")

        update_button = widgets.QPushButton("Update data", self)
        update_button.clicked.connect(self.update_data)

        data_layout = widgets.QHBoxLayout()
        data_layout.addWidget(self.new_data_input)
        data_layout.addWidget(update_button)

        self.canvas = Canvas(Figure(figsize=(5, 3)))

        layout = widgets.QVBoxLayout()
        layout.addWidget(load_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.plot_type)
        layout.addWidget(draw_button)
        layout.addLayout(data_layout)
        layout.addWidget(self.canvas)

        main_widget = widgets.QWidget(self)
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)

        self.ax = self.canvas.figure.add_subplot(111)

    def load_csv(self) -> None:
        options = widgets.QFileDialog.Options()
        path, _ = widgets.QFileDialog.getOpenFileName(
            self,
            "Choose CSV file",
            "",
            "CSV Files (*.csv);;All Files (*)",
            options=options,
        )
        if path:
            self.data = pd.read_csv(path)
            self.update_statistic()

    def update_statistic(self) -> None:
        if self.data is None:
            return
        stats = (
            "Statistic:\n"
            f"Lines number: {self.data.shape[0]}\n"
            f"Columns number: {self.data.shape[1]}"
        )
        for column in self.data.columns:
            if pd.api.types.is_numeric_dtype(self.data[column]):
                stats += f"\n{column}: Min: {self.data[column].min()}, Max: {self.data[column].max()}"
        self.status_label.setText(stats)

    def draw_plot(self) -> None:
        if self.data is None:
            return

        self.ax.clear()
        match self.plot_type.currentText():
            case "Linear":
                sns.lineplot(ax=self.ax, data=self.data, x="Date", y="Value1")
                title = "Linear plot: Date[Value1]"
                x_label = "Date"
                y_label = "Value1"
                self.ax.set_aspect("auto")
            case "Hist":
                sns.barplot(ax=self.ax, data=self.data, x="Date", y="Value2")
                title = "Hist: Date[Value2]"
                x_label = "Date"
                y_label = "Value2"
                self.ax.set_aspect("auto")
            case "Pie":
                self.data["Category"].value_counts().plot.pie(
                    ax=self.ax, autopct="%1.1f%%"
                )
                title = "Pie:"
                x_label = ""
                y_label = ""
            case _:
                return

        self.ax.set_title(title)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.canvas.draw()
        self.update_statistic()

    def update_data(self) -> None:
        if self.data is None:
            self.status_label.setText("Load CSV data before updating data")
            return

        input_format_msg = "Input data in CSV format"
        new_data = self.new_data_input.text().strip()
        if not new_data:
            self.status_label.setText(input_format_msg)
            return

        new_row = new_data.split(",")
        if len(new_row) != 5:
            self.status_label.setText(input_format_msg)
            return

        date = new_row[0].strip()
        category = new_row[1].strip()
        try:
            value1 = int(new_row[2])
        except ValueError:
            self.status_label.setText("Value1 should be an integer number")
            return
        try:
            value2 = float(new_row[3])
        except ValueError:
            self.status_label.setText("Value2 should be a float number")
            return
        if new_row[4].strip() not in ("True", "False"):
            self.status_label.setText("BooleanFlag should be 'True' or 'False'")
            return
        bool_flag = new_row[4].strip() == "True"

        self.data = pd.concat(
            [
                self.data,
                pd.DataFrame(
                    [
                        {
                            "Date": date,
                            "Category": category,
                            "Value1": value1,
                            "Value2": value2,
                            "BooleanFlag": bool_flag,
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )
        self.update_statistic()
        self.status_label.setText("New values added successfully")


if __name__ == "__main__":
    app = widgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
