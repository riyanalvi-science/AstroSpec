from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QHBoxLayout,
    QLabel
)

from PyQt5.QtCore import pyqtSignal


class PlotSelector(QWidget):
    plot_changed = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.plot_map = {

            "📈  Raw Spectrum":
                "raw",

            "🔬  Spectrum Comparison":
                "multiple",

            "📊  Normalized Spectrum":
                "normalized",

            "〰  Continuum":
                "continuum",

            "✂  Continuum Subtracted":
                "continuum_subtracted",

            "🔵  Polarization Components (Q/U)":
                "stokes",

            "🔵  Stokes Q":
                "stokes_q",

            "🟣  Stokes U":
                "stokes_u",

            "🌀  Polarization":
                "polarization",

            "📉  Signal to Noise Ratio":
                "snr",

            "⚠  Error Spectrum":
                "error"
        }
        self.label = QLabel("Visualization")
        self.combo = QComboBox()
        self.combo.addItems(self.plot_map.keys())
        self.combo.currentTextChanged.connect(self.change_plot)
        self.combo.setMinimumWidth(260)
        self.combo.setMinimumHeight(42)
        self.label.setStyleSheet(
            """
            QLabel {

                color:#4da6ff;

                font-size:20px;

                font-weight:bold;

            }
            """
        )



        self.combo.setStyleSheet(
            """

            QComboBox {

                background-color:#0b1320;

                color:white;

                border:1px solid #34495e;

                border-radius:8px;

                padding-left:12px;

                font-size:20px;

            }


            QComboBox:hover {

                border:1px solid #4da6ff;

            }


            QComboBox::drop-down {

                width:30px;

                border:none;

            }


            QComboBox QAbstractItemView {

                background-color:#111827;

                color:white;

                border:1px solid #34495e;

                selection-background-color:#1f6feb;

                selection-color:white;

                padding:5px;

            }

            """
        )
        layout = QHBoxLayout()
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(12)
        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        self.setLayout(layout)



    def change_plot(self, text):
        self.plot_changed.emit(self.plot_map[text])