# Step 1: Install the necessary libraries
# pip install ome-types tifffile
#%%
import tifffile
from ome_types import from_xml
#%%
file_path = r"F:\test_006\default_protocol-sub-default_subject_ses-default_session_task-default_task_007.ome.tif"

#%%

def parse_ome_tiff_metadata(file_path):
    # Step 2: Read the OME-TIFF file
    with tifffile.TiffFile(file_path) as tif:
        # Extract the OME-XML metadata
        ome_xml = tif.ome_metadata

    # Step 3: Parse the OME-XML metadata
    ome_metadata = from_xml(ome_xml)
    
    return ome_metadata

# Example usage
metadata = parse_ome_tiff_metadata(file_path)
print(metadata)
#%%
tif = tifffile.TiffFile(file_path)
ome_xml = tif.ome_metadata
ome_metadata = from_xml(ome_xml)

# %%
ome_metadata.