import numpy as np


class NormalizedSpectrumPlot:

    def draw(self, figure, observations, **kwargs):

        print("NORMALIZED PLOT CALLED")


        figure.clear()

        ax = figure.add_subplot(111)

        ax.set_facecolor("#0b1320")


        if observations is None or len(observations) == 0:

            ax.set_title(
                "No observations available",
                color="white"
            )

            return ax



        plotted = False



        for observation in observations:


            spectrum = observation.spectra.get(
                "STOKES_I"
            )


            if spectrum is not None:


                print(
                    "Normalizing:",
                    observation.object_name
                )


                flux = spectrum.flux


                # Simple normalization
                continuum = np.median(
                    flux
                )


                normalized_flux = (
                    flux / continuum
                )


                ax.plot(
                    spectrum.wavelength,
                    normalized_flux,
                    linewidth=1.5,
                    label=observation.object_name
                )


                plotted = True



        if not plotted:

            ax.set_title(
                "No Stokes I spectrum available",
                color="white"
            )

            return ax



        ax.set_title(
            "Normalized Spectrum",
            fontsize=14,
            color="white"
        )


        ax.set_xlabel(
            "Wavelength (Å)",
            fontsize=12,
            color="white"
        )


        ax.set_ylabel(
            "Normalized Flux",
            fontsize=12,
            color="white"
        )


        ax.tick_params(
            colors="white"
        )


        for spine in ax.spines.values():

            spine.set_color(
                "white"
            )


        ax.grid(
            True,
            linestyle="--",
            alpha=0.3
        )


        ax.legend(
            fontsize=10,
            facecolor="#0b1320",
            edgecolor="white",
            labelcolor="white"
        )


        return ax