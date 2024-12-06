#%% GET LIBRARIES
import numpy as np
import pandas as pd
from pathlib import Path

#%% SET DIRECTORY PATH
pathlist = Path(r'/Volumes/Sinbas_Stuf/Projects/SU24_F31/raw/sub-03/baseline-SB03/suite2p/plane0').glob('*.npy')

#%% LOAD ALL SUITE2P OUTPUTS WITHIN DIRECTORY

file_list = [] # initiate empty list
for path in pathlist:  
    print(f'this is the current path {path}')
    file_path = str(path)
    print(f'this is the file_path found {file_path}')
    file_list.append(file_path)
    print(f'this is the appending list {file_list}')


print(file_list)

for file in file_list:
    roi_fluorescence = np.load(file_list[0], allow_pickle = True) # ALL ROI FLUORESCENCE
    neuropil_fluorescence = np.load(file_list[1], allow_pickle = True) # NEUROPIL FLUORESCENCE 
    cell_identifier = np.load(file_list[2], allow_pickle = True) # INDEX FOR DETERMINING ROI AS CELL
    intermediate_outputs = np.load(file_list[3], allow_pickle = True) # SUITE2P RUN SESSION METADATA
    roi_traces = np.load(file_list[4], allow_pickle = True) # DECONVOLVED TRACES
    roi_statistics = np.load(file_list[5], allow_pickle = True) #STATISTICS PER ROI

print(roi_fluorescence)

#%% FILTER ROIs (CELLS ONLY)

# assign bool T/F based on confidence index
true_cells_only = cell_identifier[:,0].astype(bool)
print(true_cells_only)

# filter ROIs and neuropil based on bool value
filtered_roi = np.array(roi_fluorescence[true_cells_only])
filtered_neuropil = np.array(neuropil_fluorescence[true_cells_only])

#
num_roi = len(filtered_roi)

#%% NEUROPIL SUBTRACTION

neuropil_subtracted_roi = (filtered_roi - filtered_neuropil)

#%% PLOT ROIS

import matplotlib.pyplot as plt

roi_number = neuropil_subtracted_roi[3,:]
avg_fluorescence = np.mean

plt.plot(range(len(roi_number)), roi_number)
plt.show()

#%% CALCULATE DF/F

# i have an ndarray containing the fluorescence values of the neuropil subtracted rois
# i want to populate another array or a list with fluorescence values emcompassing a baseline percentile
# i want to then use the percentile array as my "baseline fluorescence" aka F0
# then i must perform a (f-f0)/(f0) calculation for each ROI, at each frame to get a dff output 
# I want to then plot an overlay of before and after percentile normalization of ROI fluorescence 

# initiate empty list
percentile_list = []
fluorescence_percentile = 5 # set percentile value for calculating baseline fluorescence (f0)
for row in neuropil_subtracted_roi[:,:]:
    percentile = np.percentile(row, fluorescence_percentile)
    percentile_list.append(np.abs(percentile))
baseline_fluorescence = np.array(percentile_list)

print(baseline_fluorescence)

#%%
dff_roi = []
for row in neuropil_subtracted_roi:
    dff = ((neuropil_subtracted_roi.T) - (baseline_fluorescence))/ (baseline_fluorescence)
    dff_roi.append(dff)

print(dff_roi[3])


# %% PLOTTING DFF 
import matplotlib.pyplot as plt

roi_number = dff_roi[3]

plt.plot(range(len(roi_number)), roi_number)
plt.show()
# %%
