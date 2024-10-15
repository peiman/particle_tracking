import unittest
import numpy as np
from particle_tracker.particle_detection import detect_particles


class TestParticleDetection(unittest.TestCase):
    def test_detect_particles(self):
        # Create a sample image with some bright spots
        image = np.zeros((100, 100))
        image[20, 20] = 1.0
        image[50, 50] = 1.0
        image[80, 80] = 1.0

        # Add some noise
        np.random.seed(42)  # For reproducibility
        image += np.random.normal(0, 0.1, image.shape)

        roi_size = 5
        circ_th = 0.5  # Lowered circularity threshold

        result = detect_particles(image, roi_size, circ_th)

        self.assertIn("X", result)
        self.assertIn("Y", result)

        print(f"Detected particles: X={result['X']}, Y={result['Y']}")

        self.assertEqual(len(result["X"]), 3)
        self.assertEqual(len(result["Y"]), 3)

        # Check if detected particles are close to the actual positions
        expected_positions = [(20, 20), (50, 50), (80, 80)]
        for x, y in zip(result["X"], result["Y"]):
            self.assertTrue(
                any(abs(x - ex) <= 1 and abs(y - ey) <= 1 for ex, ey in expected_positions),
                f"Detected particle at ({x}, {y}) is not close to any expected position",
            )

        # Print image statistics
        print(f"Image with particles statistics:")
        print(
            f"Min: {np.min(image)}, Max: {np.max(image)}, Mean: {np.mean(image)}, Std: {np.std(image)}"
        )

    def test_detect_particles_no_particles(self):
        # Create a sample image with no bright spots
        np.random.seed(42)  # For reproducibility
        image = 0.1 * np.random.rand(100, 100)

        roi_size = 5
        circ_th = 0.5  # Lowered circularity threshold

        result = detect_particles(image, roi_size, circ_th)

        self.assertIn("X", result)
        self.assertIn("Y", result)
        self.assertEqual(len(result["X"]), 0)
        self.assertEqual(len(result["Y"]), 0)

        # Print image statistics
        print(f"No-particle image statistics:")
        print(
            f"Min: {np.min(image)}, Max: {np.max(image)}, Mean: {np.mean(image)}, Std: {np.std(image)}"
        )
        print(f"Detected particles: X={result['X']}, Y={result['Y']}")


if __name__ == "__main__":
    unittest.main()
