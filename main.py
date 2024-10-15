# main.py

import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from particle_tracker.tracker import ParticleTracker


def parse_arguments():
    """
    Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Particle Tracking and Analysis Script")
    parser.add_argument("file", type=str, help="Path to the .tif movie file")
    parser.add_argument(
        "--add_str", type=str, default="_Try4V", help="String to append to the saved filename"
    )
    parser.add_argument("--no_track", action="store_true", help="Disable particle tracking")
    parser.add_argument("--no_plot", action="store_true", help="Disable real-time plotting")
    parser.add_argument(
        "--min_length_analysis", type=int, default=25, help="Minimum trajectory length for analysis"
    )
    parser.add_argument(
        "--min_length_additional",
        type=int,
        default=10,
        help="Minimum trajectory length for additional analysis",
    )
    parser.add_argument(
        "--last_frame_threshold",
        type=int,
        default=300,
        help="Maximum frame index to consider in additional analysis",
    )
    parser.add_argument(
        "--nr_frames_after",
        type=int,
        default=10,
        help="Number of frames after the last tracked frame for intensity analysis",
    )
    return parser.parse_args()


def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Validate file path
    if not os.path.isfile(args.file):
        print(f"Error: File '{args.file}' does not exist.")
        sys.exit(1)

    # Initialize the ParticleTracker
    tracker = ParticleTracker(
        filepath=args.file,
        add_str=args.add_str,
        track_on=not args.no_track,
        plot_on=not args.no_plot,
    )

    # Process the movie
    tracker.process()

    # Analyze the tracked trajectories if tracking was enabled
    if tracker.track_on:
        tracker.analyze_traces(min_length=args.min_length_analysis)
        tracker.additional_analysis(
            min_length=args.min_length_additional,
            last_frame_threshold=args.last_frame_threshold,
            nr_frames_after=args.nr_frames_after,
        )
    else:
        print("Tracking was disabled. Skipping analysis.")

    # Save results
    tracker.save_results()


if __name__ == "__main__":
    main()
