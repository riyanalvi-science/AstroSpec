class Observation:

    def __init__(self):
        self.date = "Unknown"
        self.instrument = "Unknown"
        self.telescope = "Unknown"
        self.exposure = "Unknown"
        self.object_name = "Unknown"

        # Store all products
        self.spectra = {
            "STOKES_I": None,
            "STOKES_Q": None,
            "STOKES_U": None,
            "ERROR": None
        }
    def add_spectrum(self, spectrum):
        # Normal Stokes products
        if spectrum.spectrum_type in [
            "STOKES_I",
            "STOKES_Q",
            "STOKES_U"
        ]:
            self.spectra[spectrum.spectrum_type] = spectrum

        # Error spectrum
        if spectrum.error is not None:
            self.spectra["ERROR"] = spectrum.error

    def get_spectrum(self, product):
        return self.spectra.get(product,None)
    def available_products(self):
        products = []
        for key, value in self.spectra.items():
            if value is not None:
                products.append(key)
        return products