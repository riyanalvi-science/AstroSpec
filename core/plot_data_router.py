class PlotDataRouter:

    def get_data(self, plot_name, observation):
        if observation is None:
            return None
        if plot_name == "raw":
            return observation.spectra["STOKES_I"]
        elif plot_name == "stokes":
            # Combined Q + U plot
            return observation
        elif plot_name == "stokes_q":
            return observation.spectra["STOKES_Q"]
        elif plot_name == "stokes_u":
            return observation.spectra["STOKES_U"]
        elif plot_name == "polarization":
            return observation
        elif plot_name == "multiple":
            spectra = []
            for spectrum in observation.spectra.values():
                if spectrum is not None:
                    spectra.append(spectrum)
            return spectra

        elif plot_name in [
            "normalized",
            "continuum",
            "continuum_subtracted",
            "snr",
            "error"
        ]:
            return observation.spectra["STOKES_I"]
        else:
            raise ValueError(
                f"Unknown plot type: {plot_name}")