# particle_tracker/processing.py

import numpy as np
from skimage import filters, morphology
from scipy import ndimage
from scipy.linalg import lstsq
from .tracking_functions import track_frame_fluonima, trace_particles_d


def apply_filters(im_org, median_filt_region, sigma_gauss):
    if median_filt_region != 0:
        im_org = filters.median(im_org, morphology.square(median_filt_region))
    A = ndimage.gaussian_filter(im_org, sigma=sigma_gauss, mode="reflect")
    return A


def background_correction(G, A, X, Y):
    try:
        b, _, _, _ = lstsq(G, A.flatten())
    except Exception as e:
        print(f"Error during least squares solve: {e}")
        b = np.zeros(6)  # Fallback to zero coefficients
    bg1 = b[5] + b[0] * X**2 + b[1] * Y * X + b[2] * Y**2 + b[3] * X + b[4] * Y
    image_after_bg = A - bg1
    return image_after_bg
