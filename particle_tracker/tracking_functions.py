# particle_tracker/tracking_functions.py

import numpy as np
from skimage import feature, measure
from scipy.optimize import linear_sum_assignment


def track_frame_fluonima(
    filtered_data, peak_thr, rcweight, roi_size, secondary_thr, im_org_bg_sub, circ_th
):
    """
    Detects particle positions in the current frame.
    """
    # Detect peaks using skimage's peak_local_max
    coordinates = feature.peak_local_max(
        filtered_data, min_distance=roi_size // 2, threshold_abs=peak_thr
    )

    if coordinates.size == 0:
        return {"X": np.array([]), "Y": np.array([])}

    # Create a labeled image from the binary mask
    binary_mask = filtered_data > peak_thr
    labeled_image = measure.label(binary_mask)

    # Extract properties of labeled regions
    properties = measure.regionprops(labeled_image)

    X = []
    Y = []
    for prop in properties:
        # Calculate circularity
        if prop.area == 0:
            continue
        perimeter = prop.perimeter
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * prop.area / (perimeter**2)
        if circularity >= circ_th:
            Y.append(prop.centroid[0])
            X.append(prop.centroid[1])

    return {"X": np.array(X), "Y": np.array(Y)}


def trace_particles_d(positions, traces, displ_threshold, current_index):
    """
    Links detected positions across frames to form particle trajectories.

    Parameters:
        positions (dict): Current frame positions with keys 'X', 'Y'.
        traces (list): Existing traces.
        displ_threshold (float): Maximum allowable displacement squared.
        current_index (int): Current frame index.

    Returns:
        list: Updated traces.
    """
    # Convert existing traces' last positions to array
    if not traces:
        # Initialize traces with current positions
        for x, y in zip(positions["X"], positions["Y"]):
            traces.append({"frames": [current_index], "X": [x], "Y": [y]})
        return traces

    last_positions = np.array([[trace["X"][-1], trace["Y"][-1]] for trace in traces])
