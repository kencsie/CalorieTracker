import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Load the data from the .npy file
estimate_data = np.load('../data/output/20240423_144013_rgb.npy')
gt_data = np.load('../data/input/food_dataset/20240423/pineapple/height_2/144013/depth_in_millimeters.npy')

# Normalize the depth values to the range 0-1 for better visualization
normalized_gt_data = (gt_data - np.min(gt_data)) / (np.max(gt_data) - np.min(gt_data))
normalized_estimate_data = (estimate_data - np.min(estimate_data)) / (np.max(estimate_data) - np.min(estimate_data))

# Save the normalized depth map as a PNG file
plt.imsave('normalized_esti_depth_map.png', normalized_estimate_data, cmap='gray')
plt.imsave('normalized_gt_depth_map.png', normalized_gt_data, cmap='gray')


# Convert depth values from meters to millimeters
'''data_mm = data * 1000

# Cast to 16-bit unsigned integer
data_mm = data_mm.astype(np.uint16)

# Save the depth map in millimeters as a PNG file
Image.fromarray(data_mm).save('depth_map_mm.png')'''