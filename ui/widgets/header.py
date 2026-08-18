from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap 

class AstroSpecHeader(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(120)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20,15,20,15)

        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignCenter)
        logo_pixmap= QPixmap(r"D:\AstroSpec\assets\LV_logo.png")
        scaled_logo = logo_pixmap.scaled(75,75,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(scaled_logo)
        main_layout.addWidget(self.logo)
        title_layout = QVBoxLayout()

        self.title = QLabel("AstroSpec")
        self.title.setStyleSheet(
            """
            QLabel {
                color:white;
                font-size:28px;
                font-weight:bold;
            }
            """
        )

        self.subtitle = QLabel("Spectroscopic Analysis Suite")
        self.subtitle.setStyleSheet(
            """
            QLabel {
                color:#9ca3af;
                font-size:16px;
            }
            """
        )

        title_layout.addWidget(self.title)
        title_layout.addWidget(self.subtitle)

        main_layout.addLayout(title_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.dashboard)
        self.setLayout(main_layout)

    def update_observation(
        self,
        object_name,
        mode,
        points
    ):

        self.object_label.setText(
            f"""
OBJECT

{object_name}
"""
        )

        self.mode_label.setText(
            f"""
MODE

{mode}
"""
        )

        self.points_label.setText(
            f"""
DATA POINTS

{points}
"""
        )


    def update_mode(self, mode):

        self.mode_label.setText(
            f"""
MODE

{mode}
"""
        )