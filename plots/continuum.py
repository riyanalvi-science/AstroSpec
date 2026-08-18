import numpy as np


class ContinuumPlot:

    def draw(self, figure, observations, **kwargs):
        print("CONTINUUM PLOT CALLED")
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
            print("Calculating continuum for:",observation.object_name)


            # -----------------------------
            # Remove strong spectral features
            # -----------------------------

            median_flux = np.median(flux)
            mask = (flux < 1.3 * median_flux) & (flux > 0.7 * median_flux)
            if np.sum(mask) < 20:
                continue



            # -----------------------------
            # Polynomial continuum fit
            # -----------------------------

            coefficients = np.polyfit(wavelength[mask],flux[mask],3)
            continuum = np.polyval(coefficients,wavelength)


            # Original spectrum

            ax.plot(
                wavelength,
                flux,
                alpha=0.35,
                label=f"{observation.object_name} Spectrum"
            )


            # Continuum

            ax.plot(
                wavelength,
                continuum,
                linewidth=2,
                label=f"{observation.object_name} Continuum"
            )


            plotted = True



        if not plotted:
            ax.set_title("Continuum could not be estimated",color="white")
            return ax
        ax.set_title("Continuum Fit",fontsize=14,color="white")
        ax.set_xlabel("Wavelength (Å)",fontsize=12,color="white")
        ax.set_ylabel("Flux",fontsize=12,color="white")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("white")
        ax.grid(True,linestyle="--",alpha=0.3)
        ax.legend(
            fontsize=9,
            facecolor="#0b1320",
            edgecolor="white",
            labelcolor="white"
        )
        return ax