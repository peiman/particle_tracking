import unittest
import numpy as np
from particle_tracker.image_processing import apply_filters, background_correction


class TestImageProcessing(unittest.TestCase):
    def test_apply_filters(self):
        # Create a sample image
        image = np.random.rand(100, 100)

        # Test with no median filter
        filtered_image = apply_filters(image, 0, 0.1)
        self.assertEqual(filtered_image.shape, image.shape)

        # Test with median filter
        filtered_image = apply_filters(image, 3, 0.1)
        self.assertEqual(filtered_image.shape, image.shape)

    def test_background_correction(self):
        # Create a sample image with a background trend
        x, y = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
        background = 10 * x + 5 * y
        particles = np.zeros((100, 100))
        particles[20, 20] = 10
        particles[50, 50] = 10
        particles[80, 80] = 10
        image = background + particles + np.random.rand(100, 100)

        corrected_image = background_correction(image, 15)
        self.assertEqual(corrected_image.shape, image.shape)
        self.assertLess(np.std(corrected_image), np.std(image))

        # Check if particles are still visible
        self.assertGreater(corrected_image[20, 20], np.mean(corrected_image))
        self.assertGreater(corrected_image[50, 50], np.mean(corrected_image))
        self.assertGreater(corrected_image[80, 80], np.mean(corrected_image))


if __name__ == "__main__":
    unittest.main()
