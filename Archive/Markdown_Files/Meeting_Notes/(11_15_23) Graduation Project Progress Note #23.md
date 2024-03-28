# 組員
* 411021391 張晉睿
* 411021312 張愷恩
* 411021342 Kenrick Albert
* 411021365 Nguyễn Minh Trang

## Meeting Contents
Ken:
Demonstrate the way to create dataset on Roboflow, train, and test it
Trang:
General discussion on future plans for Nutrition System:

## Nutrition estimation system
### 1.	Recognition model:
***Dataset*** for training includes:
-	Images consisting of a plate of food items
-	Label (with bounding box information) of each item inside the image

***Input:*** An image of a food plate and a 10NT coin
***Output:*** Bounding box information and classification label of each food item in the image
Model: YOLOv5
Tool: Roboflow to plot the bounding box —> prepare the dataset for training the model

### 2.	Segmentation model:
***Dataset:***
-	Cropped images (from the original using the bounding box info) containing only 1 food item
-	Ground truth mask of that food item

***Input:*** A cropped image of 1 food item
***Output:*** The segmented image for that food item (with transparent background)
***Model:*** Can look at Mask R-CNN, U-Net, ENet, DeepLabV3 (later)
***Tool:*** Roboflow to create the ground truth mask for training the model (prepare the dataset)

Food area estimation using the predicted mask

### 3.	Weight estimation model (Regression model)
***Dataset:*** for each instance
-	Food class
-	Real area
-	Weight

***Input:*** food class and real area
***Output:*** Weight
***Model:*** need to choose an appropriate regression model to predict the weight based on the real area of a specific food item. Can use neural networks (study later)

Calorie and nutrition estimation based on estimated weight using a nutrition table(?)

### Note: 
- need to capture the food with top-down view (ideally 90 degrees) so that the ratio of the coin and the plate (with the food on top) is correct —> beneficial for the weight estimation model.
-	The 3rd model can be improved by adding more features (e.g: shape features (perimeter, aspect ratio, minimum bounding boxes), color features (color histograms, etc.), texture features, etc.), might consider after training with only 3 mentioned features —> might perform well with more photo angles other than 90 degrees —> harder to create the dataset

---

## What can be done now?
- Create and organize the dataset, and retrain the first model (recognition model) according to our needs
- Study the segmentation model (constrains for images in the dataset (if padding is needed), which model to use)
Some notable information:
  - CNNs often require fixed input dimensions, so padding might be needed, but it might affect the accuracy of segmentation.
  - FCNs are designed to work well with various input sizes —> might be more useful in our case when cropped images can vary in size
- Find reliable sources and start creating the nutrition table for calorie and nutrition estimation

## 分工 Division of Labour
Entire Team:
- Continue with collection of data at the Lakeside Restaurant