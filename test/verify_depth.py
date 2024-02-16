import numpy as np
import os
import glob
from PIL import Image

def normalize_depth_for_display(depth):
    depth_normalized = (depth - np.min(depth)) / (np.max(depth) - np.min(depth))
    depth_normalized = (depth_normalized * 255).astype(np.uint8)
    return depth_normalized


# Replace 'path_to_your_npy_file.npy' with the actual path to your .npy file
npy_file_path = './input/Food-18/test/depths/20231106_115308_jpg.rf.1767faa5ab150f7b9999e51e59515919_depth.npy'

# Load the array
depth_metric_array = np.load(npy_file_path)
depth_normalized = normalize_depth_for_display(depth_metric_array)
depth_image = Image.fromarray(depth_normalized)

# Construct a file name for the depth map image
base_name = os.path.basename(npy_file_path)
depth_map_file_name = os.path.splitext(base_name)[0] + '_depth_map.png'
depth_map_path = os.path.join("./", depth_map_file_name)

depth_image.save(depth_map_path)
print(f"Saved depth map to {depth_map_path}")