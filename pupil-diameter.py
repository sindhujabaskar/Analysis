import math
import numpy as np
import statistics as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
def load_df_from_file(pickle_path):
    """ Load a DataFrame from a pickle file """
    unpickled_data = pd.read_pickle(pickle_path) #unpickles full.pickle file
    new_df = pd.DataFrame(data = unpickled_data)
    return new_df

# Calculation Functions
def confidence_filter_coordinates(frames_coords, frames_conf, threshold):
    """
    Apply a boolean label to coordinates based on whether 
    their confidence exceeds `threshold`.
    
    Parameters
    ----------
    frames_coords : list
        List of numpy arrays containing pupil coordinates for each frame.
    frames_conf : list
        List of numpy arrays containing confidence values corresponding 
        to the coordinates in `frames_coords`.
    threshold : float
        Confidence cutoff.

    Returns
    -------
    list
        A list of [coords, conf, labels] for each frame, where 'labels' 
        is a list of booleans (True if above threshold, else False).
    """
    thresholded = []
    for coords, conf in zip(frames_coords[1:], frames_conf[1:]):
        frame_coords, frame_conf, frame_labels = [], [], []
        # Each frame has 8 sets of pupil points 
        for i in range(8):
            point = coords[0, i, 0, :]
            cval = conf[i, 0, 0]
            label = (cval >= threshold)
            frame_coords.append(point)
            frame_conf.append(cval)
            frame_labels.append(label)
        thresholded.append([frame_coords, frame_conf, frame_labels])
    return thresholded

def euclidean_distance(coord1, coord2):
    """Calculate the Euclidean distance between two points."""
    return math.dist(coord1, coord2)

# Plot a single frame's coordinates

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


# Main Function
def process_deeplabcut_pupil_data(
    pickle_data: pd.DataFrame, show_plot: bool, confidence_threshold: float, pixel_to_mm: float) -> pd.DataFrame:
    """
    Load a DeepLabCut output pickle file and compute the pupil diameter per frame.
    
    Parameters
    ----------
    pickle_path : str
        Path to the DLC output pickle file (e.g., '*full.pickle').
    show_plot : bool
        If True, displays a matplotlib plot of pupil diameter (in mm) across frames.
        Defaults to False.
    confidence_threshold : float
        Minimum confidence required to include two landmarks in the diameter calculation.
        Defaults to 0.1.
    pixel_to_mm : float
        Conversion factor from pixels to millimeters. Defaults to 53.6.
    
    Returns
    -------
    pd.DataFrame
        A DataFrame with one column ('pupil_diameter_mm') indexed by frame number.
        Frames for which no valid diameter could be calculated will have NaN values.
    """
    
    # 1) Load the raw dataframe from the pickle
    raw_df = pickle_data

    # 2) Convert each column's 'coordinates' & 'confidence' to arrays
    frame_coordinates_array = []
    frame_confidence_array = []
    for frame_column in raw_df.columns:
        coords_list = raw_df.at['coordinates', frame_column]
        conf_list = raw_df.at['confidence', frame_column]
        frame_coordinates_array.append(np.array(coords_list))
        frame_confidence_array.append(np.array(conf_list))
    
    # 3) Filter coordinates by confidence
    labeled_frames = confidence_filter_coordinates(
        frame_coordinates_array,
        frame_confidence_array,
        confidence_threshold)
    
    # 4) Calculate mean pupil diameter (in pixels) per frame
    pupil_diameters = []
    for frame_data in labeled_frames:
        coords, conf, labels = frame_data
        frame_diameters = []
        
        # Pairs: (0,1), (2,3), (4,5), (6,7)
        for i in range(0, 7, 2):
            if labels[i] and labels[i+1]:
                diameter_pix = euclidean_distance(coords[i], coords[i+1])
                frame_diameters.append(diameter_pix)
        
        # If multiple diameters exist, use the average
        if len(frame_diameters) > 1:
            pupil_diameters.append(st.mean(frame_diameters))
        else:
            pupil_diameters.append(np.nan)
    
    # 5) Convert diameters to Series and interpolate missing values
    diam_series = pd.Series(pupil_diameters).interpolate()
    
    # 6) Convert from pixels to mm
    diam_series = diam_series / pixel_to_mm
    
    # 7) Optionally plot the results
    if show_plot is True:
        plt.figure(dpi=300)
        plt.plot(diam_series, color='blue')
        plt.xlabel('Frame')
        plt.ylabel('Pupil Diameter (mm)')
        plt.title('Pupil Diameter Over Frames')
        plt.show()
    
    # 8) Return a DataFrame with the final diameters
    result_df = pd.DataFrame({'pupil_diameter_mm': diam_series})
    return result_df

# Define path and run script
raw_df = load_df_from_file(r'D:\inbox\sub-SB03_ses-01_20240805_122757DLC_Resnet50_su24_etoh-vis_dlc-model_SB-AHJan16shuffle1_snapshot_200_full.pickle')
pupil_dimater_df = process_deeplabcut_pupil_data(raw_df,
    show_plot = False,
    confidence_threshold = 0.1,
    pixel_to_mm = 53.6 )
