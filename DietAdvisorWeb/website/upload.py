from flask import Blueprint, request, redirect, flash, current_app, render_template, url_for
from werkzeug.utils import secure_filename
import os
import json
import torch
from urllib.parse import quote, unquote

upload = Blueprint('upload', __name__)

@upload.route('/upload', methods=['POST'])
def upload_file():
    def yolo_object_detection(image_path, output_path):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='./website/data/models/yolo.pt')
        model.eval()
        results = model(image_path)

        # Convert predictions into padnas dataframe
        predictions_df = results.pandas().xyxy[0]

        # Obtain names of the detected classes from the image
        detected_classes = list()
        for index, row in predictions_df.iterrows():
            detected_classes.append(row['name'])

        results.save(save_dir=output_path, exist_ok=True)

        return detected_classes

    # Define the path to save processed images
    output_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'results')
    os.makedirs(output_folder, exist_ok=True)

    # Collect file object
    file = request.files['file']

    # Sanitize file name
    filename = secure_filename(file.filename)

    # Store file object
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Yolo object detection
    detected_classes = yolo_object_detection(file_path, output_folder)

    # Serialize the detected classes to JSON to be sent through the query parameters
    serialized_classes = json.dumps(detected_classes)

    # Encode data to be sent through query parameters
    encoded_classes = quote(serialized_classes)

    return redirect(url_for('views.results', detected_classes=encoded_classes))