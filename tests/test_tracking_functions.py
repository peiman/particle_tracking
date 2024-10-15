import unittest
import numpy as np
from particle_tracker.trajectory_linking import link_trajectories


class TestTrajectoryLinking(unittest.TestCase):
    def test_link_trajectories_new_traces(self):
        positions = {"X": np.array([1.0, 2.0]), "Y": np.array([1.0, 2.0])}
        traces = []
        displ_threshold = 10
        current_index = 0

        result = link_trajectories(positions, traces, displ_threshold, current_index)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["frames"], [0])
        self.assertEqual(result[0]["X"], [1.0])
        self.assertEqual(result[0]["Y"], [1.0])
        self.assertEqual(result[1]["frames"], [0])
        self.assertEqual(result[1]["X"], [2.0])
        self.assertEqual(result[1]["Y"], [2.0])

    def test_link_trajectories_existing_traces(self):
        positions = {"X": np.array([1.5, 2.5]), "Y": np.array([1.5, 2.5])}
        traces = [{"frames": [0], "X": [1.0], "Y": [1.0]}, {"frames": [0], "X": [2.0], "Y": [2.0]}]
        displ_threshold = 10
        current_index = 1

        result = link_trajectories(positions, traces, displ_threshold, current_index)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["frames"], [0, 1])
        self.assertEqual(result[0]["X"], [1.0, 1.5])
        self.assertEqual(result[0]["Y"], [1.0, 1.5])
        self.assertEqual(result[1]["frames"], [0, 1])
        self.assertEqual(result[1]["X"], [2.0, 2.5])
        self.assertEqual(result[1]["Y"], [2.0, 2.5])

    def test_link_trajectories_new_particle(self):
        positions = {"X": np.array([1.5, 2.5, 3.0]), "Y": np.array([1.5, 2.5, 3.0])}
        traces = [{"frames": [0], "X": [1.0], "Y": [1.0]}, {"frames": [0], "X": [2.0], "Y": [2.0]}]
        displ_threshold = 10
        current_index = 1

        result = link_trajectories(positions, traces, displ_threshold, current_index)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[2]["frames"], [1])
        self.assertEqual(result[2]["X"], [3.0])
        self.assertEqual(result[2]["Y"], [3.0])


if __name__ == "__main__":
    unittest.main()
