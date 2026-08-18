class StokesPlot:

    def draw(self, figure, observations, **kwargs):
        figure.clear()
        ax = figure.add_subplot(111)
        ax.set_facecolor("#0b1320")
        plotted = False
        for observation in observations:
            q = observation.spectra.get("STOKES_Q")
            u = observation.spectra.get("STOKES_U")
            if q is not None:
                print("Plotting Q:",observation.object_name)
                ax.plot(q.wavelength,q.flux,linewidth=1.5,label=f"{observation.object_name} - Stokes Q")
                plotted = True
            if u is not None:
                print("Plotting U:",observation.object_name)
                ax.plot(u.wavelength,u.flux,linewidth=1.5,label=f"{observation.object_name} - Stokes U")
                plotted = True
        if not plotted:
            ax.set_title("No Stokes Q/U data available",color="white")
            return ax
        ax.set_title("Linear Polarization Components (Q & U)",fontsize=14,color="white")
        ax.set_xlabel("Wavelength (Å)",fontsize=12,color="white")
        ax.set_ylabel("Polarization",fontsize=12,color="white")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("white")
        ax.grid(True,linestyle="--",alpha=0.3)
        ax.legend(fontsize=10,facecolor="#0b1320",edgecolor="white",labelcolor="white")
        return ax