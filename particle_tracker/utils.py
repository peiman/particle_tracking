# particle_tracker/utils.py

import os
import numpy as np


def gen_save_name(fname, add_str):
    """
    Generates a base name and save name by appending add_str to the original filename.

    Parameters:
        fname (str): Original filename.
        add_str (str): String to append.

    Returns:
        tuple: (name_base, save_name)
    """
    name_base = os.path.splitext(os.path.basename(fname))[0]
    save_name = f"{name_base}{add_str}"
    return name_base, save_name


def generate_rcweight(roi_size):
    """
    Generates a weighting matrix based on ROI size.
    This function creates a Gaussian weighting matrix within the ROI.

    Parameters:
        roi_size (int): Size of the Region of Interest.

    Returns:
        np.ndarray: Weighting matrix.
    """
    # Create a Gaussian kernel
    x = np.linspace(-1, 1, roi_size)
    y = np.linspace(-1, 1, roi_size)
    X, Y = np.meshgrid(x, y)
    sigma = 0.5
    rcweight = np.exp(-(X**2 + Y**2) / (2 * sigma**2))
    # Normalize the weighting matrix
    rcweight /= np.sum(rcweight)
    return rcweight
