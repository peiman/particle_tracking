import unittest
import os
import tempfile
import numpy as np
from particle_tracker.io_operations import gen_save_name, save_results


class TestIOOperations(unittest.TestCase):
    def test_gen_save_name(self):
        fname = "/path/to/file.tif"
        add_str = "_test"
        name_base, save_name = gen_save_name(fname, add_str)

        self.assertEqual(name_base, "file")
        self.assertEqual(save_name, "file_test")

    def test_save_results(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            name_base = os.path.join(tmpdir, "test")
            traces = [
                {"frames": [0, 1], "X": [1.0, 1.5], "Y": [1.0, 1.5]},
                {"frames": [0, 1], "X": [2.0, 2.5], "Y": [2.0, 2.5]},
            ]
            save_data = np.random.rand(100, 100, 10)

            save_results(traces, save_data, name_base, True)

            self.assertTrue(os.path.exists(f"{name_base}_Traces.csv"))
            self.assertTrue(os.path.exists(f"{name_base}.npz"))
            self.assertTrue(os.path.exists(f"{name_base}_processed_frames.npy"))


if __name__ == "__main__":
    unittest.main()
