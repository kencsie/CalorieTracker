import csv
import os
import torch
import tqdm
import numpy as np
from PIL import Image
from torch import nn
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights

# Global Constants
IMG_LEN      = 640
HOME         = os.getcwd()
DATASET_PATH = os.path.join(HOME, "Food-14")

# Custom Multi Layer Perceptron Class
# class MLP(nn.Module):
#     def __init__(self, in_count: int, out_count: int = 1):
#         '''
#         Inputs:
#             - in_count  : Number of nodes in input layer
#             - out_count : Number of nodes in output layer
#         '''
#         super().__init__()
#         self.layers = nn.Sequential(
#                 nn.Linear(in_count, ),
#                 nn.ReLU(),
#                 nn.Linear(),
#                 nn.ReLU(),
#                 nn.Linear(, out_count),
#                 ) 
#         pass
#
#     def forward(self, x):
#         return self.layers(x)

def main():
    ########################
    # Image Preprocessing 
    ########################

    # Load the pre-trained ResNet50 model
    weights = ResNet50_Weights.DEFAULT
    resnet50_model = resnet50(weights=weights)

    # Remove the last fully connected layer (Classifier -> Regressor)
    # resnet50_model.children() returns iterator
    resnet50_model = torch.nn.Sequential(*(list(resnet50_model.children())[:-1]))
    resnet50_model.eval()

    # Preprocess the Image
    preprocess = transforms.Compose([
        transforms.Resize(256),     # Resize image to 256 * 256
        transforms.CenterCrop(224), # Crop image to 224 * 224

        # Normalize pixel intensity values from the range [0, 255] (standard for images) to [0.0, 1.0].
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    ########################
    # Image Loading
    ########################

    # Get output.csv file path
    csv_file_path = os.path.join(HOME, "output.csv")

    # Obtain image name, and bbox coordinates from each row
    box_info_list = list()
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            image_name, _, x_center, y_center, width, height, *_ = map(lambda x : x, row.values())

            # Calculate box coordinates
            x_min = (x_center * IMG_LEN) - (width  * IMG_LEN) / 2
            y_min = (y_center * IMG_LEN) - (height * IMG_LEN) / 2
            x_max = (x_center * IMG_LEN) + (width  * IMG_LEN) / 2
            y_max = (y_center * IMG_LEN) + (height * IMG_LEN) / 2

            box_info_list.append({
                'name'  : image_name + ".jpg"
                'x_min' : x_min 
                'y_min' : y_min 
                'x_max' : x_max 
                'y_max' : y_max 
            })

        # for box in box_info_list:
        #     print(box)

    # Load image and crop out the corresponding subimage
    image_list = list()
    for box in box_info_list:
        # TODO: Implement aquisition of these images (find the images within the folders of the dataset)
        with Image.open(box['name']) as image:
            region = image.crop()



        


    ########################
    # Feature Extraction
    ########################


    ########################
    # Model Training
    ########################

    # TODO: Instantiate model once design parameters are more clear
    model = None

    # Define loss function for regression
    loss_fn = nn.MSELoss()  # Mean Squared Error -> Popular because differentiable -> Not too useful as is

    # Define optimizer
    optimizer = torch.optim.Adam(model.parameters())

    # [OPTIONAL] Early Stopping (Stop when loss minimization has began to plateau for n-iterations)
    # es = EarlyStopping()

    epoch = 0
    done = False
    while epoch < 100 and not done:
        pass


# Entry Point
if __name__ == '__main__':
    main()
