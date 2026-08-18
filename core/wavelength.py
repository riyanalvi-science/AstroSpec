import numpy as np
def calculate_wavelength(spectrum):
    header = spectrum.header
    crval = header.get("CRVAL1")
    crpix = header.get("CRPIX1")
    cdelt = header.get("CDELT1")
    if None in [crval,crpix, cdelt]:
        raise ValueError("Missing wavelength calibration information")
    pixels = np.arange(len(spectrum.flux))
    wavelength = crval + (pixels + 1 - crpix)* cdelt
    return wavelength