import numpy as np
from scipy.io import wavfile
import IPython.display as ipd
import pandas as pd
from hue_extraction import pixels_df

# Load the frequencies from your DataFrame (assuming you have already loaded the DataFrame)
frequencies = pixels_df['notes'].to_numpy()

# Define audio parameters
sr = 22050  # Sample rate
T = 0.1     # 0.1 second duration
t = np.linspace(0, T, int(T * sr), endpoint=False)  # Time variable

# Initialize an empty song array
song = np.array([])

# Define the number of pixels or notes you want to include in the song
nPixels = 60  # Adjust this to the number of notes you want

for i in range(nPixels):
    val = frequencies[i]
    note = 0.5 * np.sin(2 * np.pi * val * t)  # Represent each note as a sine wave
    song = np.concatenate([song, note])  # Add notes to create the song

# Save the song as an audio file using wavfile.write
wavfile.write('output_audio.wav', sr, song.astype(np.float32))

# Play the audio
ipd.Audio('output_audio.wav')  # Load the saved audio file and play it
