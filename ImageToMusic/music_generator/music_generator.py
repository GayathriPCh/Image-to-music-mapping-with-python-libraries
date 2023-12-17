import tempfile

import numpy as np
import pandas as pd
import cv2
from scipy.io import wavfile
import random
from pedalboard import Pedalboard, LadderFilter, Delay, Reverb, PitchShift
from pedalboard.io import AudioFile
import librosa
from midiutil import MIDIFile


# Function to map hue values to frequencies (replace with your implementation)
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


def generate_music_from_image(uploaded_image_path):  # Pass the file path instead of the image
    # Load an image and create a DataFrame with hue values
    uploaded_image = cv2.imread(uploaded_image_path)
    hsv_image = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2HSV)
    pixels_df = pd.DataFrame(hsv_image.reshape(-1, 3), columns=['hues', 'saturations', 'values'])

    # Define scale frequencies (A Harmonic Minor)
    scale_freqs = [220.00, 246.94, 261.63, 293.66, 329.63, 349.23, 415.30]

    # Add 'notes' column to 'pixels_df' based on hue values
    pixels_df['notes'] = pixels_df['hues'].apply(lambda hue: hue2freq(hue, scale_freqs))

    # Define other parameters
    sr = 22050
    T = 0.1  # Duration of each note
    t = np.linspace(0, T, int(T * sr), endpoint=False)
    nPixels = 60 # Number of notes in the song

    # Initialize arrays for song and harmony
    song = np.array([])
    harmony = np.array([])

    # Choose octaves as desired
    octaves = np.array([0.5, 1, 2])

    # Define harmony intervals
    harmony_intervals = ['P4', 'M3', 'P5']  # Example intervals, you can customize this list

    # Create a dictionary for harmony intervals and their ratios
    harmony_select = {
        'P4': 4 / 3,
        'M3': 5 / 4,
        'P5': 3 / 2
    }

    # Create a new DataFrame for the musical data
    musical_df = pd.DataFrame(columns=['frequencies', 'notes', 'midi_number'])

    # Create a MIDI file
    midi = MIDIFile(1)  # 1 track
    midi.addTempo(0, 0, 120)  # track, time, tempo

    # Generate the song and harmony
    for i in range(nPixels):
        octave = random.choice(octaves)
        val = octave * random.choice(pixels_df['notes'])
        harmony_interval = random.choice(harmony_intervals)
        harmony_val = harmony_select[harmony_interval] * val
        note = 0.5 * np.sin(2 * np.pi * val * t)
        harmony_note = 0.5 * np.sin(2 * np.pi * harmony_val * t)
        song = np.concatenate([song, note])
        harmony = np.concatenate([harmony, harmony_note])

        # Calculate frequency, note, and MIDI number
        frequency = val
        note_name = librosa.hz_to_note(frequency)
        midi_number = librosa.note_to_midi(note_name)

        # Append data to the new DataFrame
        new_row = {'frequencies': frequency, 'notes': note_name, 'midi_number': midi_number}
        musical_df = pd.concat([musical_df, pd.DataFrame([new_row])], ignore_index=True)

        # Add note to MIDI file
        midi.addNote(0, 0, midi_number, i, 1, 100)  # track, channel, note, time, duration, volume

    # Save the MIDI file
    midi_file_path = tempfile.NamedTemporaryFile(suffix=".mid", delete=False).name
    with open(midi_file_path, "wb") as midi_file:
        midi.writeFile(midi_file)

    # Create a 2D numpy array for song and harmony
    song_and_harmony = np.column_stack((song, harmony))

    # Transpose the array to have the shape (Nsamples, Nchannels)
    song_and_harmony = song_and_harmony.T

    # Normalize the audio to the 16-bit range
    song_and_harmony = (song_and_harmony * 32767).astype(np.int16)
    song_and_harmony = np.clip(song_and_harmony, -32768, 32767)  # Clip values to the valid range

    # Save the generated song and harmony as an audio file
    output_audio_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    wavfile.write(output_audio_path, sr, song_and_harmony.T)

    # Apply audio effects using the Pedalboard
    board = Pedalboard([
        LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=100),
        Delay(delay_seconds=0.3),
        Reverb(room_size=0.6, wet_level=0.2, width=1.0),
        PitchShift(semitones=6),
    ])

    # Read the generated audio file
    with AudioFile(output_audio_path, 'r') as f:
        audio = f.read(f.frames)
        samplerate = f.samplerate

    # Apply audio effects using the Pedalboard
    effected = board(audio, samplerate)

    # Save the processed audio as a new WAV file
    # Normalize the audio to the 16-bit range
    effected = (effected * 32767).astype(np.int16)
    processed_output_audio_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    wavfile.write(processed_output_audio_path, sr, effected.T)

    return processed_output_audio_path, midi_file_path
