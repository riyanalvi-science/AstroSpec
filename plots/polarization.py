import numpy as np


class PolarizationPlot:


    def draw(self, figure, observations, **kwargs):

        print("POLARIZATION PLOT CALLED")

        figure.clear()

        ax = figure.add_subplot(111)

        ax.set_facecolor("#0b1320")


        plotted = False


        for observation in observations:


            q = observation.spectra.get(
                "STOKES_Q"
            )

            u = observation.spectra.get(
                "STOKES_U"
            )


            if q is None or u is None:

                continue


            if q.flux is None or u.flux is None:

                continue


            if len(q.flux) != len(u.flux):

                print(
                    "Q/U length mismatch"
                )
                ax.set_title("Polarization unavailable", color= "white", fontsize=14)
                ax.text(0.5,0.5, "Stokes Q and Stokes U length Mismatch", transform= ax.transAxes, ha= "center", va="center", color="white", fontsize=12)

                return ax



            polarization = np.sqrt(
                q.flux**2 +
                u.flux**2
            )


            wavelength = q.wavelength


            ax.plot(
                wavelength,
                polarization,
                linewidth=1.5,
                label=observation.object_name
            )


            plotted = True



        if not plotted:

            ax.set_title(
                "No Q/U data available",
                color="white"
            )

            return ax



        ax.set_title(
            "Degree of Linear Polarization",
            fontsize=14,
            color="white"
        )


        ax.set_xlabel(
            "Wavelength (Å)",
            color="white"
        )


        ax.set_ylabel(
            "Polarization",
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