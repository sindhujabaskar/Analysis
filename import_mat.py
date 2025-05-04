#%%
import scipy.io
import tifffile
import numpy as np
import os
import glob

def find_files(path):
    mat_files = glob.glob(os.path.join(path, '*.mat'))
    return mat_files


def load_files(mat_files):
    loaded= []
    for item in mat_files:
        loaded.append(scipy.io.loadmat(item))
    return loaded


def index_files(loaded):
    all_movies = []
    for item in loaded:
        data = item['movnew']
        all_movies.append(data)
    return all_movies


def set_mov_shape(all_movies):
    reshaped = []
    for item in all_movies:
        item.astype(np.uint8)
        data_array = np.transpose(item, (2, 0, 1))
        reshaped.append(data_array)
    return reshaped
   
def save_to_tiff(data_list, output_dir, base_filename="mov", metadata=None):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, data_array in enumerate(data_list):
        output_path = os.path.join(output_dir, f"{base_filename}{i + 1}.tiff")
        tifffile.imwrite(
            output_path,
            data_array,
            metadata=metadata or {'axes': 'ZYX'},
            imagej=True
        )

#%%

def main():
    path = r'C:\Users\Sipe_Lab\Documents\scripts\astrostim\visual\movies\movies'
    mat_files = find_files(path)
    loaded = load_files(mat_files)
    all_movies = index_files(loaded)
    shaped_movies = set_mov_shape(all_movies)

    save_to_tiff(shaped_movies, output_dir= r'C:\2P\Experiment Types\Natural Movies Experiment', base_filename='mov', metadata = {'axes': 'ZYX'})
#BUG- renumbers mov# after converting instead of maintaining originial mov number

if __name__ == "__main__": 
    main()




#%% 
"""
SINDHU BABY MADE THIS SO COOL
For converting a single .mat video file into a .tiff

Parameters
----------
path  :  str
File path for .mat file

Returns
-------
TIFF  
uint8 re-shaped .tiff file in save_dir that can be opened in imagej for easy viewing :)
"""
# load .mat file
mat_file = scipy.io.loadmat(r"C:\Users\Sipe_Lab\Documents\scripts\astrostim\visual\movies\movies\mov1.mat")
print(mat_file)
print(mat_file.keys())  # Print keys to see where the image array is 

data = mat_file['movnew'] # Extract the data from the dict
data_array = np.transpose(data, (2, 0, 1))  # Reorder to (Z, Y, X) 
print(f'reshaped:',{data_array.shape})  # Print the shape of the array to verify dimensions

data_array = data_array.astype(np.uint8) # cast as uint8 which is the original datatype as failsafe in case datatype changes somehow

# Save as a .tiff file, specifying axes as imageJ hyperstacks must be in TZCYXS order
tifffile.imwrite(r'C:\2P\Experiment Types\Natural Movies Experiment\mov1.tiff', data_array, metadata = {'axes':'ZYX'}, imagej=True) 


# %%
