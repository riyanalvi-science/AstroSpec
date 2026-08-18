class MultipleSpectraPlot:

    def draw(self, figure, data, **kwargs):

        ax = figure.add_subplot(111)

        ax.set_facecolor("#0b1320")


        spectra = data


        if spectra is None or len(spectra) == 0:

            ax.set_title(
                "No spectra available",
                color="white",
                fontsize=14
            )

            return ax



        for spectrum in spectra:

            if (
                spectrum.wavelength is not None
                and spectrum.flux is not None
            ):

                ax.plot(
                    spectrum.wavelength,
                    spectrum.flux,
                    linewidth=1.5,
                    label=spectrum.object_name
                )



        ax.set_title(
            "Spectrum Comparison",
            fontsize=14,
            color="white"
        )


        ax.set_xlabel(
            "Wavelength (Å)",
            fontsize=12,
            color="white"
        )


        ax.set_ylabel(
            "Flux",
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