import pandas as pd
from hue_extraction import pixels_df
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
