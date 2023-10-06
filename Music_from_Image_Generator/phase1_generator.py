import numpy as np
from scipy.io import wavfile
import IPython.display as ipd
import pandas as pd
import random

from hue_extraction import pixels_df

# Define the sample rate globally
sr = 22050

# Function to map hue values to frequencies
def hue2freq(h, scale_freqs):
    thresholds = [26, 52, 78, 104, 128, 154, 180]
    note = scale_freqs[0]
    if h <= thresholds[0]:
        note = scale_freqs[0]
    elif h > thresholds[0] and h <= thresholds[1]:
        note = scale_freqs[1]
    elif h > thresholds[1] and h <= thresholds[2]:
        note = scale_freqs[2]
    elif h > thresholds[2] and h <= thresholds[3]:
        note = scale_freqs[3]
    elif h > thresholds[3] and h <= thresholds[4]:
        note = scale_freqs[4]
    elif h > thresholds[4] and h <= thresholds[5]:
        note = scale_freqs[5]
    elif h > thresholds[5] and h <= thresholds[6]:
        note = scale_freqs[6]
    else:
        note = scale_freqs[0]

    return note

# Load an image and create a DataFrame with hue values
# (Assuming you have a DataFrame named 'pixels_df' with a 'hues' column)

# Define scale frequencies (you can choose any scale)
scale_freqs = [220.00, 246.94, 261.63, 293.66, 329.63, 349.23, 415.30]

# Add 'notes' column to 'pixels_df' based on hue values
pixels_df['notes'] = pixels_df['hues'].apply(lambda hue: hue2freq(hue, scale_freqs))

# Define other parameters
T = 0.1  # Duration of each note
t = np.linspace(0, T, int(T * sr), endpoint=False)
nPixels = 60  # Number of notes in the song

# Initialize an empty song array
song = np.array([])

# Choose octaves and harmonies as desired
octaves = np.array([0.5, 1, 2])
harmonies = np.array([1, 2, 3])

# Generate the song
for i in range(nPixels):
    octave = random.choice(octaves)
    val = octave * random.choice(pixels_df['notes'])
    harmony = random.choice(harmonies)
    note = 0.5 * np.sin(2 * np.pi * harmony * val * t)
    song = np.concatenate([song, note])

# Save the generated song as an audio file
wavfile.write('output_audio.wav', sr, song.astype(np.float32))

# Play the generated audio
ipd.Audio('output_audio.wav')
