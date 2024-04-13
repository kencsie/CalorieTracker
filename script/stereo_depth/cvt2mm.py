import os
import cv2 as cv
import numpy as np


def main():
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.startswith('.'):
                os.remove(os.path.join(root, file))

            if file == "depth_in_meters.npy":
                # Load the numpy file
                depth_file = np.load(os.path.join(root, file))

                # Convert to millimeters and set datatype to uint16
                depth_in_mm = np.uint16(depth_file * 1000)

                # Overwrite the original depth image as a 16 bit png
                cv.imwrite(os.path.join(root, "depth_no_cm.png"), depth_in_mm)

                # Write to an npy file
                np.save(os.path.join(root, "depth_in_millimeters.npy"), depth_in_mm)


if __name__ == "__main__":
    main()
