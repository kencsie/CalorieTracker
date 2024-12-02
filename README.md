# **CalorieTrackerPlus**

**Track Your Nutrition with Food Image Analysis**

## **Overview**

**CalorieTrackerPlus** is a web-based application designed to help users monitor and manage their daily nutritional intake effortlessly. By analyzing images of food, the application identifies food items, estimates portion sizes, and calculates nutritional values, providing users with detailed dietary insights. Additionally, the app offers tailored meal recommendations based on users’ physical characteristics and diet patterns, empowering them to make healthier choices.

---

## **Features**

- **Food Recognition**: Utilizes YOLOv5 to detect and identify food items from uploaded images.
- **Food Segmentation**: Implements the Segment Anything Model (SAM) for accurate food segmentation.
- **Dimension and Mass Estimation**: Leverages Depth Anything for dimensional analysis and Support Vector Regression (SVR) for food mass prediction.
- **Nutritional Analysis**: Provides comprehensive nutritional breakdowns for recognized food items.
- **Personalized Meal Recommendations**: Uses an LLM (GPT-4) to generate tailored recommendations based on users’ physical characteristics (e.g., age, weight, height) and dietary patterns.
- **User-Friendly Interface**: A simple, intuitive interface for easy navigation.

---

## **Technologies Used**

- **Machine Learning Models**: YOLOv5, SAM, Depth Anything, scikit-learn.
- **Recommender System**: GPT-4.
- **Backend**: Flask framework.
- **Database**: MongoDB for user data and meal tracking.
- **Languages/Tools**: Python, TorchHub, HTML/CSS, JavaScript.

---

## **Setup Instructions**

### **Prerequisites**

Before running the application, ensure the following are installed:

- Python 3.8 or higher
- MongoDB
- Pip (Python Package Installer)

### **Steps to Set Up and Run**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/CalorieTrackerPlus.git
   ```
2. **Navigate to the Application Directory**:
   ```bash
   cd DietAdvisorWeb
   ```
3. **Run the Application**:
   ```bash
   ./run.sh
   ```
   The application will start running locally at [http://localhost:5004](http://localhost:5004).

---

## **Screenshots and Demo Video**

### **Screenshots**

Here are some examples of the application's features:

1. **Meal Nutrient Analysis**:

   - The application detects food items from the image and calculates their nutritional content, providing users with detailed results.

     ![image](https://github.com/user-attachments/assets/12d89845-3d7d-491a-a7ef-c30c417e97ee)

2. **Nutrient Tracking**:

   - Users can track their nutrient intake (e.g., calories, carbs, fats, proteins) over the past week, helping them monitor their dietary habits.

   ![image](https://github.com/user-attachments/assets/e9fc90de-f95b-4eb2-b03e-68b7a54dd409)

3. **Personalized Meal Recommendations**:
   - The app generates customized meal plans based on users' physical characteristics and dietary goals.

     ![image](https://github.com/user-attachments/assets/d5388bbe-9861-4125-b91c-c7126499f0b0)

### **Demo Video**

For a complete walkthrough of the app's features, watch the demo video on Youtube: 👉[Demo Video](https://www.youtube.com/watch?v=GW8UuorKOcc)

---

## **Future Plans**

- **Expand Dataset**: Incorporate a wider variety of food items and cuisines for better recognition.
- **Mobile Integration**: Extend the application to Android and iOS platforms for broader accessibility.
- **Incorporate Stereo Vision**: Leverage stereo vision capabilities on devices equipped with multiple cameras (e.g., dual-camera phones) to enhance depth estimation accuracy and reduce reliance on external depth estimation models.

---

## **License**

This project is licensed under the MIT License.

---

## **Acknowledgements**

- **YOLOv5** by Ultralytics for object detection.
- **Segment Anything Model (SAM)** by Meta for precise food segmentation.
- **Depth Anything** for dimension estimation.
- **GPT-4** by OpenAI for personalized meal recommendations.
- **Team Members**: Kenrick Albert, Ken Chang, and Nguyen Minh Trang.
