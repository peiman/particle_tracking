import numpy as np
from skimage import filters, morphology
from scipy import ndimage


def apply_filters(im_org, median_filt_region, sigma_gauss):
    if median_filt_region != 0:
        im_org = filters.median(im_org, morphology.square(median_filt_region))
    return ndimage.gaussian_filter(im_org, sigma=sigma_gauss, mode="reflect")


def background_correction(image, nr_frames_bg):
    if nr_frames_bg > 0:
        # Estimate background using a large-scale median filter
        background = filters.median(image, morphology.disk(nr_frames_bg))
        return image - background
    return image
