import unittest
import numpy as np
import tempfile
import os
from particle_tracker.tracker import ParticleTracker


class TestParticleTracker(unittest.TestCase):
    def setUp(self):
        # Create a temporary TIFF file for testing
        self.temp_tiff = tempfile.NamedTemporaryFile(suffix=".tif", delete=False)
        self.temp_tiff.close()

        # Create a simple TIFF file with 5 frames
        from tifffile import TiffWriter

        with TiffWriter(self.temp_tiff.name) as tif:
            for _ in range(5):
                tif.write(np.random.rand(100, 100).astype(np.float32))

    def tearDown(self):
        # Remove the temporary file
        os.unlink(self.temp_tiff.name)

    def test_particle_tracker_initialization(self):
        tracker = ParticleTracker(self.temp_tiff.name)
        self.assertIsNotNone(tracker)
        self.assertEqual(tracker.filepath, self.temp_tiff.name)

    def test_particle_tracker_process(self):
        tracker = ParticleTracker(self.temp_tiff.name)
        tracker.process()
        self.assertIsNotNone(tracker.save_data)
        self.assertEqual(tracker.save_data.shape[2], 5)  # 5 frames

    def test_particle_tracker_save_results(self):
        tracker = ParticleTracker(self.temp_tiff.name)
        tracker.process()
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            try:
                tracker.save_results()
                self.assertTrue(os.path.exists(f"{tracker.name_base}_processed_frames.npy"))
            finally:
                os.chdir(original_dir)


if __name__ == "__main__":
    unittest.main()
