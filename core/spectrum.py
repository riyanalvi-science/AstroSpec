class Spectrum:
    def __init__(self):
        self.object_name = "Unknown"
        self.wavelength = None
        self.flux= None
        self.error = None
        self.continuum = None
        self.normalized_flux = None
        self.stokes = {"I": None, "Q": None, "U": None}
        self.lines = []
        self.redshift = None
        self.equivalent_width = None
        self.metadata = {}
        self.fits_info= {}
        self.header = None
        self.spectrum_type = "UNKNOWN"
    def summary(self):
        print("="*40)
        print("ASTROSPEC REPORT")
        print("="*40)
        print("OBJECT:", self.object_name)
        if self.flux is not None:
            print("Data points:", len(self.flux))
        print("\nMetadata:")
        for key, value in self.metadata.items():
            print(f"{key}:{value}")
    def inspect_header(self):
        print("\n============== COMPLETE FITS HEADER =============\n")
        for key in self.header.keys():
            print(f"{key:10}:{self.header[key]}")
        print("\n=================================================\n") 
    def show_fits_info(self):
        print("\nFITS INFORMATION:")
        print("------------------")
        for key, value in self.fits_info.items():
            print(f"{key:10}:{value}")      