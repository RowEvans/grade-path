import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from scraper import LoginFailedError
from platformdirs import user_data_dir
import keyring
import scraper
import sqlite3
import os

APP_DIR = user_data_dir("GradePath", "yourname")
os.makedirs(APP_DIR, exist_ok=True)

CHARCOAL = "#333333"
DEEP_CHARCOAL = "#222222"
SOFT_CHARCOAL = "#4d4d4d"
GREEN = "#5FD877"
DARK_GREEN = "#3FAE58"

def resource_path(relative_path):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        center_card = CenterCard()

        outer_layout = QHBoxLayout(self)
        outer_layout.addStretch()

        inner_layout = QVBoxLayout()
        inner_layout.addStretch()
        inner_layout.addWidget(center_card)
        inner_layout.addStretch()

        outer_layout.addLayout(inner_layout)
        outer_layout.addStretch()

    
class CenterCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"""
            width: 200px;
            background: {DEEP_CHARCOAL};
            border: 2px solid {CHARCOAL};
            border-radius: 10px;
            padding: 10px;
        """)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)

        title = QLabel("Login")
        title.setStyleSheet("""
            margin: 0;
            margin-bottom: 5px;
            font-size: 24px;
            font-weight: bold;
            border: none;
            background: transparent;
        """)


        username_frame = QFrame()
        username_frame.setStyleSheet(f"""
            padding: 1px;
            margin: 0px;
            background: transparent;
            border: 1px solid {CHARCOAL};
            border-radius: 10px;
        """)

        username_layout = QHBoxLayout(username_frame)
        user_icon = QPushButton()
        user_icon.setIcon(QIcon(resource_path("assets/user.png")))
        user_icon.setEnabled(False)
        user_icon.setStyleSheet("""
            background: transparent;
            border: none;
            width: 10px;
        """)

        username_label = QLineEdit(placeholderText="Username")
        username_label.setStyleSheet(f"""
            border: none;
            padding-left: 0px;
        """)

        username_layout.addWidget(user_icon)
        username_layout.addWidget(username_label)

        password_frame = QFrame()
        password_frame.setStyleSheet(f"""
            padding: 1px;
            margin: 0px;
            background: transparent;
            border: 1px solid {CHARCOAL};
            border-radius: 10px;
        """)

        password_layout = QHBoxLayout(password_frame)
        lock_icon = QPushButton()
        lock_icon.setIcon(QIcon(resource_path("assets/lock.png")))
        lock_icon.setEnabled(False)
        lock_icon.setStyleSheet("""
            background: transparent;
            border: none;
            width: 10px;
        """)

        password_label = QLineEdit(placeholderText="Password")
        password_label.setEchoMode(QLineEdit.EchoMode.Password)
        password_label.setStyleSheet(f"""
            border: none;
            padding-left: 0px;
        """)

        password_layout.addWidget(lock_icon)
        password_layout.addWidget(password_label)

        login_frame = QFrame()
        login_frame.setStyleSheet(f"""
            background: {GREEN};
            padding: 0;
        """)

        login_layout = QHBoxLayout(login_frame)
        self.login_button = QPushButton("Login")
        self.login_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.login_button.clicked.connect(self.loading)
        self.login_button.setStyleSheet(f"""
            QPushButton{{
                border: none;
                padding: 0;
                font-weight: bold;
                margin-top: 10px;
            }}
            
            QPushButton:disabled {{
                font-weight: 400;
                color: white;
            }}
        """)
        self.spinner = QLabel()
        self.movie = QMovie(resource_path("assets/loading.gif"))
        self.spinner.setMovie(self.movie)
        self.spinner.setFixedSize(24, 24)
        self.spinner.setVisible(False)
        self.spinner.setStyleSheet("""
            background: transparent;
            border: none;
        """)
        login_layout.addWidget(self.login_button)
        login_layout.addWidget(self.spinner)
        login_layout.addStretch()

        self.main_layout.addWidget(title)
        self.main_layout.addWidget(username_frame)
        self.main_layout.addWidget(password_frame)
        self.main_layout.addWidget(login_frame)

    def loading(self):
        self.login_button.setEnabled(False)
        self.spinner.setVisible(True)
        self.movie.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.setWindowTitle("LoginPage")
        self.resize(500, 600)
        self.move(QPoint(1280-550, 100))
        

        central_widget = LoginPage()
        self.setCentralWidget(central_widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    
    sys.exit(app.exec())