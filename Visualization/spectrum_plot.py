from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QSize

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure
class SpectrumPlot(QWidget):
    point_hovered = pyqtSignal(float, float)
    point_pinned = pyqtSignal(float, float)


    def __init__(self):

        super().__init__()
        self.figure = Figure(figsize=(8,5),facecolor="#0b1320")
        self.configure_figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color:#0b1320;")
        self.toolbar = NavigationToolbar(self.canvas,self)
        self.toolbar.setFixedHeight(32)
        self.toolbar.setStyleSheet(
        """
        QToolBar {
            background-color:#111827;
            border:1px solid #334155;
        }

        QToolButton {
            background-color:#1e293b;
            border:1px solid #475569;
            border-radius:4px;
            padding:3px;
        }

        QToolButton:hover {
            background-color:#2563eb;
        }

        QToolButton:pressed {
            background-color:#1d4ed8;
        }
        """
        )
        self.toolbar.setContentsMargins(0,0,0,0)
        self.toolbar.setIconSize(QSize(22,22))
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas,1)
        self.setLayout(layout)
        self.pinned_points = []
        self.marker_artists = []
        self.marker_labels = []
        self.canvas.mpl_connect("motion_notify_event",self.mouse_move)
        self.canvas.mpl_connect("button_press_event",self.mouse_click)



    def configure_figure(self):
        self.figure.subplots_adjust(
            left=0.08,
            right=0.98,
            top=0.95,
            bottom=0.12
        )

    def get_figure(self):
        return self.figure

    def refresh(self):
        self.canvas.draw_idle()

    def clear(self):
        self.figure.clear()
        self.configure_figure()

    def mouse_move(self,event):
        if event.inaxes is None:
            return
        if event.xdata is None or event.ydata is None:
            return
        self.point_hovered.emit(event.xdata,event.ydata)

    def mouse_click(self,event):
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        if event.xdata is None or event.ydata is None:
            return
        x = event.xdata
        y = event.ydata
        self.pinned_points.append((x,y))

        marker = event.inaxes.plot(x,y,marker="o",markersize=8,markerfacecolor="red",markeredgecolor="white")[0]
        self.marker_artists.append(marker)
        label = event.inaxes.annotate(
            f"P{len(self.pinned_points)}",
            xy=(x,y),
            xytext=(8,12),
            textcoords="offset points",
            fontsize=11,
            color="white",
            fontweight="bold")
        self.marker_labels.append(label)
        self.refresh()
        self.point_pinned.emit(x,y)

    def add_marker(self,wavelength,flux):
        ax = self.figure.gca()
        marker = ax.scatter(
            wavelength,
            flux,
            s=60,
            marker="o",
            edgecolors="white",
            zorder=10)


        label = ax.annotate(
            f"{wavelength:.1f} Å",
            (wavelength,flux),
            xytext=(10,10),
            textcoords="offset points",
            fontsize=9,
            color="white")
        self.pinned_points.append((wavelength,flux))
        self.marker_artists.append(marker)
        self.marker_labels.append(label)
        self.refresh()

    def clear_pins(self):
        self.pinned_points.clear()
        for artist in self.marker_artists:
            artist.remove()
        for label in self.marker_labels:
            label.remove()
        self.marker_artists.clear()
        self.marker_labels.clear()
        self.refresh()