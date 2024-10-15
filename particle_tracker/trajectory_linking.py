# particle_tracker/trajectory_linking.py

import numpy as np
from scipy.optimize import linear_sum_assignment


def link_trajectories(positions, traces, displ_threshold, current_index):
    if not traces:
        return [
            {"frames": [current_index], "X": [x], "Y": [y]}
            for x, y in zip(positions["X"], positions["Y"])
        ]

    last_positions = np.array([[trace["X"][-1], trace["Y"][-1]] for trace in traces])
    current_positions = np.array([[x, y] for x, y in zip(positions["X"], positions["Y"])])

    if len(last_positions) == 0 or len(current_positions) == 0:
        return traces

    dist_matrix = np.linalg.norm(
        last_positions[:, np.newaxis, :] - current_positions[np.newaxis, :, :], axis=2
    )
    row_ind, col_ind = linear_sum_assignment(dist_matrix)

    for r, c in zip(row_ind, col_ind):
        if dist_matrix[r, c] ** 2 <= displ_threshold:
            traces[r]["frames"].append(current_index)
            traces[r]["X"].append(current_positions[c, 0])
            traces[r]["Y"].append(current_positions[c, 1])

    for c in set(range(len(current_positions))) - set(col_ind):
        traces.append(
            {
                "frames": [current_index],
                "X": [current_positions[c, 0]],
                "Y": [current_positions[c, 1]],
            }
        )

    return traces
