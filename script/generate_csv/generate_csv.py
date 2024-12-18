import subprocess
import numpy as np
import csv
import os
import torch
import cv2
import supervision as sv

HOME = os.getcwd()
VERSION = 21
# print("HOME:", HOME)

"""**Download dataset from Roboflow**"""

dataset_path = os.path.join(HOME, f"Food-{VERSION}")
if not os.path.exists(dataset_path):
    subprocess.run(["pip", "install", "roboflow"])

    from roboflow import Roboflow
    rf = Roboflow(api_key="")
    project = rf.workspace("school-yrws4").project("food-pion4")
    dataset = project.version(VERSION).download("yolov5")

"""**Write on CSV file with the annotation files**"""

def preprocess_file_name(file_path):
      concatenated_lines = {}
      with open(file_path, 'r') as file:
          for line in file:
              parts = line.strip().split()
              line_id = parts[0]

              if line_id in concatenated_lines:
                  concatenated_lines[line_id] += ' ' + ' '.join(parts[1:])
              else:
                  concatenated_lines[line_id] = ' '.join(parts[1:])

      #print(concatenated_lines)
      #with open('./data.json', 'w') as file:
      #  json.dump(concatenated_lines, file, indent=4)
      return concatenated_lines

def process_label_file(file_path):
    concatenated_lines = preprocess_file_name(file_path)
    objects = []
    for line_id in concatenated_lines:
        line = concatenated_lines[line_id]
        parts = line.strip().split()
        parts_float = [float(coord) for coord in parts]
        num_vertices = len(parts_float) // 2
        assert len(parts_float) % 2 == 0, "The number of coordinates should be even."
        
        polygon = np.array(parts_float).reshape(num_vertices, 2)   
        bounding_box = sv.polygon_to_xyxy(polygon)
        #print(bounding_box)

        if len(bounding_box) == 4:  # Ensure there are 4 elements for bounding box
            object_id, x_center, y_center, width, height = map(float, np.concatenate([[float(line_id)], bounding_box]))
            objects.append([object_id, x_center, y_center, width, height, '', '', ''])  # Leaving area and mass empty
    return objects

def process_image_mass(file_path):
    concatenated_lines = preprocess_file_name(file_path)
    image_mass_list = []
    for line_id in concatenated_lines:
        line = concatenated_lines[line_id]

        parts = line.strip().split()

        if not parts:
            continue

        parts_float = [float(coord) for coord in parts]
        num_vertices = len(parts_float) // 2
        assert len(parts_float) % 2 == 0, "The number of coordinates should be even."
        
        polygon = np.array(parts_float).reshape(num_vertices, 2)   
        #Convert from polygon to mask
        mask = sv.polygon_to_mask((polygon*640).astype(int), (640,640))
        #Count nonzero pixels
        image_area = np.count_nonzero(mask)
        image_mass_list.append(image_area)
            
    return image_mass_list

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
    for folder in ['train']:
        label_path = os.path.join(dataset_path, folder, 'labels')
        for label_file in os.listdir(label_path):
            if label_file.endswith('.txt'):
                image_name = label_file.replace('.txt', '')
                adjusted_image_name = adjust_image_name(image_name)
                if adjusted_image_name not in processed_images:
                    objects = process_label_file(os.path.join(label_path, label_file))
                    image_areas = process_image_mass(os.path.join(label_path, label_file))
                    #print(objects)
                    #print(image_areas)
                    for obj, image_area in zip(objects, image_areas):
                        #Replace image_area in obj with number
                        obj[5] = image_area
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
    for folder in ['train']:
        image_folder_path = os.path.join(dataset_path, folder, 'images')
        for image_file in os.listdir(image_folder_path):
            image_name = os.path.splitext(image_file)[0]
            adjusted_image_name = adjust_image_name(image_name)

            info = []
            need_process = False
            for row in csv_data:
                if row[0] == adjusted_image_name:
                    info.append(row)
                    if (row[6]==''):
                        need_process = True

            if need_process:
                raise Exception("The image_area should already be calculated.")

            coin_image = 0
            coin_area = (13**2) * np.pi  # coin area in mm^2
            for obj in info:
                if float(obj[1]) == 4.0:
                    coin_image = float(obj[6])

            for obj in info:
                if float(obj[1]) != 4.0:
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

'''
# sam.to('cpu')
# del sam
# del mask_predictor
torch.cuda.empty_cache()'''
