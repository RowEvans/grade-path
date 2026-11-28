import sys
import os
from platformdirs import user_data_dir
import sqlite3
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

GREEN, BORDER_GREEN = "#5FD877", "#3FAE58"
ICON_GREEN = "#78D88B"
CHARCOAL = "#333333"
SOFT_CHARCOAL = "#4d4d4d"

def find_path(file):
    return os.path.join(os.path.dirname(__file__), file)

class HomePage(QWidget):
    add_account = Signal()
    def __init__(self):
        super().__init__()
        self.header = Header()
        self.header.add_account.connect(self.add_account.emit)
        self.center = CenterPage()
        self.footer = Footer()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.center, 1)
        self.layout.addWidget(self.footer)

class accountDialog(QDialog):
    add_account = Signal()
    def __init__(self):
        super().__init__()

        #self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(300, 100)
        self.setStyleSheet(f"""
            QDialog {{
                background: {CHARCOAL};
                border-radius: 20px;
            }}
            QLabel {{
                color: white;
                font-size: 18px;
                font-weight: bold;
            }}
        """)

        layout = QVBoxLayout()

        new_account = QPushButton("+ Add new account")
        new_account.setStyleSheet(f"""
            background: {BORDER_GREEN};
            padding: 5px;
            border: 2px solid {ICON_GREEN};
            border-radius: 5px;
            color: white;
        """)
        new_account.clicked.connect(self.add_account.emit)
        new_account.clicked.connect(self.reject)

        self.con = sqlite3.connect(find_path("grades.db"))
        
        cur = self.con.cursor()
        els = cur.execute("SELECT username FROM accounts")

        for username in els:
            account = QLabel(username[0])
            account.setStyleSheet(f"""
                background: {CHARCOAL};
            """)
            layout.addWidget(account)

        layout.addWidget(new_account)
        self.setLayout(layout)

        

class Header(QWidget):
    refreshed = Signal()
    login_error = Signal()
    add_account = Signal()

    def __init__(self):
        super().__init__()

        self.setStyleSheet(f"""
            background-color: {GREEN};
            padding: 0px;
            height: auto;
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
            padding-left:6px;
            padding-bottom: 12px;
        """)

        self.icon_button = QPushButton("R")
        self.icon_button.setStyleSheet(f"""
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
        self.icon_button.clicked.connect(self.button_clicked)

        top_layout.addWidget(main_label)
        top_layout.addStretch(1)
        top_layout.addWidget(self.icon_button, alignment=Qt.AlignRight)

        self.header_layout.addLayout(top_layout)

    def button_clicked(self):
        dlg = accountDialog()
        dlg.add_account.connect(self.add_account.emit)
        dlg.adjustSize()
        center = self.window().geometry().center()
        dlg.move(center - dlg.rect().center())
        dlg.exec()



class CenterPage(QWidget):
    def __init__(self):
        super().__init__()

class Footer(QWidget):
    switch = Signal(int)
    def __init__(self):
        super().__init__()

        self.setStyleSheet(f"background: {CHARCOAL}")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)
        self.main_layout.addStretch()

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for i, item in enumerate(["home", "grade", "calendar"]):
            button = QPushButton()
            path = find_path("assets/" + item + ".png")
            active_path = find_path("assets/" + item + "-green.png")

            button.setIcon(QIcon(path))
            button.setIconSize(QSize(32, 32))
            button.setFixedSize(48, 48)
            button.setCheckable(True)
            button.setStyleSheet(f"""
                QPushButton{{
                    border: none;
                    background: transparent;
                }}

                QPushButton:checked {{
                    background: {SOFT_CHARCOAL};
                    border-radius: 15px;
                }}
            """)

            button.toggled.connect(
                lambda checked, b=button, n=path, a=active_path:
                b.setIcon(QIcon(a if checked else n))
            )
            if i == 0:
                button.setChecked(True)

            self.button_group.addButton(button, i)
            self.main_layout.addWidget(button)
            self.main_layout.addStretch()

        self.button_group.idClicked.connect(self.switch.emit)


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