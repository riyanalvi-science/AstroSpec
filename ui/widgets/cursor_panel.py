from PyQt5.QtWidgets import (QWidget,QVBoxLayout,QLabel,QPushButton)

from PyQt5.QtCore import pyqtSignal
class CursorPanel(QWidget):
    clear_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(260)
        layout = QVBoxLayout()
        self.title = QLabel("CURSOR INFORMATION")
        self.title.setStyleSheet(
            """
            QLabel {
color:#4da6ff;font-size:18px;font-weight:bold;}""")
        self.position_label = QLabel(
            """
Wavelength:
--
Flux:
--""")

        self.position_label.setStyleSheet(
            """
            QLabel {
                color:white;
                font-size:15px;
                background-color:#111827;
                border-radius:8px;
                padding:15px;
            }
            """
        )
        self.pinned_title = QLabel("PINNED POINTS")
        self.pinned_title.setStyleSheet(
            """
            QLabel {
                color:#4da6ff;
                font-size:18px;
                font-weight:bold;
            }
            """
        )
        self.pinned_points = QLabel("No pinned points")
        self.pinned_points.setStyleSheet(
            """
            QLabel {
                color:white;
                background-color:#111827;
                border-radius:8px;
                padding:15px;
            }
            """
        )
        self.clear_button = QPushButton("🗑 Clear Markers")
        self.clear_button.setStyleSheet(
            """
            QPushButton {
                background-color:#1f2937;
                color:white;
                border-radius:8px;
                padding:8px;
                font-size:14px;
            }
            QPushButton:hover {
                background-color:#2563eb;
            }
            """
        )
        self.clear_button.clicked.connect(self.clear_requested.emit)
        layout.addWidget(self.title)
        layout.addWidget(self.position_label)
        layout.addSpacing(20)
        layout.addWidget(self.pinned_title)
        layout.addWidget(self.pinned_points)
        layout.addStretch()
        layout.addWidget(self.clear_button)
        self.setLayout(layout)
        self.points = []
    def update_cursor(self,wavelength,flux):
        self.position_label.setText(
            f"""
Wavelength:
{wavelength:.3f} Å
Flux:
{flux:.5f}
            """
        )
    def add_point(self,wavelength,flux):
        self.points.append((wavelength,flux))
        text = ""
        for i, point in enumerate(self.points,start=1):
            text += (
                f"{i}.  λ = {point[0]:.3f} Å\n"
                f"    Flux = {point[1]:.5f}\n\n")
        self.pinned_points.setText(text)
    def clear_points(self):
        self.points = []
        self.pinned_points.setText("No pinned points")