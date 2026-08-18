from astropy.io import fits
import os
from .spectrum import Spectrum

def find_header_value(header, keys):
    for key in keys:
        if key in header:
            return header[key]
    return "Unknown"

def classify_fits_type(data, header):
    if data is None:
        return "Unknown"
    if data.ndim == 1:
        if all(key in header
            for key in ["CRVAL1", "CDELT1", "CRPIX1"]):
            return "1D Spectrum"
        return "1D Dataset"
    elif data.ndim == 2:
        return "2D Spectrum/Image"
    elif data.ndim == 3:
        return "Data Cube"
    return f"{data.ndim}D Dataset"

def classify_stokes_type(filename):

    """
    Identify spectropolarimetric product
    from filename convention.
    """

    filename = os.path.basename(filename).lower()
    if ".q" in filename or "_q" in filename:
        return "STOKES_Q"
    elif ".u" in filename or "_u" in filename:
        return "STOKES_U"
    elif "spec" in filename:
        return "STOKES_I"
    else:
        return "UNKNOWN"

def find_error_extension(hdul):
    """
    Search FITS extensions for error spectrum.
    """
    error_keywords = [
        "ERR",
        "ERROR",
        "SIGMA",
        "UNCERTAINTY",
        "VAR",
        "IVAR",
        "NOISE"
    ]


    for hdu in hdul:
        print("Checking HDU:", hdu.name)
        if hdu.data is None:
            continue
        name = hdu.name.upper()
        for key in error_keywords:
            if key in name:
                if hdu.data is not None:
                    return hdu.data
    return None

def load_spectrum(filename):
    spectrum = Spectrum()
    try:
        with fits.open(filename) as hdul:
            print("\n===== FITS STRUCTURE =====")
            for i, hdu in enumerate(hdul):
                shape = None
                if hdu.data is not None:
                    shape = hdu.data.shape
                print(i,hdu.name,shape)
            print("==========================\n")
            data = hdul[0].data
            print("DATA TYPE:", type(data))
            print("DATA SHAPE:", data.shape)
            print("FIRST 10 VALUES:", data[:10])
            header = hdul[0].header
            error_data = find_error_extension(hdul)

    except Exception as e:
        raise Exception(f"Unable to open FITS file: {e}")
    if data is None:
        raise ValueError("No data found in FITS file")

    # ------------------------------
    # Basic information
    # ------------------------------

    spectrum.filename = filename
    spectrum.header = header

    # ------------------------------
    # Stokes identification
    # ------------------------------
    spectrum.spectrum_type = classify_stokes_type(filename)

    # ------------------------------
    # FITS information
    # ------------------------------
    spectrum.fits_info = {
        "NAXIS":
            header.get("NAXIS", "Unknown"),
        "NAXIS1":
            header.get("NAXIS1", "Unknown"),
        "BITPIX":
            header.get("BITPIX", "Unknown"),
        "CRVAL1":
            header.get("CRVAL1", "Unknown"),
        "CRPIX1":
            header.get("CRPIX1", "Unknown"),
        "CDELT1":
            header.get("CDELT1", "Unknown"),
        "BUNIT":
            header.get("BUNIT", "Unknown")

    }



    # ------------------------------
    # Object name
    # ------------------------------

    if "OBJECT" in header:
        spectrum.object_name = header["OBJECT"]
    else:
        spectrum.object_name = os.path.basename(filename)

    # ------------------------------
    # Flux
    # ------------------------------

    spectrum.flux = data

    # ------------------------------
    # Error spectrum
    # ------------------------------

    spectrum.error = error_data
    if spectrum.error is not None:
        print("Error spectrum found:",spectrum.error.shape)
    else:
        print("No error spectrum found")

    # ------------------------------
    # Metadata
    # ------------------------------

    spectrum.metadata = {
        "Instrument":
            find_header_value(
                header,
                [
                    "INSTRUME",
                    "INSTRUMENT",
                    "CAMERA"
                ]
            ),


        "Telescope":
            find_header_value(
                header,
                [
                    "TELESCOP",
                    "OBSERVAT",
                    "FACILITY"
                ]
            ),


        "Date":
            find_header_value(
                header,
                [
                    "DATE-OBS",
                    "DATE"
                ]
            ),


        "Observation Time":
            find_header_value(
                header,
                [
                    "UT",
                    "TIME-OBS"
                ]
            ),


        "Exposure Time":
            find_header_value(
                header,
                [
                    "EXPTIME"
                ]
            ),


        "Origin":
            find_header_value(
                header,
                [
                    "ORIGIN",
                    "OBSERVAT"
                ]
            ),


        "Type":
            classify_fits_type(
                data,
                header
            ),


        "Stokes Type":
            spectrum.spectrum_type

    }

    print("Loaded:",spectrum.object_name)
    return spectrum