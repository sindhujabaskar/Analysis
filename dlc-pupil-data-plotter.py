# purpose: unpickling dlc output for pupil analysis 
#%%
#get libraries
import pandas as pd
import numpy as np
import math
import statistics as st

#%%
#set file directory
DATA_PATH = (r'E:\pupil_test-SB-2024-07-29\videos\240701_sb7_grat_6_DLCDLC_Resnet50_pupil_testJul29shuffle2_snapshot_200_full.pickle')
SAVE_CSV = (r'D:\Resources\DeepLabCut\Pupil\pupil_test-SB-2024-07-29\analysis')


#%% LOAD FUNCTIONS

# unpickle file and load into a new df
def load_df_from_file(path=DATA_PATH):
    unpickled_data = pd.read_pickle(path) #unpickles full.pickle file
    print('loading file...')
    new_df = pd.DataFrame(data = unpickled_data)
    return new_df

# create a new df with just the coordinates 
def coordinates_array(new_df: pd.DataFrame):
    """ return row 8 from all columns of a dataframe 'new_df' """
    return new_df.iloc[8, :]


#%% Run Functions

raw_dataframe = load_df_from_file(DATA_PATH) # new_df = whatever load_file 'returns'
raw_dataframe.at
coordinates_dataframe = coordinates_array(raw_dataframe) # gets the 8th row from every column of df
 
# get one frame's coordinates and cast list to a numpy array
one_coord_frame = raw_dataframe.iloc[8, 1] # get one frame's coordinates
coords = one_coord_frame[0] # get the list of arrays from the Tuple
coords = np.array(coords) # cast the list to a Numpy array

# create list indices for coords and empty list structure
p = [0, 2, 4, 6] # coords indices as a list 'p'
q = [1, 3, 5, 7] # coords indices as a list 'q'
diameters = [] # empty list structure 'diameters'

# calculate euclidean distance between even and odd pupil coordinate pair to get diameters
for index in range(4):
    even = p[index]
    odd = q[index]
    diameters.append(math.dist(coords[even,0,:], coords[odd,0,:])) 
print(diameters)

# calculation of mean per frame
st.mean(diameters) #calculate mean of all diameters for one frame

#%%
    
# DEV: iterate through each frame's coordinates and cast list to a numpy array
new_df = load_df_from_file() # new_df = whatever load_file 'returns'

frame_in_array = [] 
for frames in range(len(new_df.shape[8,:])):
    coord_values = new_df.iloc[8, frames]
    frame_in_array.append([coord_values])
    


each_frame_coord = new_df.iloc[8, :] # get one frame's coordinates
for i in each_frame_coord():
    
    coords2 = each_frame_coord[]
    coords2 = np.array(coords2)
    
  
#%% 241003 SB wrap-up
# try to make the math.dist into a function that you can later run to find st.mean(diameters)

# next step is to create another function for iterating through each column of coords to 
# get a final array of two columns, 1: frame# 2: avg diameter and save it as a csv (or w/e)

# finally, write a plot command to create a line plot of the pupil diameter across each frame



# Initialize an empty list to store the coordinate arrays
coordinate_arrays = []

# Iterate through each column in the DataFrame
for column in raw_dataframe.columns:
    # Extract the 'coordinates' row from the current column
    coordinates = raw_dataframe.at['coordinates', column]
    
    # Convert the extracted data to a numpy array
    coordinates_array = np.array(coordinates)
    
    # Append the numpy array to the list of coordinate arrays
    coordinate_arrays.append(coordinates_array)

# Now coordinate_arrays contains the list of arrays for each frame
print(coordinate_arrays)

#%%

# Function to calculate Euclidean distance between two points
def euclidean_distance(point1, point2):
    return math.dist(point1, point2)

# Initialize an empty list to store the diameters for each frame
diameters = []

# Iterate through each array in coordinate_arrays
for coordinates in coordinate_arrays[1:]:
    # Initialize an empty list to store the diameters for the current frame
    frame_diameters = []
    coordinates = coordinates.T
    # Iterate through each pair of coordinates in the current frame
    for i in range(0, 7, 2):
        # Calculate the Euclidean distance between the two points
        diameter = euclidean_distance(coordinates[0,i], coordinates[0,i+1])
        
        # Append the calculated diameter to the list of diameters for the current frame
        frame_diameters.append(diameter)
    
    # Calculate the mean diameter for the current frame
    mean_diameter = st.mean(frame_diameters)
    
    # Append the mean diameter to the list of diameters for all frames
    diameters.append(mean_diameter)


# Now diameters contains the list of distances for each frame
print(diameters)

#%% 241004 Jake's Help

p = [0, 2, 4, 6] # coords indices as a list 'p'
q = [1, 3, 5, 7] # coords indices as a list 'q'

def get_avg_frame_diameter(coords):
    diameters = [] # empty list structure 'diameters'

    for index in range(4):
        even = p[index]
        odd = q[index]
        diameters.append(math.dist(coords[even], coords[odd])) 
    return st.mean(diameters)
        

avg_diameters = []
#new_df.iloc[8, 1:]
for frame_coords in new_df.iloc[8, 1:]:
    frame_coords = pd.DataFrame(frame_coords).T
    avg_diameters.append(get_avg_frame_diameter(frame_coords))



# print('this is the end')
# the above forloop lists all the values per frame. now you need to direct it so that it only lists the values you want 
# (i.e. xy coordinates of pupil1, pupil2). after that, you want just those values to be put into a data frame where rows are 
# each frame and columns are pupil1 x, pupil1 y, pupil2 x, pupil2 y so that you can compute the pupil diameter per frame 
# and track across the entire session 

#create new dat Jaframe