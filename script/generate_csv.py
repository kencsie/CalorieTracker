# -*- coding: utf-8 -*-
"""generate_csv.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xYBhRiuO2BadU-S7RcthER_bAqGqLdIj
"""

# -*- coding: utf-8 -*-
"""generate_csv.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Oy4zmYiUwzhMi5UNMpTwGLMNLutGZznB
"""

import subprocess
import numpy as np
import csv
import os
import torch
import cv2

HOME = os.getcwd()
# print("HOME:", HOME)

"""**Download dataset from Roboflow**"""

dataset_path = os.path.join(HOME, "Food-7")
if not os.path.exists(dataset_path):
    subprocess.run(["pip", "install", "roboflow"])

    from roboflow import Roboflow
    rf = Roboflow(api_key="lttzJNap0h9lODifvr4O")
    project = rf.workspace("school-yrws4").project("food-pion4")
    dataset = project.version(7).download("yolov5")

"""**Write on CSV file with the annotation files**"""

def process_label_file(file_path):
    objects = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 5:  # Ensure there are 5 elements in the line
                object_id, x_center, y_center, width, height = map(float, parts)
                objects.append([object_id, x_center, y_center, width, height, '', '', ''])  # Leaving area and mass empty
    return objects

def get_processed_images(csv_file):
    processed_images = set()
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip header
            for row in reader:
                if row:
                    processed_images.add(row[0])
    return processed_images

def adjust_image_name(image_name):
    for ext in ['jpg', 'jpeg']:
        index = image_name.find('_' + ext)
        if index != -1:
            return image_name[:index]
    return image_name  # Return original name if no match

def process_dataset(dataset_path, output_csv):
    processed_images = get_processed_images(output_csv)
    data_to_write = []
    for folder in ['train', 'test', 'valid']:
        label_path = os.path.join(dataset_path, folder, 'labels')
        for label_file in os.listdir(label_path):
            if label_file.endswith('.txt'):
                image_name = label_file.replace('.txt', '')
                adjusted_image_name = adjust_image_name(image_name)
                if adjusted_image_name not in processed_images:
                    objects = process_label_file(os.path.join(label_path, label_file))
                    for obj in objects:
                        data_to_write.append([adjusted_image_name] + obj)

    return data_to_write

def write_to_csv(data, output_csv):
    if_exist = os.path.exists(output_csv)
    mode = 'a' if if_exist else 'w'
    with open(output_csv, mode, newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        if not if_exist:
          csv_writer.writerow(['image_name', 'object_id', 'x_center', 'y_center', 'width', 'height', 'image_area', 'area', 'mass'])
        csv_writer.writerows(data)

def sort_csv_data(csv_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        sorted_data = sorted(reader, key=lambda x: x[0])  # Sort by image name

    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(sorted_data)

output_csv = os.path.join(HOME, "output.csv")
data_to_write = process_dataset(dataset_path, output_csv)

write_to_csv(data_to_write, output_csv)
sort_csv_data(output_csv)

"""**Load SAM**"""

subprocess.run(["pip", "install", "-q", "git+https://github.com/facebookresearch/segment-anything.git"])

subprocess.run(["pip", "install", "-q", "jupyter_bbox_widget", "dataclasses-json", "supervision"])

subprocess.run(["mkdir", "-p", f"{HOME}/weights"])
CHECKPOINT_PATH = os.path.join(HOME, "weights", "sam_vit_h_4b8939.pth")
if not os.path.exists(CHECKPOINT_PATH):
    subprocess.run(["wget", "-q", "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth", "-P", f"{HOME}/weights"])

# print(CHECKPOINT_PATH, "; exist:", os.path.isfile(CHECKPOINT_PATH))

DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
MODEL_TYPE = "vit_h"

from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH).to(device=DEVICE)

# print(sam.device)

mask_predictor = SamPredictor(sam)

"""**Calculate areas and rewrite on CSV file**"""

#     # Replace the original file with the updated temp file
#     os.remove(csv_file)
#     os.rename(temp_file, csv_file)

import supervision as sv

def process_images_and_create_masks(dataset_path, csv_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header
        csv_data = list(reader)

    rows_temp = []
    for folder in ['train', 'test', 'valid']:
        image_folder_path = os.path.join(dataset_path, folder, 'images')
        for image_file in os.listdir(image_folder_path):
            image_name = os.path.splitext(image_file)[0]
            adjusted_image_name = adjust_image_name(image_name)

            IMAGE_PATH = os.path.join(image_folder_path, image_file)
            image_bgr = cv2.imread(IMAGE_PATH)
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

            info = []
            need_process = False
            for row in csv_data:
                if row[0] == adjusted_image_name:
                    info.append(row)
                    if (row[6]==''):
                        need_process = True

            if need_process:
                mask_predictor.set_image(image_rgb)
                for row in info:
                    if (row[6]==''):
                        x_center, y_center, width, height = map(float, row[2:6])
                        id = row[1]
                        x_min = (x_center * 640) - (width *640) / 2
                        y_min = (y_center * 640) - (height *640) / 2
                        x_max = (x_center * 640) + (width *640) / 2
                        y_max = (y_center * 640) + (height *640) / 2

                        bbox = np.array([x_min, y_min, x_max, y_max])

                        masks, scores, logits = mask_predictor.predict(
                            box=bbox,
                            multimask_output= True
                        )
                        image_area = np.count_nonzero(masks[2])

                        # visualize the mask with sv
                        # sv.plot_images_grid(
                        #     images=masks,
                        #     grid_size=(1, 4),
                        #     size=(16, 4)
                        # )

                        # box_annotator = sv.BoxAnnotator(color=sv.Color.red())
                        # mask_annotator = sv.MaskAnnotator(color=sv.Color.red(), color_lookup=sv.ColorLookup.INDEX)

                        # detections = sv.Detections(
                        #     xyxy=sv.mask_to_xyxy(masks=masks),
                        #     mask=masks
                        # )
                        # detections = detections[detections.area == np.max(detections.area)]

                        # source_image = box_annotator.annotate(scene=image_bgr.copy(), detections=detections, skip_label=True)
                        # segmented_image = mask_annotator.annotate(scene=image_bgr.copy(), detections=detections)

                        # sv.plot_images_grid(
                        #     images=[source_image, segmented_image],
                        #     grid_size=(1, 2),
                        #     titles=['source image', 'segmented image']
                        # )

                        # print(f"{adjusted_image_name} {id} {image_area}")
                        row[6] = image_area

                # Reset image
                mask_predictor.reset_image()
                torch.cuda.empty_cache()

            coin_image = 0
            coin_area = (13**2) * np.pi  # coin area in mm^2
            for obj in info:
                if float(obj[1]) == 2.0:
                    coin_image = float(obj[6])

            for obj in info:
                if float(obj[1]) != 2.0:
                    if obj[7] == '' and coin_image != 0:
                        S = float(obj[6]) / float(coin_image) * coin_area
                        obj[7] = S
                        rows_temp.append(obj)
                    else:
                        rows_temp.append(obj)

    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['image_name', 'object_id', 'x_center', 'y_center', 'width', 'height', 'image_area', 'area', 'mass'])
        writer.writerows(rows_temp)
    sort_csv_data(csv_file)

process_images_and_create_masks(dataset_path, output_csv)

# sam.to('cpu')
# del sam
# del mask_predictor
torch.cuda.empty_cache()