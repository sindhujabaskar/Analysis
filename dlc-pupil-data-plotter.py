# purpose: unpickling dlc output for pupil analysis 
#%% GET LIBRARIES

import pandas as pd
import numpy as np
import math
import statistics as st
import pathlib
import matplotlib.pyplot as plt


#%% SET FILE DIRECTORIES

DIRECTORY = (r'/Volumes/Sinbas_Stuf/Resources/DeepLabCut/Pupil/Pupil_Diameter-SB-2024-11-06/videos')
DATA_PATH = (r'//Volumes/Sinbas_Stuf/Resources/DeepLabCut/Pupil/Pupil_Diameter-SB-2024-11-06/videos/sub-SB03_ses-01_20240807_133242DLC_Resnet50_Pupil_DiameterNov6shuffle1_snapshot_200_full.pickle')
#SAVE_CSV = (r'D:\Resources\DeepLabCut\Pupil\pupil_test-SB-2024-07-29\analysis')


#%% GET FILE LIST

# 241022 Note- this does not currently list all full.pickle files SB

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

def euclidean_distance(coord1, coord2):
    """ Calculate the Euclidean distance between two points """
    return math.dist(coord1, coord2)

#%% LOAD DATA
# Note, this script will look for the ['coordinates'] row in the DataFrame

raw_dataframe = load_df_from_file(DATA_PATH) # new_df = whatever load_df_from_file 'returns'
print(raw_dataframe)


#%% SLICE FRAME COORDINATES AND CONFIDENCE INTO LIST OF ARRAYS

# Initialize an empty list to store the coordinate and confidence arrays
frame_coordinates_array = []
frame_confidence_array = []

# Iterate through each column in the DataFrame
for frame in raw_dataframe.columns:
    # Extract the 'coordinates' row from the current column
    coordinates_list = raw_dataframe.at['coordinates', frame]
    
    # Extract the 'confidence' row from the current column
    confidence_list = raw_dataframe.at['confidence', frame]
    
    # Convert the extracted data to a numpy array
    coordinates_array = np.array(coordinates_list)
    confidence_array = np.array(confidence_list)
    
    # Append the numpy array to the list of coordinate arrays
    frame_coordinates_array.append(coordinates_array)
    
    # Append the numpy array to the list of coordinate arrays
    frame_confidence_array.append(confidence_array)

# Now frame_''_array contains the list of arrays for each frame
print(frame_coordinates_array)
print(frame_confidence_array)


#%% LABEL COORDINATES BASED ON CONFIDENCE 

def confidence_filter_coordinates(frame_coordinates_array, frame_confidence_array, threshold):
    
    #Initialize an empty list to store the threshold-labeled list of coordinates
    thresholded_frame_coordinates = []
    
    #Zip the coordinate and its confidence into a pair, skipping the first item in the list (null metadata)
    for coordinates, confidence in zip(frame_coordinates_array[1:], frame_confidence_array[1:]): 
        
        # Initialize lists to store coords, conf, and label for current frame
        frame_coords = []
        frame_conf = []
        frame_label = []
        
        # Per frame, iterate through zip pairs 
        for i in range(8):
            
            # Get coordinate and confidence value
            coord = coordinates[0,i,0,:]
            conf = confidence[i,0,0]
            
            # Assign True/False boolean label to each coordinate based on confidence criteria
            label: bool = False
            if conf >= threshold:
                label = True 
                
            # Append the filtered frame values for coords, conf, and label
            frame_coords.append(coord)
            frame_conf.append(conf)
            frame_label.append(label)
            
        # Append the list of filtered coordinates with bool label
        thresholded_frame_coordinates.append([frame_coords, frame_conf, frame_label])
                
    return thresholded_frame_coordinates

threshold = 0.1

# Cast list of thresholded coordinates to a DataFrame
labeled_frames = confidence_filter_coordinates(frame_coordinates_array, frame_confidence_array, threshold)
print(labeled_frames)

#%% AVERAGE DIAMETER FOR EACH FRAME

# Initialize an empty list to store the averaged diameter for each frame
pupil_diameters = []
# Iterate through each array of coordinates of each frame
for frame in labeled_frames: 
    # Initialize an empty list to store the diameters for the current frame
    frame_diameters = []
    
    # In the current frame iterate through each pair of coordinates
    for i in range(0, 7, 2): # 0, 2, 4, 6 results in (x_1, y_1) paired with (x_2, y_2), (x_3, y_3) and (x_4, y_4), etc.
        # Set conditional that both coordinates must have True labels to be included in diameter calculation
        if frame[2][i] and frame[2][i+1]:
            # Calculate the Euclidean distance between each coordinate pair using our custom euclidean_distance function
            diameter = euclidean_distance(frame[0][i], frame[0][i+1])
           # Append the calculated diameter to the list of diameters for the current frame
            frame_diameters.append(diameter)
        
    # Calculate mean if current frame has more than one diameter
    if len(frame_diameters) > 1:
        mean_diameter = st.mean(frame_diameters)
        
    else:
        # If frame has less than one diameter, mean diameter is appended with NaN value
        mean_diameter = None

    # Append the mean diameter to the list of diameters for all frames
    pupil_diameters.append(mean_diameter)
    
# Convert mean pupil diameter to Pandas Series
pupil_diameters = pd.Series(pupil_diameters)
# Use Linear Interpolation to fill in mean diameter for excluded frames
pupil_diameters.interpolate()
    
# Now diameters contains the list of distances for each frame
print(pupil_diameters)


#%% PLOT PUPIL DIAMETERS

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


#%% TODO

#TODO Linear interpolation or qubic spline interpolation
#TODO Convert pupil diameter to mm 
#TODO Integrate the timestamps for the frames
#TODO Plot labeled coordinate points on a grid defined by the pixels of the video frames
#TODO Use common interesection point as a means to calculate pupil movement