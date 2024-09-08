#!/usr/bin/env python3

import os
import numpy as np
import soundfile as sf
from scipy.signal import correlate
import matplotlib.pyplot as plt

def calculate_time_shift(signal1, signal2, sample_rate):
    """
    Calculate the time shift between two signals using cross-correlation.

    Parameters:
    signal1 (numpy array): The first audio signal.
    signal2 (numpy array): The second audio signal.
    sample_rate (int): The sample rate of the audio signals.

    Returns:
    float: Time shift in milliseconds.
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
    max_corr_index = np.argmax(np.abs(correlation))

    # Compute lag
    lag = max_corr_index - mid_point

    # Adjust lag to be positive or zero
    if lag < 0:
        lag = -lag

    # Debugging outputs
    # print(f"Correlation length: {correlation_length}")
    # print(f"Max correlation index: {max_corr_index}")
    # print(f"Mid point of correlation: {mid_point}")
    # print(f"Calculated lag (sample points): {lag}")

    # Convert lag to time shift in milliseconds
    time_shift = lag / sample_rate * 1000
    return lag, time_shift

def plot_correlation(signal1, signal2, correlation):
    """
    Plot the signals and their cross-correlation.

    Parameters:
    signal1 (numpy array): The first audio signal.
    signal2 (numpy array): The second audio signal.
    correlation (numpy array): The cross-correlation of the signals.
    """
    plt.figure()

    plt.subplot(3, 1, 1)
    plt.plot(signal1[:1000])  # Plot first 1000 samples
    plt.title('Signal 1')

    plt.subplot(3, 1, 2)
    plt.plot(signal2[:1000])  # Plot first 1000 samples
    plt.title('Signal 2')

    plt.subplot(3, 1, 3)
    plt.plot(correlation)
    plt.title('Cross-Correlation')
    plt.xlabel('Lag (samples)')
    plt.show()

def process_audio_folder(folder_path):
    """
    Process all audio files in a folder and calculate time shifts between them.

    Parameters:
    folder_path (str): Path to the folder containing audio files.
    """
    audio_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

    signals = {}
    sample_rate = None

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
            print(f"Sample rates do not match for file {audio_file}. Skipping.")
            continue
        
        signals[audio_file] = signal
    
    # Calculate time shifts
    for i, (file1, signal1) in enumerate(signals.items()):
        for file2, signal2 in list(signals.items())[i+1:]:
            lag, time_shift = calculate_time_shift(signal1, signal2, sample_rate)
            print(f"Time shift between {file1} and {file2}: {lag}, {time_shift:.2f} ms")

if __name__ == "__main__":
    folder_path = '/Users/maxbauer/Desktop/cross-corr_test'  # Replace with the path to your folder
    process_audio_folder(folder_path)
