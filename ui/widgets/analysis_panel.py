from PyQt5.QtWidgets import (QWidget,QVBoxLayout,QLabel,QTableWidget,QTableWidgetItem,QPushButton,QHeaderView)
from PyQt5.QtCore import pyqtSignal
class AnalysisPanel(QWidget):
    clear_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(260)
        layout = QVBoxLayout()
        # ==========================
        # Title
        # ==========================
        title = QLabel("POINT INSPECTOR")
        title.setStyleSheet(
            """
            QLabel {

                color:#4da6ff;
                font-size:18px;
                font-weight:bold;

            }""")
        layout.addWidget(title)



        # ==========================
        # Cursor information
        # ==========================

        self.cursor_label = QLabel("""Cursor Position
Wavelength:--
Flux:--""")

        self.cursor_label.setStyleSheet(
            """
            QLabel {

                background-color:#111827;
                border:1px solid #34495e;
                border-radius:10px;
                padding:15px;
                color:white;
                font-size:14px;

            }
            """
        )
        self.cursor_label.setMinimumHeight(120)
        layout.addWidget(self.cursor_label)
        # ==========================
        # Pinned Points
        # ==========================

        pinned_title = QLabel("Pinned Points")
        pinned_title.setStyleSheet(
            """
            QLabel {

                color:#4da6ff;
                font-size:16px;
                font-weight:bold;

            }
            """
        )


        layout.addWidget(pinned_title)
        self.point_table = QTableWidget()
        self.point_table.setColumnCount(3)
        self.point_table.setHorizontalHeaderLabels(["#","Wavelength","Flux"])
        self.point_table.horizontalHeader().setStretchLastSection(True)
        self.point_table.setStyleSheet(
            """
            QTableWidget {

                background-color:#111827;
                color:white;
                border:1px solid #34495e;

            }


            QHeaderView::section {

                background-color:#0b1320;
                color:#4da6ff;
                font-weight:bold;
                border:none;

            }
            """
        )
        layout.addWidget(self.point_table)
        # ==========================
        # Clear button
        # ==========================
        self.clear_button = QPushButton("🗑 Clear Markers")
        self.clear_button.setStyleSheet(
            """
            QPushButton {

                background-color:#1f2937;
                color:white;
                border:1px solid #34495e;
                border-radius:8px;
                padding:8px;

            }


            QPushButton:hover {

                border:1px solid #4da6ff;

            }

            """
        )


        self.clear_button.clicked.connect(self.clear_points)
        self.clear_button.clicked.connect(lambda: self.clear_requested.emit())
        layout.addWidget(self.clear_button)

        # ==========================
        # Observation Information
        # ==========================

        info_title = QLabel("Observation Information")
        info_title.setStyleSheet(
            """
            QLabel {

                color:#4da6ff;
                font-size:16px;
                font-weight:bold;

            }
            """
        )


        layout.addWidget(info_title)
        self.info_label = QLabel(
            """
Object:
Instrument:
Telescope:
Date:
"""
        )
        self.info_label.setStyleSheet(
            """
            QLabel {

                background-color:#111827;
                border:1px solid #34495e;
                border-radius:10px;
                padding:15px;
                color:white;
                font-size:14px;

            }
            """
        )


        layout.addWidget(self.info_label)
        layout.addStretch()
        self.setLayout(layout)

    # ==========================
    # Update cursor position
    # ==========================

    def update_cursor(
        self,
        wavelength,
        flux
    ):

        self.cursor_label.setText(
            f"""
Cursor Position

Wavelength:
{wavelength:.3f} Å

Flux:
{flux:.5e}
"""
        )



    # ==========================
    # Add pinned point
    # ==========================

    def add_pinned_point(
        self,
        wavelength,
        flux
    ):

        row = self.point_table.rowCount()
        self.point_table.insertRow(row)
        self.point_table.setItem(row,0,QTableWidgetItem(str(row + 1)))
        self.point_table.setItem(row,1,QTableWidgetItem(f"{wavelength:.3f}"))
        self.point_table.setItem(row,2,QTableWidgetItem(f"{flux:.5e}"))
    # ==========================
    # Clear table
    # ==========================

    def clear_points(self):
        self.point_table.setRowCount(0)

    # ==========================
    # Observation details
    # ==========================

    def update_information(self,observations):
        if not observations:
            return
        obs = observations[0]
        self.info_label.setText(
            f"""
Object:
{obs.object_name}

Instrument:
{obs.instrument}

Telescope:
{obs.telescope}

Date:
{obs.date}
"""
        )