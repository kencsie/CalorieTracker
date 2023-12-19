import torch
from torchvision.models import resnet50, ResNet50_Weights
import torchvision.transforms as transforms
from PIL import Image

# Load the pre-trained ResNet50 model
weights = ResNet50_Weights.DEFAULT
resnet50_model = resnet50(weights=weights)

# Remove the last fully connected layer (classifier)
# resnet50_model.children() returns iterator
resnet50_model = torch.nn.Sequential(*(list(resnet50_model.children())[:-1]))
#for child in resnet50_model.children():
#    print(child, end='\n\n')

resnet50_model.eval()

#Preprocess the Image
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    #It changes the pixel intensity values from the range [0, 255] (standard for images) to [0.0, 1.0].
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

img = Image.open("1.jpg")
img_t = preprocess(img)
#Add extra dimension to simulate batch: [3,224,224] -> [1,3,224,224]
batch_t = torch.unsqueeze(img_t, 0)

with torch.no_grad():
    features = resnet50_model(batch_t)

    # Flatten the features for use in an MLP
    features = torch.flatten(features, start_dim=1)
    print(features.shape)
    print(features)
