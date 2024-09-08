#!/usr/bin/env python3

import os
import numpy as np
import soundfile as sf
from scipy.signal import correlate
import matplotlib.pyplot as plt
import argparse

def calculate_time_shift(signal1, signal2, sample_rate):
    """
    Calculate the time shift between two signals using cross-correlation.

    Parameters:
    signal1 (numpy array): The first audio signal.
    signal2 (numpy array): The second audio signal.
    sample_rate (int): The sample rate of the audio signals.

    Returns:
    int: Lag in sample points.
    """
    # Ensure signals are the same length for accurate cross-correlation
    min_length = min(len(signal1), len(signal2))
    signal1 = signal1[:min_length]
    signal2 = signal2[:min_length]

    # Compute cross-correlation
    correlation = correlate(signal1, signal2, mode='full')

    # Length of the correlation
    correlation_length = len(correlation)
    mid_point = (correlation_length - 1) // 2

    # Index of maximum correlation value
    max_corr_index = np.argmax(np.abs(abs(correlation)))

    # Compute lag
    lag = max_corr_index - mid_point

    # Adjust lag to be positive or zero
    if lag < 0:
        lag = -lag

    return lag

def process_audio_folder(folder_path):
    """
    Process all audio files in a folder and calculate time shifts between them.

    Parameters:
    folder_path (str): Path to the folder containing audio files.
    """
    audio_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

    signals = {}
    sample_rate = None
    lags = []

    # Read all audio files
    for audio_file in audio_files:
        file_path = os.path.join(folder_path, audio_file)
        signal, sr = sf.read(file_path)
        
        # Convert to mono if stereo
        if signal.ndim > 1:
            signal = np.mean(signal, axis=1)
        
        if sample_rate is None:
            sample_rate = sr
        elif sample_rate != sr:
            print(f"Warning: Sample rates do not match for file {audio_file}. Skipping.")
            return  # Exit if sample rates don't match

        signals[audio_file] = signal
    
    # Calculate time shifts
    for i, (file1, signal1) in enumerate(signals.items()):
        for file2, signal2 in list(signals.items())[i+1:]:
            lag = calculate_time_shift(signal1, signal2, sample_rate)
            lags.append({
                'file1': file1,
                'file2': file2,
                'lag_samples': lag
            })
            print(f"Time shift between {file1} and {file2}: {lag} samples ({(lag / sample_rate * 1000):.4f} ms)")

def main():
    parser = argparse.ArgumentParser(description='Process audio files to calculate time shifts using cross-correlation.')
    parser.add_argument('folder', type=str, help='Path to the folder containing audio files.')
    args = parser.parse_args()

    folder_path = args.folder
    if not os.path.isdir(folder_path):
        print(f"Error: The directory {folder_path} does not exist.")
        return

    process_audio_folder(folder_path)

if __name__ == "__main__":
    main()
