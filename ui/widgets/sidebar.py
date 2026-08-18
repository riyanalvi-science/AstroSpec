from PyQt5.QtWidgets import (QWidget,QVBoxLayout,QPushButton,QTreeWidget,QTreeWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal

class SideBar(QWidget):
    observation_changed = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.objects = {}
        self.selected_spectrum_type = "STOKES_I"
        self.create_ui()
        self.setStyleSheet(
            """
            QWidget {background-color: #111827;color: white;font-size: 12px;}
            QPushButton {background-color: #1f6feb;color: white;border-radius: 6px;padding: 8px;font-weight: bold;}
            QPushButton:hover {background-color: #388bfd;}
            QPushButton:pressed {background-color: #1158c7;}
            QTreeWidget {background-color: #0b1320;color: white;border: 1px solid #30363d;border-radius: 8px; padding: 5px;}
            QTreeWidget::item {height: 24px;padding-left: 5px;}
            QTreeWidget::item:hover {background-color: #1f2937;}
            QTreeWidget::item:selected {background-color: #1f6feb;color: white;border-radius: 4px;}
            QHeaderView::section {background-color: #111827;color: #4da6ff;padding: 6px;border: none;font-weight: bold;}
            """
        )
        self.tree.itemChanged.connect(self.emit_change)
        self.tree.itemClicked.connect(self.product_selected)

    def create_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(12,12,12,12)
        self.open_button = QPushButton("📂  Open FITS")
        self.open_button.setMinimumHeight(35)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Astronomical Objects")
        self.tree.setMinimumWidth(260)
        layout.addWidget(self.open_button)
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def add_observation(self, astro_object, observation):
        object_name = astro_object.name
        if object_name not in self.objects:
            object_item = QTreeWidgetItem(self.tree,[object_name])
            self.objects[object_name] = object_item
        else:
            object_item = self.objects[object_name]
        obs_item = QTreeWidgetItem(object_item,[observation.date])
        obs_item.observation = observation
        obs_item.setFlags(
            obs_item.flags()
            |
            Qt.ItemIsUserCheckable)
        obs_item.setCheckState(0,Qt.Checked)

        for product in ["STOKES_I","STOKES_Q","STOKES_U"]:
            product_item = QTreeWidgetItem(obs_item,[product])
            spectrum = observation.spectra.get(product)
            if spectrum is not None:
                product_item.setText(0,product + " ✓")
            else:
                product_item.setText(0,product + " (not available)")
        object_item.setExpanded(True)
        obs_item.setExpanded(True)

    def update_observation(self, observation):
        for object_item in self.objects.values():
            for i in range(object_item.childCount()):
                obs_item = object_item.child(i)
                if obs_item.observation == observation:
                    obs_item.takeChildren()
                    for product in ["STOKES_I","STOKES_Q","STOKES_U"]:
                        product_item = QTreeWidgetItem(obs_item,[product])
                        product_item.setFlags(
                            product_item.flags()
                            |
                            Qt.ItemIsSelectable
                        )

                        spectrum = observation.spectra.get(product)

                        if spectrum is not None:
                            product_item.setText(0,product + " ✓")
                        else:
                            product_item.setText(0,product + " (not available)")
                    obs_item.setExpanded(True)
                    return



    def clear_objects(self):
        self.objects.clear()
        self.tree.clear()

    def get_selected_observations(self):
        selected = []
        for object_item in self.objects.values():
            for i in range(object_item.childCount()):
                obs_item = object_item.child(i)
                if obs_item.checkState(0) == Qt.Checked:
                    selected.append(obs_item.observation)
        return selected

    def emit_change(self, item, column):
        self.observation_changed.emit()

    def product_selected(self, item, column):
        print("CLICKED:",item.text(0))
        text = item.text(0)
        if "STOKES_I" in text:
            self.selected_spectrum_type = "STOKES_I"
        elif "STOKES_Q" in text:
            self.selected_spectrum_type = "STOKES_Q"
        elif "STOKES_U" in text:
            self.selected_spectrum_type = "STOKES_U"
        print("CURRENT TYPE:",self.selected_spectrum_type)
        self.observation_changed.emit()

    def get_selected_spectrum_type(self):
        return self.selected_spectrum_type