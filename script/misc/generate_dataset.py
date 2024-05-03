import os
import random
from dataclasses import dataclass

@dataclass
class Dataset:
  rgb: str
  depth: str
  intrinsic: str

  def __init__(self, rgb, depth):
    self.rgb = rgb
    self.depth = depth
    self.intrinsic = "897.655"

ROOT_PATH = "./food_dataset/"
food_data = []

for date in os.listdir(ROOT_PATH):
  for item in os.listdir(os.path.join(ROOT_PATH, date)):
    for height in os.listdir(os.path.join(ROOT_PATH, date, item)):
      orientations = os.listdir(os.path.join(ROOT_PATH, date, item, height))
      for i, orientation in enumerate(orientations):
        ori_path = os.path.join(ROOT_PATH, date, item, height,orientation)
        item_dir = os.listdir(ori_path)
        item_dir.sort()
        #print(item_dir)
        rgb_pic = item_dir[0]
        depth_pic = item_dir[4]
        food_data.append(Dataset(os.path.join(ori_path, rgb_pic), os.path.join(ori_path, depth_pic)))

# Randomly shuffle the data
random.shuffle(food_data)

# Split the data into training and testing sets (80% training, 20% testing)
split_index = int(0.8 * len(food_data))
print(split_index)
train_data = food_data[:split_index]
test_data = food_data[split_index:]

# Write train data to train.txt
with open('food_train_files_with_gt.txt', 'w') as f:
    for data in train_data:
        f.write(f'{data.rgb[1:]} {data.depth[1:]} {data.intrinsic}\n')

# Write test data to test.txt
with open('food_test_files_with_gt.txt', 'w') as f:
    for data in test_data:
        f.write(f'{data.rgb[1:]} {data.depth[1:]} {data.intrinsic}\n')
