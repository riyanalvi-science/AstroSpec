from PyQt5.QtCore import QObject, pyqtSignal
from plots.raw_spectrum import RawSpectrumPlot
from plots.multiple_spectra import MultipleSpectraPlot
from plots.normalized_spectrum import NormalizedSpectrumPlot
from plots.continuum import ContinuumPlot
from plots.continuum_subtracted import ContinuumSubtractedPlot
from plots.stokes import StokesPlot
from plots.polarization import PolarizationPlot
from plots.snr import SNRPlot
from plots.error_spectrum import ErrorSpectrumPlot
from plots.stokes_u import StokesUPlot
from plots.stokes_q import StokesQPlot
from core.plot_data_router import PlotDataRouter



class PlotManager(QObject):
    plot_changed = pyqtSignal(str)

    def __init__(self, viewer):
        super().__init__()
        self.viewer = viewer
        self.router = PlotDataRouter()
        self.plots = {"raw":
                RawSpectrumPlot(),
            "multiple":
                MultipleSpectraPlot(),
            "normalized":
                NormalizedSpectrumPlot(),
            "continuum":
                ContinuumPlot(),
            "continuum_subtracted":
                ContinuumSubtractedPlot(),
            "stokes":
                StokesPlot(),
            "stokes_q":
                StokesQPlot(),
            "stokes_u":
                StokesUPlot(),
            "polarization":
                PolarizationPlot(),
            "snr":
                SNRPlot(),
            "error":
                ErrorSpectrumPlot()
        }

    def show(self, plot_name, observations, **kwargs):
        print(
            "Plot requested:",plot_name)
        if plot_name not in self.plots:
            raise ValueError(f"Unknown plot type: {plot_name}")

        # -----------------------------------
        # Decide what data the plot receives
        # -----------------------------------

        if plot_name == "multiple":
            data = []
            for observation in observations:
                spectra = self.router.get_data(plot_name,observation)
                if spectra:
                    data.extend(spectra)
        else:
            # Existing scientific plots
            # work on observations

            data = observations
        print(
            "DATA SENT TO PLOT:",
            len(data)
            if data
            else 0
        )

        plot = self.plots[plot_name]
        figure = self.viewer.get_figure()
        figure.clear()
        plot.draw(
            figure,
            data,
            **kwargs
        )
        self.viewer.refresh()

        # notify UI/dashboard
        self.plot_changed.emit(plot_name)