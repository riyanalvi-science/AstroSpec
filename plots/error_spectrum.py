class ErrorSpectrumPlot:

    def draw(self, figure, observations, **kwargs):
        print("ERROR SPECTRUM PLOT CALLED")
        figure.clear()
        ax = figure.add_subplot(111)
        ax.set_facecolor("#0b1320")
        if observations is None or len(observations) == 0:
            ax.set_title("No observations available",color="white")
            return ax
        plotted = False
        for observation in observations:
            print(observation.spectra.keys())


            # ---------------------------------
            # Check if separate ERROR exists
            # ---------------------------------

            error = observation.spectra.get("ERROR")
            print("ERROR OBJECT:", error)
            print("ERROR TYPE:", type(error))

            # ---------------------------------
            # Fallback:
            # Check error stored inside Stokes I
            # ---------------------------------

            if error is None:
                stokes_i = observation.spectra.get("STOKES_I")
                print("STOKES I:",stokes_i)
                if stokes_i is not None:
                    print("WAVELENGTH:",stokes_i.wavelength)
                    if hasattr(stokes_i,"error"):
                        error = stokes_i.error
            # ---------------------------------
            # If error exists, plot it
            # ---------------------------------

            if error is not None:
                print("Plotting error spectrum:",observation.object_name)
                # Wavelength comes from Stokes I
                stokes_i = observation.spectra.get("STOKES_I")
                if stokes_i is None:
                    print("No Stokes I available for wavelength")
                    continue
                wavelength = stokes_i.wavelength
                if wavelength is None:
                    print("No wavelength available")
                    continue

                if len(wavelength) != len(error):
                    print(
                        "Wavelength and error length mismatch:",
                        len(wavelength),
                        len(error)
                    )
                    continue
                ax.plot(
                    wavelength,
                    error,
                    linewidth=1.5,
                    label=observation.object_name)
                plotted = True

        # ---------------------------------
        # No error spectrum found
        # ---------------------------------

        if not plotted:
            ax.set_title("No uncertainty spectrum available",fontsize=14,color="white")
            ax.text(
                0.5,
                0.5,
                "This FITS file does not contain\n"
                "an error spectrum",
                ha="center",
                va="center",
                transform=ax.transAxes,
                color="white",
                fontsize=12
            )
            ax.tick_params(colors="white")
            for spine in ax.spines.values():
                spine.set_color("white")
            return ax
        # ---------------------------------
        # Formatting
        # ---------------------------------

        ax.set_title(
            "Flux Uncertainty Spectrum",
            fontsize=14,
            color="white"
        )
        ax.set_xlabel(
            "Wavelength (Å)",
            fontsize=12,color="white")
        ax.set_ylabel("Uncertainty",fontsize=12,color="white")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("white")
        ax.grid(True,linestyle="--",alpha=0.3)
        ax.legend(fontsize=10,facecolor="#0b1320",edgecolor="white",labelcolor="white")
        return ax