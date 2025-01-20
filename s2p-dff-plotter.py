# %% GET LIBRARIES
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import csv

# %% DEFINE FUNCTIONS

def load_suite2p_outputs(directory_path): # this will load all Suite2p output files from the specified directory
    file_dict = {
        'roi_fluorescence': '*F.npy',
        'neuropil_fluorescence': '*Fneu.npy',
        'cell_identifier' : '*iscell.npy',
        'intermediate_outputs' : '*ops.npy',
        'roi_traces' : '*spks.npy',
        'roi_statistics' : '*stat.npy'}
    loaded_data_files = {}
    pathlist = Path(directory_path)
    for key, value in file_dict.items():
        suite2p_files = list(pathlist.glob(value))
        for file in suite2p_files:
            loaded_data_files[key] = np.load(file, allow_pickle = True)
    return loaded_data_files

def calculate_dff(raw, baseline): # this will calculate the dff values for each roi
    dff_list = []
    for row in range(len(raw)):
        dff = ((raw[row] - baseline[row])/(baseline[row]))
        dff_list.append(dff)
    return dff_list

def calculate_baseline(raw_fluorescence, percentile): # this will calculate the specified percentile along each roi's raw fluorescence
    percentile_list = []
    for row in raw_fluorescence:
        find_percentile = np.percentile(row, percentile, keepdims = True)
        percentile_list.append(find_percentile)
    return percentile_list

# %% LOAD DATA
suite2p_data_output = load_suite2p_outputs(r'C:\dev\2p-analysis\suite2p\SB03\tiff\sb03_high\suite2p\plane0')
    
# %% FILTER ROIs (CELLS ONLY)

# assign bool T/F based on confidence index
true_cells_only = suite2p_data_output['cell_identifier'][:,0].astype(bool)
# print(true_cells_only)

# filter ROIs and neuropil based on bool value
filtered_roi = np.array(suite2p_data_output['roi_fluorescence'][true_cells_only])
filtered_neuropil = np.array(suite2p_data_output['neuropil_fluorescence'][true_cells_only])

# %% NEUROPIL SUBTRACTION

neuropil_subtracted_roi = (filtered_roi - (filtered_neuropil))

#%% PLOT ROIS
plt.plot(neuropil_subtracted_roi[2])
plt.title('Raw Fluorescence of ROI')
plt.xlabel('frames')
plt.ylabel('raw fluorescence')
plt.show()

# %% CALCULATE BASELINE FLUORESCENCE
baseline_fluorescence = calculate_baseline(filtered_roi, percentile = 10)
#print(baseline_fluorescence)

# %% CALCULATE DF/F
roi_dff = calculate_dff(neuropil_subtracted_roi, baseline_fluorescence)
# print(roi_dff)

# %% PLOTTING DFF 
import matplotlib.pyplot as plt

plt.plot(roi_dff[2])
plt.title('Neuronal Ca2+ activity across session')
plt.xlabel('Frames')
plt.ylabel('df/f')
plt.show()

# %% CREATE VIS STIM SIMULATED VECTOR

# def generate_vis_stim_vector(frame_rate, total_frames, stim_duration, gray_duration): #frames per second, total number of frames in session, grat duration (s), gray duration(s))
#     gray_frames = int(gray_duration * frame_rate) # gray frames in a single trial
#     stim_frames = int(stim_duration * frame_rate) # vis stim frames in a single trial
#     vis_trial_timestamps = np.hstack([ np.zeros(gray_frames),np.ones(stim_frames)]) # fills array with 1 for stim frame, 0 for gray
#     vis_session_timestamps = np.resize (vis_trial_timestamps, total_frames) # 
#     return vis_session_timestamps

# simulated_vis_stim = generate_vis_stim_vector(40, 6000, 2, 3)
# print(simulated_vis_stim[:50])

#%% IMPORT VIS STIM TIMESTAMPS 
# LABEL BY VIS STIM YES/NO
# YES FRAMES IN ONE ARRAY, NO FRAMES IN ANOTHER
# AVG ACROSS THE ARRAYS, AND SEE HOW ACTIVITY IS DIFFERENT DURING VIS STIM AND OUTSIDE

# with open('file', 'r'
# # %% 
# plt.plot(neuropil_subtracted_roi[2][:500])
# plt.plot(simulated_vis_stim[:500])
# plt.show()
# %%
