import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import pyrealsense2 as rs
from datetime import datetime
from PIL import Image, ImageTk

# Constants
FRAME_WIDTH    = 1280
FRAME_HEIGHT   = 720
FRAME_RATE     = 30
CROP_WIDTH     = 640
COLOR_BLUE_BGR = (255, 0, 0)


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
    depth_frame = hf_filter.process(depth_frame)  # Fill in gaps gaps

    return depth_frame


def crop_images(color_img, depth_cm, depth_img):
    # Get image dimensions
    height, width, _ = depth_cm.shape

    # Crop the depth image to 640x 640 from the center
    start_x = (width // 2) - (CROP_WIDTH // 2)
    start_y = (height // 2) - (CROP_WIDTH // 2)

    cropped_color    = color_img[start_y: start_y + CROP_WIDTH, start_x: start_x + CROP_WIDTH]
    cropped_depth_cm = depth_cm[start_y: start_y + CROP_WIDTH, start_x: start_x + CROP_WIDTH]
    cropped_depth    = depth_img[start_y: start_y + CROP_WIDTH, start_x: start_x + CROP_WIDTH]

    return cropped_color, cropped_depth_cm, cropped_depth


class App:
    def __init__(self, window, window_title):
        self.photo = None  # The image in the viewfinder
        self.window = window
        self.window.title(window_title)

        # Configure depth and color streams from the RealSense camera
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, FRAME_WIDTH, FRAME_HEIGHT, rs.format.bgr8, FRAME_RATE)
        self.config.enable_stream(rs.stream.depth, FRAME_WIDTH, FRAME_HEIGHT, rs.format.z16 , FRAME_RATE)
        self.pipeline.start(self.config)

        # Init the Tkinter Canvas object
        self.canvas = tk.Canvas(window, width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.canvas.pack()

        # Button to capture a frame
        ttk.Style().configure('Large.TButton', font=('Helvetica', 32))
        self.btn_capture = ttk.Button(window, text="Capture Frame", style='Large.TButton', command=self.capture_frame)
        self.btn_capture.pack(anchor=tk.CENTER, expand=True, padx=10, pady=5)

        # Begin updating the viewfinder
        self.update()

    def capture_frame(self):
        # Get frames from camera
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            return

        # Apply filters to depth frame
        depth_frame = apply_filters(depth_frame)

        # Convert frame to numpy array
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        # Apply color map to the depth frame for better visualization
        depth_cm = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.5), cv2.COLORMAP_JET)

        # Crop images
        cropped_color, cropped_depth_cm, cropped_depth = crop_images(color_image, depth_cm, depth_image)

        # Convert cropped depth image to meters
        depth_in_meters = cropped_depth / 1000.0

        # Construct Save Path
        date = datetime.now().strftime("%Y%m%d")  # YYYYMMDD
        time = datetime.now().strftime("%H%M%S")  # HHMMSS
        os.makedirs(f"./{date}", exist_ok=True)
        save_path = f"./{date}/{time}"  # "./20240407/030937"

        # Save images
        cv2.imwrite(f"{save_path}_rgb.jpg", cropped_color)
        cv2.imwrite(f"{save_path}_cm.png", cropped_depth_cm)
        np.save(f"{save_path}_depth_in_meters.npy", depth_in_meters)

        print(f"Data saved to: {os.getcwd()}\\{date}")  # For debugging; remove or comment out in production

    def update(self):
        # Get frame from camera
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        # Apply filters to depth image
        depth_frame = apply_filters(depth_frame)

        if depth_frame:
            # Convert from frame to numpy array
            depth_image = np.asanyarray(depth_frame.get_data())

            # Apply color map to the depth frame for better visualization
            depth_cm = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.5), cv2.COLORMAP_JET)

            # Calculate box coordinates
            height, width = depth_image.shape
            start_x = (width // 2) - (CROP_WIDTH // 2)
            start_y = (height // 2) - (CROP_WIDTH // 2)

            # Draw rectangle on depth color map
            depth_cm = cv2.rectangle(
                depth_cm, (start_x, start_y), (start_x + CROP_WIDTH, start_y + CROP_WIDTH), COLOR_BLUE_BGR, 2
            )

            # Update viewfinder
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(depth_cm, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def __del__(self):
        self.pipeline.stop()


if __name__ == '__main__':
    # Create the Tkinter window
    root = tk.Tk()

    # Set the window title and size (optional)
    root.title("RealSense Camera Viewer")
    root.geometry(f"{FRAME_WIDTH}x{FRAME_HEIGHT + 100}")  # Window needs extra height to show the button on start

    # Create and run the app
    app = App(root, "RealSense Camera Viewer")

    # Start the Tkinter event loop
    root.mainloop()
