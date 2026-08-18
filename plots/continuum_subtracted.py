import numpy as np

class ContinuumSubtractedPlot:
    def draw(self, figure, observations, **kwargs):
        print("CONTINUUM SUBTRACTED PLOT CALLED")
        figure.clear()
        ax = figure.add_subplot(111)
        ax.set_facecolor("#0b1320")
        if observations is None or len(observations) == 0:
            ax.set_title("No observations available",color="white")
            return ax
        plotted = False
        for observation in observations:
            spectrum = observation.spectra.get("STOKES_I")
            if spectrum is None:
                continue
            wavelength = spectrum.wavelength
            flux = spectrum.flux
            mask = np.ones_like(flux,dtype=bool)

            for _ in range(8):
                coefficients = np.polyfit(wavelength[mask],flux[mask],2)
                continuum = np.polyval(coefficients,wavelength)
                residual = flux - continuum
                sigma = np.std(residual[mask])
                mask = (residual < 1.5*sigma)
            line_spectrum = (flux - continuum)
            ax.plot(wavelength,line_spectrum,linewidth=1.5,label=observation.object_name)
            plotted = True

        if not plotted:
            ax.set_title("No Stokes I spectrum available",color="white")
            return ax
        ax.set_title("Continuum Subtracted Spectrum",fontsize=14,color="white")
        ax.set_xlabel("Wavelength (Å)",fontsize=12,color="white")
        ax.set_ylabel("Flux - Continuum",fontsize=12,color="white")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("white")
        ax.axhline(0,linestyle="--",alpha=0.5)
        ax.grid(True,linestyle="--",alpha=0.3)
        ax.legend(fontsize=10,facecolor="#0b1320",edgecolor="white",labelcolor="white")
        return ax