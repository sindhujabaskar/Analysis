# %% GET LIBRARIES
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# %% DEFINE FUNCTIONS

def load_suite2p_outputs(directory_path):
    file_dict = {
        'roi_fluorescence': '*F.npy',
        'neuropil_fluorescence': '*Fneu.npy',
        'cell_identifier' : '*iscell.npy',
        'intermediate_outputs' : '*ops.npy',
        'roi_traces' : '*spks.npy',
        'roi_statistics' : '*stat.npy'
    }
    loaded_data_files = {}
    pathlist = Path(directory_path)

    for key, value in file_dict.items():
        suite2p_files = list(pathlist.glob(value))
        for file in suite2p_files:
            loaded_data_files[key] = np.load(file, allow_pickle = True)
    return loaded_data_files

# %% LOAD DATA
suite2p_data_output = load_suite2p_outputs(r'/Volumes/Sinbas_Stuf/Projects/SU24_F31/raw/sub-03/high-SB03/suite2p/plane0')
    
# %% FILTER ROIs (CELLS ONLY)

# assign bool T/F based on confidence index
true_cells_only = suite2p_data_output['cell_identifier'][:,0].astype(bool)
print(true_cells_only)

# filter ROIs and neuropil based on bool value
filtered_roi = np.array(suite2p_data_output['roi_fluorescence'][true_cells_only])
filtered_neuropil = np.array(suite2p_data_output['neuropil_fluorescence'][true_cells_only])

# %% NEUROPIL SUBTRACTION
#neuropil_subtracted_roi = (filtered_roi - (0.7 * filtered_neuropil))
neuropil_subtracted_roi = filtered_roi
#%% PLOT ROIS
plt.plot(neuropil_subtracted_roi[2])
plt.title('Raw Fluorescence of ROI')
plt.xlabel('frames')
plt.ylabel('raw fluorescence')
plt.show()

# %% CALCULATE BASELINE FLUORESCENCE
# initiate empty list
percentile_list = []
fluorescence_percentile = 10 # set percentile value for calculating baseline fluorescence (f0)
## TODO: THIS NEEDS TO BE A FUNCTION
for row in neuropil_subtracted_roi:
    percentile = np.percentile(row, fluorescence_percentile, keepdims= True)
    percentile_list.append(percentile)
baseline_fluorescence = np.array(percentile_list)

#print(baseline_fluorescence)

# %% CALCULATE DF/F
## TODO: THIS NEEDS TO BE A FUNCTION

roi_dff = []
print (neuropil_subtracted_roi.shape[0])
#for row in range(neuropil_subtracted_roi.shape[0]):
for row in range(300):
    foo=neuropil_subtracted_roi[row]
    foo2=(baseline_fluorescence[row])
    print(foo2)
    dff = ((foo) - (baseline_fluorescence[row]))/ (baseline_fluorescence[row])
    roi_dff.append(dff)

# %% PLOTTING DFF 
import matplotlib.pyplot as plt

plt.plot(roi_dff[10])
plt.title('Neuronal Ca2+ activity across session')
plt.xlabel('Frames')
plt.ylabel('df/f')
plt.show()

# %% CREATE VIS STIM SIMULATED VECTOR

def generate_vis_stim_vector(frame_rate, total_frames, stim_duration, gray_duration): #frames per second, total number of frames in session, grat duration (s), gray duration(s))
    gray_frames = int(gray_duration * frame_rate) # gray frames in a single trial
    stim_frames = int(stim_duration * frame_rate) # vis stim frames in a single trial
    vis_trial_timestamps = np.hstack([ np.zeros(gray_frames),np.ones(stim_frames)]) # fills array with 1 for stim frame, 0 for gray
    vis_session_timestamps = np.resize (vis_trial_timestamps, total_frames) # 
    return vis_session_timestamps

simulated_vis_stim = generate_vis_stim_vector(40, 6000, 2, 3)
# print(simulated_vis_stim[:50])

# %% STIM FRAMES ONLY



# %% 
plt.plot(neuropil_subtracted_roi[2][:500])
plt.plot(simulated_vis_stim[:500])
plt.show()
# %%
