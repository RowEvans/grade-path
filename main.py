import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "grades.db")

# COLORS
GREEN, BORDER_GREEN = "#5FD877", "#3FAE58"
BLUE, BORDER_BLUE = "#4C8DF0", "#2E6FD1"
ORANGE, BORDER_ORANGE = "#F0A94C", "#D18A2E"
RED, BORDER_RED = "#E0554F", "#C0362F"

class Header(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: green")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.header_layout = QVBoxLayout(self)
        self.header_layout.setContentsMargins(10, 10, 10, 10)
        self.header_layout.setSpacing(8)

    #   now the main text
        top_layout = QHBoxLayout()

        main_label = QLabel("Grades")
        main_label.setStyleSheet("color: white; font-size: 32px; font-weight:bold; border: 2px;")

        refresh_button = QPushButton("Refresh")

        top_layout.addWidget(main_label)
        top_layout.addStretch(1)
        top_layout.addWidget(refresh_button, alignment=Qt.AlignRight)

    #   now the nav bar
        nav_bar = QHBoxLayout()
        for name in ["Q1", "Q2", "Q3", "Q4"]:
            nav_button = QPushButton(name)
            nav_button.setStyleSheet("color: white; background: gray; border: none;")
            nav_bar.addWidget(nav_button)

        self.header_layout.addLayout(top_layout)
        self.header_layout.addLayout(nav_bar)



class Classes(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("padding: 10px;")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)

        self.con = sqlite3.connect(DB_FILE)

        cur = self.con.cursor()
        els = cur.execute("SELECT name, grade, class_id, period FROM grades ORDER BY period")


        # now for one class
        for item in els:
            row = QFrame()
            row.setStyleSheet("""
                border: none;
                border-radius: 10px;
                background: #333333;
            """)
            row.setAttribute(Qt.WA_StyledBackground, True)

            layout = QHBoxLayout(row)
            layout.setContentsMargins(0, 0, 0, 8)

            title_layout = QVBoxLayout()
            title_layout.setContentsMargins(0, 0, 0, 0)

            class_name = item[0]
            title = QLabel(class_name)
            title.setStyleSheet("""
                border: none;
                font-size: 24px;
                font-weight: bold;
                color: white;
                padding-bottom: 5px;
            """)
            title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            id = str(item[2])
            period = str(item[3])
            class_id = QLabel(f"{id} - {period}")
            class_id.setStyleSheet("""
                font-size: 16px;
                color: gray;
            """)

            title_layout.addWidget(title)
            title_layout.addWidget(class_id)

            grade_num = str(item[1])
            color, border_color = self.get_grade_colors(grade_num)
            grade = QPushButton(grade_num)
            grade.setStyleSheet(f"""
                border: 2px solid {border_color};
                border-radius: 5px;
                background: {color};
                width: 60px;
                font-weight: bold;
                font-size: 24px;
            """)

            layout.addLayout(title_layout)
            layout.addStretch()
            layout.addWidget(grade)

            self.main_layout.addWidget(row)

        self.con.close()

    def get_grade_colors(self, num):
        grade = float(num)
        if grade >= 90:
            return GREEN, BORDER_GREEN
        elif grade >= 80:
            return BLUE, BORDER_BLUE
        elif grade >= 70:
            return ORANGE, BORDER_ORANGE
        else:
            return RED, BORDER_RED




class Footer(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background: gray")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)

        for item in ["Home", "Grades", "Calendar"]:
            button = QPushButton(item)
            button.setStyleSheet("background: gray; border: none;")
            self.main_layout.addWidget(button)
            self.main_layout.addStretch()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GradePath")
        self.setWindowIcon(QIcon("assets/favicon-white.png"))
        self.resize(500, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.header = Header()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.classes = Classes()
        scroll.setWidget(self.classes)

        self.footer = Footer()

        self.window_layout = QVBoxLayout()
        central_widget.setLayout(self.window_layout)
        self.window_layout.addWidget(self.header, alignment=Qt.AlignTop)
        self.window_layout.addWidget(scroll)
        self.window_layout.addWidget(self.footer, alignment=Qt.AlignBottom)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    sys.exit(app.exec())
