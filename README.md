# Particle Tracking and Analysis

## Overview

This project provides a Python implementation for tracking particles in `.tif` movie files, performing background correction, and analyzing their trajectories. The code is organized into modular components for better readability and maintainability.

## Features

- Particle detection in .tif image sequences
- Background correction
- Trajectory linking
- Analysis of particle movements
- Handling of high-noise and low-contrast scenarios
- Customizable parameters for different experimental conditions

## Project Structure

```
particle_tracking/
├── main.py
├── particle_tracker/
│   ├── __init__.py
│   ├── tracker.py
│   ├── particle_detection.py
│   ├── trajectory_linking.py
│   ├── image_processing.py
│   ├── visualization.py
│   └── io_operations.py
├── tests/
│   ├── test_particle_detection.py
│   ├── test_particle_detection_advanced.py
│   └── ...
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/particle_tracking.git
   cd particle_tracking
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main script with the required `.tif` file and optional arguments:

```
python main.py path_to_your_file.tif [options]
```

### Arguments

- `file`: Path to the .tif movie file.
- `--add_str`: String to append to the saved filename (default: _Try4V).
- `--no_track`: Disable particle tracking.
- `--no_plot`: Disable real-time plotting.
- `--min_length_analysis`: Minimum trajectory length for analysis (default: 25).
- `--min_length_additional`: Minimum trajectory length for additional analysis (default: 10).
- `--last_frame_threshold`: Maximum frame index to consider in additional analysis (default: 300).
- `--nr_frames_after`: Number of frames after the last tracked frame for intensity analysis (default: 10).

### Example

```
python main.py "data/sample_movie.tif" --add_str _Experiment1 --min_length_analysis 30
```

## Running Tests

To run the unit tests, use the following command from the project root directory:

```
python -m unittest discover -v
```

## Contributing

Contributions to this project are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write tests for your changes.
4. Implement your changes and ensure all tests pass.
5. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
