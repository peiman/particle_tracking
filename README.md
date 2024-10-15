# Particle Tracking and Analysis

## Overview

This project provides a Python implementation for tracking particles in `.tif` movie files, performing background correction, and analyzing their trajectories. The code is organized into modular components for better readability and maintainability.

## Project Structure

particle_tracking/
├── main.py
├── particle_tracker/
│   ├── init.py
│   ├── tracker.py
│   ├── utils.py
│   └── tracking_functions.py
├── requirements.txt
└── README.md

- **`main.py`**: Entry point of the application.
- **`particle_tracker/`**: Contains all modules related to particle tracking.
  - **`__init__.py`**: Makes Python treat the directory as a package.
  - **`tracker.py`**: Contains the `ParticleTracker` class.
  - **`utils.py`**: Contains utility functions.
  - **`tracking_functions.py`**: Contains functions for particle detection and trajectory linking.
- **`requirements.txt`**: Lists all Python dependencies.
- **`README.md`**: Provides an overview and instructions.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/particle_tracking.git
   cd particle_tracking
   ```

2. Set Up a Virtual Environment (Optional but Recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Dependencies:

```bash
pip install -r requirements.txt# On Windows: venv\Scripts\activate
```

Usage

Run the main.py script with the required .tif file and optional arguments.

```bash
python main.py path_to_your_file.tif [options]
```

Positional Arguments:

 • file: Path to the .tif movie file.

Optional Arguments:

 • --add_str: String to append to the saved filename (default:_Try4V).
 • --no_track: Disable particle tracking.
 • --no_plot: Disable real-time plotting.
 • --min_length_analysis: Minimum trajectory length for analysis (default: 25).
 • --min_length_additional: Minimum trajectory length for additional analysis (default: 10).
 • --last_frame_threshold: Maximum frame index to consider in additional analysis (default: 300).
 • --nr_frames_after: Number of frames after the last tracked frame for intensity analysis (default: 10).

Example:

```bash
python main.py "../Rhod-pH Drop 6.6 + 150 mM NaCl.tif" --add_str _Experiment1 --min_length_analysis 30
```

Output

 • Tracking Data: If tracking is enabled, the script saves the tracking data and processed frames in a compressed NumPy .npz file named {name_base}{add_str}.npz. For example, if your input file is pH_drop_6_Rho.tif and add_str is _Experiment1, the output file will be pH_drop_6_Rho_Experiment1.npz.
 • Plots: The script generates various plots to visualize displacement vectors, intensity relationships, uncertainties, and cumulative events. If real-time plotting is enabled, you will see the processing frames with overlaid particle positions and trajectories.
 • Console Output: Progress updates are printed every 100 frames, and significant events detected during additional analysis are reported.
