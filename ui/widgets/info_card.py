from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class InfoCard(QWidget):

    def __init__(self, title, value="Unknown"):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(12, 10, 12, 10)

        self.title_label = QLabel(title)
        self.value_label = QLabel(value)

        self.title_label.setStyleSheet("""
            color: #4da6ff;
            font-size: 11px;
            font-weight: bold;
        """)
        self.value_label.setStyleSheet("""color: white;font-size: 15px;""")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        self.setLayout(layout)
        self.setStyleSheet("""
            InfoCard {
                background-color: #181818;
                border-left: 3px solid #4da6ff;
                border-radius: 5px;
            }
        """)