#!/usr/bin/env python3

import numpy as np
import soundfile as sf

# Filename of the output signal
filename = './ressources/pulsedNoise.wav'
# Sample rate
sample_rate = 48000
# Count for pulse intervals
interval = 6

# Logarithmic lengths for noise and silence
noise_lengths = np.linspace(100, 200, interval).astype(int)
silence_lengths = np.linspace(4000, 2000, interval).astype(int)

# Initialize array for audio data
signal = np.array([])

# Create & concatenate silence & noise to audio array for each interval
for i in range(interval):
    # Create noise & silence
    noise = np.random.rand(noise_lengths[i])
    silence = np.zeros(silence_lengths[i])
    
    # Concatenate silence to noise
    sequence = np.concatenate((noise, silence))
    signal = np.concatenate((signal, sequence))

# Normalize signal to fit within 24-bit range
signal = np.float32(signal)  # Convert to float32
signal = np.clip(signal, -1, 1)  # Ensure values are within -1 to 1 range

# Write signal to WAV file
sf.write(filename, signal, samplerate=sample_rate, subtype='PCM_24')
