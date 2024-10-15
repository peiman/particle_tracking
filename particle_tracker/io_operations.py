# particle_tracker/io_operations.py

import os
import numpy as np
import pandas as pd


def gen_save_name(fname, add_str):
    name_base = os.path.splitext(os.path.basename(fname))[0]
    save_name = f"{name_base}{add_str}"
    return name_base, save_name


def save_results(traces, save_data, name_base, track_on):
    if track_on and traces:
        data = []
        for trace_id, trace in enumerate(traces, start=1):
            for frame, x, y in zip(trace["frames"], trace["X"], trace["Y"]):
                data.append({"TraceID": trace_id, "Frame": frame, "X": x, "Y": y})

        df = pd.DataFrame(data)
        df.to_csv(f"{name_base}_Traces.csv", index=False)

        np.savez_compressed(f"{name_base}.npz", Traces=traces, save_data=save_data)
        print(f"Tracking data saved to {name_base}.npz and {name_base}_Traces.csv")
    elif track_on:
        print("No traces were generated during tracking. Unable to save results.")
    else:
        print("Processing completed without tracking.")

    if save_data is not None:
        np.save(f"{name_base}_processed_frames.npy", save_data)
        print(f"Processed frames saved to {name_base}_processed_frames.npy")
    else:
        print("No processed frame data available to save.")
