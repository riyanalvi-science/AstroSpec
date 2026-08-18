from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QFileDialog,
    QWidget,
    QTabWidget,
    QHBoxLayout,
    QToolBar,
    QAction
)

from ui.widgets.header import AstroSpecHeader
from core.plot_data_router import PlotDataRouter
from core.fits_reader import load_spectrum
from core.wavelength import calculate_wavelength
from core.observation import Observation
from core.astro_object import AstroObject
from ui.widgets.analysis_panel import AnalysisPanel
from ui.widgets.sidebar import SideBar
from Visualization.spectrum_plot import SpectrumPlot
from core.plot_manager import PlotManager
from PyQt5.QtGui import QColor


class AstroSpecWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AstroSpec 1.0")
        self.setGeometry(
            100,
            100,
            1000,
            700
        )
        self.objects = {}

        # Plot system
        self.plot_widget = SpectrumPlot()
        self.plot_manager = PlotManager(self.plot_widget)
        self.plot_manager.plot_changed.connect(self.update_header_plot)

        # Analysis
        self.analysis_panel = AnalysisPanel()
        self.plot_widget.point_hovered.connect(self.analysis_panel.update_cursor)
        self.plot_widget.point_pinned.connect(self.analysis_panel.add_pinned_point)
        self.analysis_panel.clear_requested.connect(self.plot_widget.clear_pins)


        # Tabs
        self.plot_tabs = QTabWidget()
        self.plot_tabs.setUsesScrollButtons(True)
        self.plot_tabs.tabBar().setExpanding(False)


        # Raw spectrum tab
        self.plot_tabs.addTab(QWidget(),"🌈 Raw Spectrum")
        self.plot_tabs.addTab(QWidget(),"📚 Multiple")
        self.plot_tabs.addTab(QWidget(),"📏 Normalized")
        self.plot_tabs.addTab(QWidget(),"〰️ Continuum")
        self.plot_tabs.addTab(QWidget(),"➖ Continuum Subtracted")
        self.plot_tabs.addTab(QWidget(),"🔵 Stokes Q")
        self.plot_tabs.addTab(QWidget(),"🟣 Stokes U")
        self.plot_tabs.addTab(QWidget(),"📐 Polarization")
        self.plot_tabs.addTab(QWidget(),"📊 SNR")
        self.plot_tabs.addTab(QWidget(),"📉 Error")
        self.plot_tabs.setStyleSheet(
        """
        QTabWidget::pane{
            border:1px solid #263244;
            background-color:#0b1320;
            top:-1px;
        }

        QTabBar::tab{
            background-color:#172033;
            color:#9ca3af;
            padding:7px 14px;
            font-size:11pt;
            min-width:130px;
            border-top-left-radius:5px;
            border-top-right-radius:5px;
            margin-right:3px;
        }

        QTabBar::tab:hover{
            background-color:#1e293b;
            color:white;
        }

        QTabBar::tab:selected{
            background-color:#2563eb;
            color:white;
            font-weight:bold;
        }

        QTabBar::tab:!selected{
            margin-top:3px;
        }
        """)
        self.plot_types = ["raw","multiple","normalized","continuum","continuum_subtracted","stokes_q","stokes_u","polarization","snr","error"]
        for i in range(self.plot_tabs.count()):
            self.plot_tabs.tabBar().setTabTextColor(i,QColor("#9ca3af"))
        self.plot_tabs.currentChanged.connect(self.change_plot_tab)
        self.current_plot_type = "raw"
        self.plot_data_router = PlotDataRouter()
        self.create_ui()
        self.create_toolbar()
    def create_ui(self):
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            main_layout = QVBoxLayout()
            self.header = AstroSpecHeader()
            self.header.setMaximumHeight(120)
            content_layout = QHBoxLayout()
            content_layout.setContentsMargins(0,0,0,0)
            content_layout.setSpacing(5)


        # Sidebar
            self.sidebar = SideBar()
            self.sidebar.observation_changed.connect(self.update_plot)
            self.sidebar.observation_changed.connect(self.update_analysis)   
            self.sidebar.setMinimumWidth(300)
            self.sidebar.open_button.clicked.connect(self.open_fits)
            content_layout.addWidget(self.sidebar,1)


        # Plot area
            plot_layout = QVBoxLayout()
            plot_layout.setContentsMargins(0,0,0,0)
            plot_layout.setSpacing(0)


        # IMPORTANT FIX:
        # Do NOT add self.plot_widget here.
        # It already exists inside the Raw tab.
            plot_layout.addWidget(self.plot_tabs)
            plot_layout.addWidget(self.plot_widget,1)
            content_layout.addLayout(plot_layout,6)
        # Analysis panel
            content_layout.addWidget(self.analysis_panel,2)
            main_layout.addWidget(self.header,0)
            main_layout.addLayout(content_layout)
            central_widget.setLayout(main_layout)



    def open_fits(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open FITS file","","FITS files (*.fits)")
        if filename:
            spectrum = load_spectrum(filename)
            spectrum.wavelength = calculate_wavelength(spectrum)
            self.header.update_observation(
                spectrum.object_name,
                spectrum.spectrum_type,len(spectrum.flux))
            object_name = spectrum.object_name
            if object_name not in self.objects:
                self.objects[object_name] = AstroObject(object_name)
            astro_object = self.objects[object_name]
            observation = None
            if len(astro_object.observations) > 0:
                observation = astro_object.observations[0]
            if observation is None:
                observation = Observation()
                observation.object_name = object_name
                observation.date = spectrum.metadata.get("Date","Unknown")
                observation.instrument = spectrum.metadata.get("Instrument","Unknown")
                observation.telescope = spectrum.metadata.get("Telescope","Unknown")
                observation.exposure = spectrum.metadata.get("Exposure Time","Unknown")
                astro_object.add_observation(observation)
                self.sidebar.add_observation(astro_object,observation)
            observation.add_spectrum(spectrum)
            self.sidebar.update_observation(observation)


            print("------------------------------")
            print(observation.spectra)
            print("Loaded:", spectrum.filename)
            print("Object:", spectrum.object_name)
            print("Spectrum type:", spectrum.spectrum_type)
            print("Observation spectra:", len(observation.spectra))
            print("------------------------------")
            self.update_plot()
            self.update_analysis()

    def set_plot_type(self, plot_type):
        print("Selected plot:",plot_type)
        self.current_plot_type = plot_type
        self.update_plot()

    def update_plot(self):
        print("UPDATE PLOT STARTED")
        self.plot_widget.clear_pins()
        selected = self.sidebar.get_selected_observations()
        if not selected:
            print("NO OBSERVATION")
            return
        print("Plot selected:",self.current_plot_type)
        for obs in selected:
            print("ACTIVE OBJECT:",obs.object_name)
        data = []
        for observation in selected:
            routed = self.plot_data_router.get_data(self.current_plot_type,observation)
            if routed is None:
                continue
            if isinstance(routed,list):
                data.extend(routed)
            else:
                data.append(routed)
        print("DATA SENT TO PLOT:",len(data))
        self.plot_manager.show(self.current_plot_type,selected)

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        open_action = QAction("📂 Open FITS",self)
        open_action.triggered.connect(self.open_fits)
        toolbar.addAction(open_action)
        toolbar.addSeparator()
        save_action = QAction("💾 Save Plot",self)
        save_action.triggered.connect(self.save_plot)
        toolbar.addAction(save_action)
        toolbar.addSeparator()
        report_action = QAction("📄 Export Report",self)
        report_action.triggered.connect(self.export_report)
        toolbar.addAction(report_action)
        toolbar.addSeparator()

    def update_analysis(self):
        observations = (self.sidebar.get_selected_observations())
        self.analysis_panel.update_information(observations)

    def update_header_plot(self, plot_name):
        plot_names = {
            "raw":
            "Raw Spectrum",
            "multiple":
            "Spectrum Comparison",
            "normalized":
            "Normalized Spectrum",
            "continuum":
            "Continuum Extraction",
            "continuum_subtracted":
            "Continuum Subtracted Spectrum",
            "stokes":
            "Polarization Components",
            "stokes_q":
            "Stokes Q",
            "stokes_u":
            "Stokes U",
            "polarization":
            "Polarization Analysis",
            "snr":"Signal to Noise Ratio",
            "error":"Error Spectrum"}
        self.header.update_mode(plot_names.get(plot_name,plot_name))

    def save_plot(self):
        print("Save Plot Clicked")

    def export_report(self):
        print("Export report clicked")

    def change_plot_tab(self, index):
        plot_type = self.plot_types[index]
        print("TAB SELECTED:",plot_type)
        self.set_plot_type(plot_type)