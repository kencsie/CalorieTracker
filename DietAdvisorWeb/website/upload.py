from flask import Blueprint, request, redirect, flash, current_app, render_template, url_for
from werkzeug.utils import secure_filename
import os
import torch

upload = Blueprint('upload', __name__)

@upload.route('/upload', methods=['POST'])
def upload_file():
    def yolo_object_detection(image_path, output_path):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='./website/data/model/yolo.pt')
        model.eval()
        results = model(image_path)
        results.save(save_dir=output_path, exist_ok=True)


    # Define the path to save processed images
    output_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'results')
    os.makedirs(output_folder, exist_ok=True)

    #Collect file object
    file = request.files['file']
    #Sanitize file name
    filename = secure_filename(file.filename)
    #Store file object
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    #Yolo object detection
    yolo_object_detection(file_path, output_folder)

    return redirect(url_for('views.home'))