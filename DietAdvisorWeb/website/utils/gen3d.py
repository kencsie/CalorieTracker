import os
import numpy as np
import open3d as o3d

# Using derived camera intrinsics for a 640x640 image for the Sony IMX586
WIDTH, HEIGHT = 640, 640
fx, fy = 360, 360 
cx, cy = WIDTH / 2, HEIGHT / 2

# Load the RGB and depth images (Hardcoded for now)
color_raw = o3d.io.read_image('../static/broccoli_original_test.jpg')

depth_raw = np.load('../data/depth_maps/20240428_192956_rgb.npy')
depth_raw = o3d.geometry.Image(depth_raw)

# Create Open3D camera intrinsics object
intrinsics = o3d.camera.PinholeCameraIntrinsic(WIDTH, HEIGHT, fx, fy, cx, cy)

# Create RGBD Image
rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
    color_raw,
    depth_raw,
    depth_scale=1000.0,  # Units are in mm
    depth_trunc=1.0,     # Truncate depth at 1 meter
    convert_rgb_to_intensity=False
)

# Generate PointClound from RGBD Image
pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, intrinsics)

# Visualize the pointcloud
o3d.visualization.draw_geometries([pcd])

