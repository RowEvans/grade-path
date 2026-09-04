import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import scraper
import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "grades.db")

# COLORS
GREEN, BORDER_GREEN = "#5FD877", "#3FAE58"
BLUE, BORDER_BLUE = "#4C8DF0", "#2E6FD1"
ORANGE, BORDER_ORANGE = "#F0A94C", "#D18A2E"
RED, BORDER_RED = "#E0554F", "#C0362F"
CHARCOAL = "#333333"

class ScraperWorker(QObject):
    finished = Signal()
    error = Signal(str)

    def run(self):
        try:
            scraper.main()
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

class Header(QWidget):
    refreshed = Signal()

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

        main_label = QLabel("Grades")
        main_label.setStyleSheet(f"""
            color: white;
            font-size: 32px;
            font-weight:bold; 
            padding-bottom: 12px;
            padding-left:6px;
        """)

        self.refresh_button = QPushButton()
        self.refresh_button.setStyleSheet("""
            padding-right: 20px;
        """)
        self.refresh_button.setIcon(QIcon("assets/refresh-icon.png"))
        self.refresh_button.clicked.connect(self.start_refresh)

        top_layout.addWidget(main_label)
        top_layout.addStretch(1)
        top_layout.addWidget(self.refresh_button, alignment=Qt.AlignRight)

    #   now the nav bar
        nav_frame = QFrame()  
        nav_frame.setStyleSheet("""
            background: black;
            border-radius: 8px;
            max-height: 125px;
        """)
        nav_frame.setAttribute(Qt.WA_StyledBackground, True)

        nav_bar = QHBoxLayout(nav_frame)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        for i, name in enumerate(["Q1", "Q2", "Q3", "Q4"]):
            nav_button = QPushButton(name)
            nav_button.setCheckable(True)
            nav_button.setStyleSheet(f"""
                QPushButton{{
                    color: gray;
                    background: {CHARCOAL};
                    border-radius: 5px;
                    border: none;
                    font-size: 12px;
                }}
                QPushButton:checked {{
                    background: {GREEN};
                    color: white;
                    font-size: 14px;
                    font-weight: 700;
                }}
                
            """)
            if i == 0:
                nav_button.setChecked(True)

            self.nav_group.addButton(nav_button)
            nav_bar.addWidget(nav_button)

        self.header_layout.addLayout(top_layout)
        self.header_layout.addWidget(nav_frame)

    def start_refresh(self):
        self.refresh_button.setEnabled(False)
        # start refresh animation

        self.thread = QThread()
        self.worker = ScraperWorker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(self.on_refresh_done)
        self.worker.error.connect(self.on_refresh_error)

        self.thread.start()

    def on_refresh_done(self):
        self.refresh_button.setEnabled(True)
        self.refreshed.emit()

    def on_refresh_error(self, message):
        self.refresh_button.setEnabled(True)
        print("Scraper failed: ", message)



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
            if item[3] == 2511:
                continue
            row = QFrame()
            row.setStyleSheet(f"""
                border: none;
                border-radius: 10px;
                background: {CHARCOAL};
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
                border-radius: 10px;
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
        self.move(QPoint(1920-550, 100))
        

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.header = Header()
        self.header.refreshed.connect(self.reload_classes)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.classes = Classes()
        self.scroll.setWidget(self.classes)

        self.footer = Footer()

        self.window_layout = QVBoxLayout()
        central_widget.setLayout(self.window_layout)
        self.window_layout.addWidget(self.header, alignment=Qt.AlignTop)
        self.window_layout.addWidget(self.scroll)
        self.window_layout.addWidget(self.footer, alignment=Qt.AlignBottom)

    def reload_classes(self):
        old = self.classes
        self.classes = Classes()
        self.scroll.setWidget(self.classes)
        old.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    sys.exit(app.exec())
