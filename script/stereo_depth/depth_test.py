import os
import cv2 as cv
import numpy as np
import pyrealsense2 as rs
from datetime import datetime

FRAME_WIDTH  = 1280
FRAME_HEIGHT = 720
FRAME_RATE   = 30
CROP_WIDTH   = 640


def crop_images(color_img, depth_cm, depth_img):
    # Get image dimensions
    height, width, _ = depth_cm.shape

    # Crop the depth image to 640x 640 from the center
    start_x = (width // 2) - (CROP_WIDTH // 2)
    start_y = (height // 2) - (CROP_WIDTH // 2)

    cropped_color = color_img[start_y: start_y + CROP_WIDTH, start_x: start_x + CROP_WIDTH]
    cropped_depth_cm = depth_cm[start_y: start_y + CROP_WIDTH, start_x: start_x + CROP_WIDTH]
    cropped_depth = depth_img[start_y: start_y + CROP_WIDTH, start_x: start_x + CROP_WIDTH]

    return cropped_color, cropped_depth_cm, cropped_depth


def apply_filters(depth_frame):
    """
    Initialize the following filters:
        - Spatial filter to reduce localized noise
        - Temporal filter to reduce noise between frames
        - Hole filling filter to remove the gaps in the depth frames
    """
    sp_filter = rs.spatial_filter()
    tp_filter = rs.temporal_filter()
    hf_filter = rs.hole_filling_filter()

    # Apply filters
    depth_frame = sp_filter.process(depth_frame)  # Smooth locally
    depth_frame = tp_filter.process(depth_frame)  # Smooth between frames
    depth_frame = hf_filter.process(depth_frame)  # Fill in remaining gaps

    return depth_frame


def main():
    # Create pipeline and configuration objects
    pipeline = rs.pipeline()
    config   = rs.config()

    # Initialize our RGB and Depth streams
    config.enable_stream(rs.stream.color, FRAME_WIDTH, FRAME_HEIGHT, rs.format.bgr8, FRAME_RATE)
    config.enable_stream(rs.stream.depth, FRAME_WIDTH, FRAME_HEIGHT, rs.format.z16 , FRAME_RATE)

    # Start the camera frame streams
    pipeline.start(config)

    save_count = 0
    while True:
        # Get frames when they become available
        frame = pipeline.wait_for_frames()
        depth_frame = frame.get_depth_frame()
        color_frame = frame.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # Apply filters to depth frame
        depth_frame = apply_filters(depth_frame)

        # Convert images to numpy arrays (they aren't in a format we can use right away)
        depth_img = np.asanyarray(depth_frame.get_data())
        color_img = np.asanyarray(color_frame.get_data())

        # Apply color map to the depth frame for better visualization
        depth_cm = cv.applyColorMap( cv.convertScaleAbs(depth_img, alpha=0.5), cv.COLORMAP_JET )

        # Crop images
        cropped_color, cropped_depth_cm, cropped_depth = crop_images(color_img, depth_cm, depth_img)

        # Show images horizontally (concatenate them)
        concat_img = cv.hconcat([cropped_color, cropped_depth_cm])
        cv.imshow("Depth Test", concat_img)

        # TODO: Probably want to change the name of the folder from the date and time to just the date
        # Save cropped color and depth images to disk. Write the depth in meters to a numpy file
        if cv.waitKey(1) == ord('p'):
            # Get current date and time
            date_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # YYYYMMDD_hhmmss

            # Create directory for that file
            folder_path = os.path.join(os.getcwd(), date_time)
            os.makedirs(folder_path, exist_ok=True)

            # Write color image to disk
            cv.imwrite(f"{folder_path}/{date_time}.png", cropped_color)

            # Write depth image to disk (color map)
            cv.imwrite(f"{folder_path}/{date_time}_depth_color_map.png", cropped_depth_cm)

            # Write the depth in meters and write to numpy file
            depth_in_meters = cropped_depth / 1000.0
            np.save(f"{folder_path}/{date_time}_depth_in_meters.npy", depth_in_meters)
            print(f"Image {save_count + 1} Successfully Saved!")
            save_count += 1

            key_pressed = None  # Reset key_pressed

        elif cv.waitKey(1) == ord('q'):
            break

    # Free the pipeline
    pipeline.stop()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
