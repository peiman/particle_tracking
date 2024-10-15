import numpy as np
from tifffile import TiffFile
from .image_processing import apply_filters, background_correction
from .particle_detection import detect_particles
from .trajectory_linking import link_trajectories
from .visualization import plot_frame
from .io_operations import save_results, gen_save_name


class ParticleTracker:
    def __init__(self, filepath, add_str="_Experiment1", track_on=True, plot_on=True):
        self.filepath = filepath
        self.add_str = add_str
        self.track_on = track_on
        self.plot_on = plot_on

        # Initialize parameters
        self.init_parameters()

        # Generate save name
        self.name_base, self.save_name = gen_save_name(self.filepath, self.add_str)

        # Initialize traces and data storage
        self.traces = []
        self.save_data = None

    def init_parameters(self):
        # Filter constants
        self.sigma_gauss = 0.1
        self.median_filt_region = 0
        self.std_filt_value_fullImage = 3
        self.std_filt_th_ratio_relBG = 5
        self.area_filt_values = (2, 50000)
        self.dilate_radius = 1
        self.frames_away_bg = 0
        self.nr_frames_bg = 1

        # Tracking parameters
        self.displ_threshold = 7**2
        self.roi_size = 8
        self.circ_th = 0.7 if self.track_on else None

    def process(self):
        try:
            with TiffFile(self.filepath) as tif:
                frames = len(tif.pages)
                if frames == 0:
                    print("No frames found in the TIFF file.")
                    return

                for k in range(frames):
                    im_org = tif.pages[k].asarray().astype(np.float64)
                    processed_frame = self.process_frame(im_org, k)

                    if self.save_data is None:
                        self.save_data = np.zeros(
                            (processed_frame.shape[0], processed_frame.shape[1], frames),
                            dtype=np.float64,
                        )

                    self.save_data[:, :, k] = processed_frame

                    if (k + 1) % 100 == 0:
                        print(f"{((k + 1) / frames) * 100:.2f}% done")

        except Exception as e:
            print(f"An error occurred during processing: {e}")
            raise  # Re-raise the exception for the test to catch

    def process_frame(self, im_org, frame_index):
        # Apply filters
        filtered_image = apply_filters(im_org, self.median_filt_region, self.sigma_gauss)

        # Background correction
        bg_corrected_image = background_correction(filtered_image, self.nr_frames_bg)

        if self.track_on:
            # Detect particles
            positions = detect_particles(bg_corrected_image, self.roi_size, self.circ_th)

            # Link trajectories
            self.traces = link_trajectories(
                positions, self.traces, self.displ_threshold, frame_index
            )

        if self.plot_on:
            plot_frame(
                bg_corrected_image, positions if self.track_on else None, self.traces, frame_index
            )

        return bg_corrected_image

    def save_results(self):
        save_results(self.traces, self.save_data, self.name_base, self.track_on)

    def analyze_traces(self, min_length=25):
        # Implement or import analyze_traces function
        pass

    def additional_analysis(self, min_length=10, last_frame_threshold=300, nr_frames_after=10):
        # Implement or import additional_analysis function
        pass
