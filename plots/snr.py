class SNRPlot:

    def draw(self, figure, observations, **kwargs):

        print("SNR PLOT CALLED")


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


            stokes_i = observation.spectra.get(
                "STOKES_I"
            )



            if stokes_i is None:

                print(
                    "Missing Stokes I or Error for:",
                    observation.object_name
                )

                continue
            error = None
            if hasattr(stokes_i, "error"):
                error = stokes_i.error
            if error is None:
                error_spectrum = observation.spectra.get("ERROR")
                if error_spectrum is not None:
                    error= error_spectrum.error
            if error is None:
                print("Missing error data for:", observation.object_name)
                continue
            if error is None:

                print(
                    "Error array unavailable for:",
                    observation.object_name
                )

                continue



            print(
                "Calculating SNR:",
                observation.object_name
            )



            snr = (
                flux /
                error
            )



            ax.plot(
                wavelength,
                snr,
                linewidth=1.5,
                label=observation.object_name
            )


            plotted = True




        if not plotted:

            ax.set_title(
                "SNR unavailable",
                color="white"
            )

            return ax




        ax.set_title(
            "Signal-to-Noise Ratio Spectrum",
            fontsize=14,
            color="white"
        )


        ax.set_xlabel(
            "Wavelength (Å)",
            fontsize=12,
            color="white"
        )


        ax.set_ylabel(
            "SNR",
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