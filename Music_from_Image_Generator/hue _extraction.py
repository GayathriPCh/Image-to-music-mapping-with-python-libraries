import cv2
import pandas as pd
import numpy as np
from scipy.io import wavfile
import IPython.display as ipd
# Load the image
ori_img = cv2.imread('cat1.jpg')

# Convert the image to the HSV color space
hsv = cv2.cvtColor(ori_img, cv2.COLOR_BGR2HSV)
height, width, _ = hsv.shape
hues = []
for i in range(height):
    for j in range(width):
        hue = hsv[i][j][0]  # This is the Hue value at pixel coordinate (i,j)
        hues.append(hue)
pixels_df = pd.DataFrame({'hues': hues})
print(pixels_df)
scale_freqs = [220.00, 246.94, 261.63, 293.66, 329.63, 349.23, 415.30]
def hue2freq(h, scale_freqs):
    thresholds = [26, 52, 78, 104, 128, 154, 180]
    note = scale_freqs[0]
    if (h <= thresholds[0]):
         note = scale_freqs[0]
    elif (h > thresholds[0]) and (h <= thresholds[1]):
        note = scale_freqs[1]
    elif (h > thresholds[1]) and (h <= thresholds[2]):
        note = scale_freqs[2]
    elif (h > thresholds[2]) and (h <= thresholds[3]):
        note = scale_freqs[3]
    elif (h > thresholds[3]) and (h <= thresholds[4]):
        note = scale_freqs[4]
    elif (h > thresholds[4]) and (h <= thresholds[5]):
        note = scale_freqs[5]
    elif (h > thresholds[5]) and (h <= thresholds[6]):
        note = scale_freqs[6]
    else:
        note = scale_freqs[0]

    return note



# Assuming you already have the 'hues' column in your DataFrame
pixels_df['notes'] = pixels_df['hues'].apply(lambda hue: hue2freq(hue, scale_freqs))
pixels_df.to_csv('pixels_with_notes.csv', index=False)
print(pixels_df)

if __name__ == "__main__":
    sample_hue = 30  # Replace with the hue value you want to test
    frequency = hue2freq(sample_hue, scale_freqs)
    print(f"The corresponding frequency for hue {sample_hue} is {frequency} Hz.")



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

# Add code for octaves here
octaves = np.array([0.5, 1, 2])
for i in range(nPixels):
    octave = np.random.choice(octaves)
    val = octave * np.random.choice(frequencies)  # Choose a random frequency from frequencies array
    note = 0.5 * np.sin(2 * np.pi * val * t)  # Represent each note as a sine wave
    song = np.concatenate([song, note])  # Add notes to create the song

# Save the song as an audio file using wavfile.write
wavfile.write('output_audio.wav', sr, song.astype(np.float32))

# Play the audio
ipd.Audio('output_audio.wav')  # Load the saved audio file and play it
