#%%
# GET LIBRARIES
import numpy as np
import pandas as pd
from pathlib import Path

#%%
# SET DIRECTORY
pathlist = Path(r'/Volumes/Sinbas_Stuf/Projects/SU24_F31/raw/sub-03/baseline-SB03/suite2p/plane0').glob('*.npy')

#%%
# LOAD ALL SUITE2P OUTPUTS 

file_list= [] # initiate empty list
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

#%%
# FILTER ROIs (CELLS ONLY)

# assign bool T/F based on confidence index
true_cells_only = cell_identifier[:,0].astype(bool)
print(true_cells_only)

# filter ROIs and neuropil based on bool value
filtered_roi = roi_fluorescence[true_cells_only]
filtered_neuropil = neuropil_fluorescence[true_cells_only]

#%%
# NEUROPIL SUBTRACTION

neuropil_subtracted_roi = (filtered_roi - filtered_neuropil)

#%%
# plot individal ROI

import matplotlib.pyplot as plt

roi_number = neuropil_subtracted_roi[3,:]

plt.plot(range(len(roi_number)), roi_number)
plt.show()

# %%
