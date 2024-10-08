# purpose: unpickling dlc output for pupil analysis 
#%%
#get libraries
import pandas as pd
import numpy as np
import math
import statistics as st
import pathlib

#%% Set file directories

DIRECTORY = (r'E:\pupil_test-SB-2024-07-29\videos')
DATA_PATH = (r'E:\pupil_test-SB-2024-07-29\videos\240701_sb7_grat_6_DLCDLC_Resnet50_pupil_testJul29shuffle2_snapshot_200_full.pickle')
SAVE_CSV = (r'D:\Resources\DeepLabCut\Pupil\pupil_test-SB-2024-07-29\analysis')

#%% GET FILE LIST
import pathlib

data_file_list = []
for file in pathlib.Path(DIRECTORY).glob('*full.pickle'):
    data_file_list.append(file)

#%% LOAD FUNCTIONS

def load_df_from_file(path=DATA_PATH):
    """ Load a DataFrame from a pickle file """
    unpickled_data = pd.read_pickle(path) #unpickles full.pickle file
    print('loading file...')
    new_df = pd.DataFrame(data = unpickled_data)
    return new_df

def coordinates_array(new_df: pd.DataFrame):
    """ return row 8 from all columns of a dataframe 'new_df' """
    return new_df.iloc[8, :]

def euclidean_distance(point1, point2):
    """ Calculate the Euclidean distance between two points """
    return math.dist(point1, point2)

#%% LOAD DATA
# Note, this script will look for the ['coordinates'] row in the DataFrame

raw_dataframe = load_df_from_file(DATA_PATH) # new_df = whatever load_file 'returns'
print(raw_dataframe)

#%% SLICE FRAME COORDINATES INTO A LIST OF ARRAYS

# Initialize an empty list to store the coordinate arrays
frame_coordinates_array = []

# Iterate through each column in the DataFrame
for frame in raw_dataframe.columns:
    # Extract the 'coordinates' row from the current column
    coordinates_list = raw_dataframe.at['coordinates', frame]
    
    # Convert the extracted data to a numpy array
    coordinates_array = np.array(coordinates_list)
    
    # Append the numpy array to the list of coordinate arrays
    frame_coordinates_array.append(coordinates_array)

# Now coordinate_arrays contains the list of arrays for each frame
print(frame_coordinates_array)

#%% AVERAGE DIAMETER FOR EACH FRAME

# Initialize an empty list to store the averaged diameter for each frame
pupil_diameters = []

# Iterate through each array of coordinates of each frame
for coordinates in frame_coordinates_array[1:]: # skip the first item in the list (null metadata)
    # Initialize an empty list to store the diameters for the current frame
    frame_diameters = []

    #  in the current frame Iterate through each pair of coordinates
    for i in range(0, 7, 2): # 0, 2, 4, 6 results in (x_1, y_1) paired with (x_2, y_2), (x_3, y_3) and (x_4, y_4), etc.
        
        # Calculate the Euclidean distance between the two coordinate points using our custom euclidean_distance function
        diameter = euclidean_distance(coordinates[0,i,0,:], coordinates[0,i+1,0,:])
        
        # Append the calculated diameter to the list of diameters for the current frame
        frame_diameters.append(diameter)
    
    # Calculate the mean diameter for the current frame
    mean_diameter = st.mean(frame_diameters)

    
    # Append the mean diameter to the list of diameters for all frames
    pupil_diameters.append(mean_diameter)

#%%
# Now diameters contains the list of distances for each frame
print(pupil_diameters)

#%% PLT PUPIL DIAMETERS

import matplotlib.pyplot as plt

# Set the DPI for the plot
plt.figure(dpi=300)
color = 'blue'  # You can change this to any color you like

# Plot the pupil diameters with the specified color
plt.plot(pupil_diameters, color=color)
plt.xlabel('Frame')
plt.ylabel('Diameter')
plt.show()
#%% PLOT INDIVIDUAL FRAME COORDINATES

# get one frame's coordinates and cast list to a numpy array
def plot_frame_coordinates(raw_dataframe: pd.DataFrame, frame_number: int):
    one_coord_frame = raw_dataframe.iloc[8, frame_number] # get one frame's coordinates
    coords = one_coord_frame[0] # get the list of arrays from the Tuple
    coords = np.array(coords) # cast the list to a Numpy array

    # Initialize the plot
    plt.figure(dpi=300)
    color = 'red'

    # Plot the x and y coordinates of the pupil
    plt.scatter(coords[:, 0, 0], coords[:, 0, 1], color=color)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()


#%%

#TODO Linear interpolation or qubic spline interpolation
#TODO Use confidence intervals to determine blinks
#TODO Integrate the timestamps for the frames
#TODO Plot labeled coordinate points on a grid defined by the pixels of the video frames
#TODO Use common interesection point as a means to calculate pupil movement