import os
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

ROOT_PATH = "./20240411_Organized"
train = []
test = []

for height in os.listdir(ROOT_PATH):
  for item in os.listdir(os.path.join(ROOT_PATH, height)):
    orientations = os.listdir(os.path.join(ROOT_PATH, height, item))
    for i, orientation in enumerate(orientations):
      ori_path = os.path.join(ROOT_PATH, height, item, orientation)
      data = Dataset(os.path.join(ori_path,"rgb.jpg"), os.path.join(ori_path,"depth_no_cm.png"))
      if i == len(orientations) - 1:  # If it's the last orientation
        test.append(data)
      else:
        train.append(data)

# Write train data to train.txt
with open('food_train_files_with_gt.txt', 'w') as f:
    for data in train:
        f.write(f'{data.rgb[1:]} {data.depth[1:]} {data.intrinsic}\n')

# Write test data to test.txt
with open('food_test_files_with_gt.txt', 'w') as f:
    for data in test:
        f.write(f'{data.rgb[1:]} {data.depth[1:]} {data.intrinsic}\n')
