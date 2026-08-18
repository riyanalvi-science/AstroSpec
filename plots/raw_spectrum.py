class RawSpectrumPlot:

    def draw(self, figure, observations, **kwargs):

        print("RAW PLOT CALLED")

        figure.clear()

        ax = figure.add_subplot(111)

        # Plot background
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
                    "Plotting:",
                    observation.object_name
                )


                ax.plot(
                    spectrum.wavelength,
                    spectrum.flux,
                    linewidth=1.5,
                    label=f"{observation.object_name} - Stokes I"
                )

                plotted = True



        if not plotted:

            ax.set_title(
                "No Stokes I spectrum available",
                color="white"
            )

            return ax



        # ---------- Appearance ----------

        ax.set_title(
            "Stokes I Spectrum Comparison",
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


        ax.ticklabel_format(
            axis="y",
            style="sci",
            scilimits=(0,0)
        )


        return ax