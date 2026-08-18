class StokesQPlot:

    def draw(self, figure, observations, **kwargs):

        figure.clear()

        ax = figure.add_subplot(111)

        ax.set_facecolor("#0b1320")

        plotted = False


        for observation in observations:

            q = observation.spectra.get("STOKES_Q")


            if q is not None:

                print(
                    "Plotting Stokes Q:",
                    observation.object_name
                )


                ax.plot(
                    q.wavelength,
                    q.flux,
                    linewidth=1.5,
                    label=observation.object_name
                )

                plotted = True



        if not plotted:

            ax.set_title(
                "No Stokes Q data available",
                color="white"
            )

            return ax



        ax.set_title(
            "Normalized Stokes Q Spectrum",
            fontsize=14,
            color="white"
        )


        ax.set_xlabel(
            "Wavelength (Å)",
            fontsize=12,
            color="white"
        )


        ax.set_ylabel(
            "Normalized Stokes Q",
            fontsize=12,
            color="white"
        )


        ax.tick_params(
            colors="white"
        )


        for spine in ax.spines.values():

            spine.set_color("white")


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