# particle_tracker/visualization.py

import matplotlib.pyplot as plt


def plot_frame(image, positions, traces, frame_index):
    plt.figure(10)
    plt.clf()
    plt.imshow(image, cmap="gray", vmin=0, vmax=3000)
    plt.colorbar()
    plt.title(f"Frame: {frame_index+1}")

    if positions is not None:
        plt.plot(
            positions["X"],
            positions["Y"],
            "o",
            markersize=4,
            markerfacecolor="none",
            markeredgecolor="r",
        )

    if traces:
        for trace in traces:
            plt.plot(trace["X"], trace["Y"], "-", linewidth=1)

    plt.draw()
    plt.pause(0.001)
