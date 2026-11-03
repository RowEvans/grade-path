import sys
import os
from platformdirs import user_data_dir
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *


APP_DIR = user_data_dir("GradePath", "yourname")
os.makedirs(APP_DIR, exist_ok=True)
DB_FILE = os.path.join(APP_DIR, "grades.db")

GREEN, BORDER_GREEN = "#5FD877", "#3FAE58"
ICON_GREEN = "#78D88B"
CHARCOAL = "#333333"

def resource_path(relative_path):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.header = Header()
        self.center = CenterPage()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.center)


class Header(QWidget):
    refreshed = Signal()
    login_error = Signal()

    def __init__(self):
        super().__init__()

        self.setStyleSheet(f"""
            background-color: {GREEN};
            height: auto;
            padding: 0px;
            border-radius: 5px;
        """)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.header_layout = QVBoxLayout(self)
        self.header_layout.setContentsMargins(10, 10, 10, 10)
        self.header_layout.setSpacing(8)

    #   now the main text
        top_layout = QHBoxLayout()

        main_label = QLabel("Hi, Rowan")
        main_label.setStyleSheet(f"""
            color: white;
            font-size: 32px;
            font-weight:bold; 
            padding-bottom: 12px;
            padding-left:6px;
        """)

        self.refresh_button = QPushButton("R")
        self.refresh_button.setStyleSheet(f"""
            color: white;
            font-weight: 700;
            font-size: 18px;
            background-color: {ICON_GREEN};
            border: 2px solid {BORDER_GREEN};
            border-radius: 20px;
            width: 40px;
            height: auto;
            text-align: center;
        """)

        top_layout.addWidget(main_label)
        top_layout.addStretch(1)
        top_layout.addWidget(self.refresh_button, alignment=Qt.AlignRight)

        self.header_layout.addLayout(top_layout)

class CenterPage(QWidget):
    def __init__(self):
        super().__init__()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Home Page")
        self.resize(500, 600)
        self.move(QPoint(1280-550, 100))

        central_widget = HomePage()
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    
    sys.exit(app.exec())