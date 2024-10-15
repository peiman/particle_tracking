import numpy as np
from skimage import feature, measure


def detect_particles(image, roi_size, circ_th):
    """
    Detect particles in the given image.

    Key features of the algorithm:
    * Normalization of the input image to a 0-1 range, making the algorithm more robust to different intensity scales.
    * Use of a dynamic threshold based on the image statistics (mean + 3 * std), which adapts to different image characteristics.
    * A two-step approach:
      a. First, try to detect particles using the threshold method.
      b. If no particles are found, look for the brightest spots and apply an additional brightness threshold.
    * Limiting the number of detected particles to a maximum of 3, focusing on the brightest spots.
    * Applying circularity and size constraints to filter out non-particle objects.
    """

    # Normalize image to 0-1 range
    image_normalized = (image - np.min(image)) / (np.max(image) - np.min(image))

    # Use a dynamic threshold based on image statistics
    threshold = np.mean(image_normalized) + 3 * np.std(image_normalized)

    # Detect peaks using the threshold method
    coordinates = feature.peak_local_max(
        image_normalized, min_distance=roi_size, threshold_abs=threshold, num_peaks=10
    )

    # Create a labeled image for region properties
    binary_mask = image_normalized > threshold
    labeled_image = measure.label(binary_mask)
    properties = measure.regionprops(labeled_image)

    X = []
    Y = []

    # Apply circularity and size constraints
    for prop in properties:
        if prop.area > 0 and prop.perimeter > 0:
            circularity = 4 * np.pi * prop.area / (prop.perimeter**2)
            if circularity >= circ_th and prop.area <= (roi_size * roi_size):
                Y.append(prop.centroid[0])
                X.append(prop.centroid[1])

    # If no particles detected, use the brightest spots method
    if len(X) == 0:
        bright_spots = np.argpartition(image_normalized.flatten(), -3)[-3:]
        Y, X = np.unravel_index(bright_spots, image_normalized.shape)

        # Apply additional brightness threshold
        brightness_threshold = np.mean(image_normalized) + 5 * np.std(image_normalized)
        X = [x for x, y in zip(X, Y) if image_normalized[y, x] > brightness_threshold]
        Y = [y for x, y in zip(X, Y) if image_normalized[y, x] > brightness_threshold]

    # Limit to top 3 brightest particles
    if len(X) > 3:
        intensities = [image_normalized[int(y), int(x)] for x, y in zip(X, Y)]
        top_3_indices = np.argsort(intensities)[-3:]
        X = np.array(X)[top_3_indices]
        Y = np.array(Y)[top_3_indices]

    # Debug information
    print(f"Number of peaks detected: {len(coordinates)}")
    print(f"Number of labeled regions: {len(properties)}")
    print(f"Number of particles after filtering: {len(X)}")
    print(f"Threshold used: {threshold}")
    print(
        f"Normalized image min: {np.min(image_normalized)}, max: {np.max(image_normalized)}, mean: {np.mean(image_normalized)}, std: {np.std(image_normalized)}"
    )

    return {"X": np.array(X), "Y": np.array(Y)}
