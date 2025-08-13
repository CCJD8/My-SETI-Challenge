import os
import numpy as np
import matplotlib.pyplot as plt
import zipfile
import ibmseti


# Read the .zip with zipfile
dataset = zipfile.ZipFile("C:/Users/Connor/Documents/Nebuchadnezzar/Learning/Python/Summer-2025/Simulated Data.zip")
list_of_files = dataset.namelist()

# Use ibmseti to read the time series data without the JSON headers
chosen_file = list_of_files[1]
processed_data = ibmseti.compamp.SimCompamp(dataset.open(chosen_file, 'r').read())
spectrogram = processed_data.get_spectrogram()

# Use matplotlib to plot the spectrogram data
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(np.log(spectrogram),  aspect = (0.5*float(spectrogram.shape[1]) / spectrogram.shape[0]))

plt.show()