import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

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
        self.setStyleSheet("background-color: darkgray;")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)

        # now for one class
        for item in ["English 4-IB", "AP Economics", "IB TOK 2", "IB Math A & A", "IB Chemistry 3", "IB History of the Americas", "IB Computer Science"]:
            layout = QHBoxLayout()
            title = QLabel(item)
            title.setStyleSheet("font-size: 24px; font-weight: bold; border: 2px; color: white;")
            grade = QPushButton("95.00")
            grade.setStyleSheet("border: 4px; border-color: green; background: green; font-weight: bold; font-size: 24px;")

            layout.addWidget(title, alignment=Qt.AlignLeft)
            layout.addStretch()
            layout.addWidget(grade, alignment=Qt.AlignRight)

            self.main_layout.addLayout(layout)




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

        self.resize(360, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.header = Header()

        self.classes = Classes()

        self.footer = Footer()

        self.window_layout = QVBoxLayout()
        central_widget.setLayout(self.window_layout)
        self.window_layout.addWidget(self.header, alignment=Qt.AlignTop)
        self.window_layout.addWidget(self.classes, alignment=Qt.AlignTop)
        self.window_layout.addWidget(self.footer, alignment=Qt.AlignBottom)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    sys.exit(app.exec())
