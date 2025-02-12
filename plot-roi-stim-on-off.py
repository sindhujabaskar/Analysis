#%% IMPORT LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

#%% DEFINE FUNCTIONS

# load roi data
def load_roi_data(directory) -> pd.DataFrame:

    # Parse the directory for a file ending with 'roi_dff_data_robust.csv'
    path = os.path.join(os.path.dirname(directory), 'beh')
    for file in os.listdir(path):
        if file.endswith('roi_dff_data_robust.csv'):
            file_path = os.path.join(path, file)
            break
    if file_path is None:
        raise FileNotFoundError(f"No file ending with 'roi_dff_data_robust.csv' found in {path}.")
    # Load the CSV into a pandas DataFrame
    df = pd.read_csv(file_path)

        # Display the first few rows of the DataFrame
    print(df.head())

    # List the columns from the DataFrame
    print(df.columns)
    
    return df

# convert roi fluorescence from frames to seconds
def frames_to_seconds(roi_dff)
    for i in range(len(roi_dff)):
        roi_dff[i] = roi_dff[i] / 29.595 # fps from thorlabs imager output
    print(roi_dff)
    return roi_dff

# load stim data
def load_psychopy_data(directory):

    # Parse the beh_path directory for a file ending with '.csv'
    path = os.path.join(os.path.dirname(directory), 'beh')
    for file in os.listdir(path):
        if file.endswith('.csv'):
            file_path = os.path.join(path, file)
            break
    if file_path is None:
        raise FileNotFoundError(f"No file ending with '.csv' found in {path}.")
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Display the first few rows of the DataFrame
    print(df.head())

    # List the columns from the DataFrame
    print(df.columns)
    
    return df

# load wheel data
def load_wheel_data(directory) -> pd.DataFrame:

    # Parse the beh_path directory for a file ending with 'wheel_df.csv'
    path = os.path.join(os.path.dirname(directory), 'beh')
    for file in os.listdir(path):
        if file.endswith('wheeldf.csv'):
            file_path = os.path.join(path, file)
            break
    if file_path is None:
        raise FileNotFoundError(f"No file ending with 'wheeldf.csv' found in {path}.")
    df = pd.read_csv(file_path)
    # Create a pandas dataframe
    return df

# 

