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

class LoadingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.spinner = QLabel()
        self.movie = QMovie(resource_path("assets/loading.gif"))
        self.movie.setScaledSize(QSize(24, 24))
        self.spinner.setMovie(self.movie)

        text = QLabel("Logging in...")

        layout = QVBoxLayout(self)
        layout.addStretch()
        layout.addWidget(self.spinner, alignment=Qt.AlignCenter)
        layout.addWidget(text, alignment=Qt.AlignCenter)
        layout.addStretch()

    def showEvent(self, event):
        self.movie.start()
        super().showEvent(event)

    def hideEvent(self, event):
        self.movie.stop()
        super().hideEvent(event)

class LoginPage(QWidget):
    submitted = Signal(str, str)

    def __init__(self):
        super().__init__()

        self.center_card = CenterCard()
        self.center_card.login_button.clicked.connect(self.submit)

        outer_layout = QHBoxLayout(self)
        outer_layout.addStretch()

        inner_layout = QVBoxLayout()
        inner_layout.addStretch()
        inner_layout.addWidget(self.center_card)
        inner_layout.addStretch()

        outer_layout.addLayout(inner_layout)
        outer_layout.addStretch()

    def submit(self):
        self.submitted.emit(
            self.center_card.username_label.text(),
            self.center_card.password_label.text()
        )

    def show_error(self, msg):
        self.center_card.error_label.setText(msg)
        self.center_card.error_label.setVisible(True)
        self.center_card.login_button.setEnabled(True)

    
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

        self.username_label = QLineEdit(placeholderText="Username")
        self.username_label.setStyleSheet(f"""
            border: none;
            padding-left: 0px;
        """)

        username_layout.addWidget(user_icon)
        username_layout.addWidget(self.username_label)

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

        self.password_label = QLineEdit(placeholderText="Password")
        self.password_label.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_label.setStyleSheet(f"""
            border: none;
            padding-left: 0px;
        """)

        password_layout.addWidget(lock_icon)
        password_layout.addWidget(self.password_label)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setVisible(False)

        self.login_button = QPushButton("Login")
        self.login_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.login_button.setStyleSheet(f"""
            QPushButton{{
                background: {GREEN};
                color: white;
                border: none;
                padding: 10px;
                font-weight: 700;
                margin-top: 10px;
            }}
            
            QPushButton:disabled {{
                background: {DARK_GREEN};
                font-weight: 400;
                color: white;
            }}
        """)

        self.main_layout.addWidget(title)
        self.main_layout.addWidget(username_frame)
        self.main_layout.addWidget(password_frame)
        self.main_layout.addWidget(self.error_label)
        self.main_layout.addWidget(self.login_button)


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