from flask import Flask
from flask_session import Session
import os

UPLOAD_FOLDER = './website/data/pics'

def create_app():
    # Create upload folder recursively
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Configuration for MongoDB
    app.config["MONGO_URI"] = "mongodb://192.168.50.50:40019/DietAdvisorWeb"

    # Configure session to use filesystem (instead of signed cookies)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './website/data/sessions'
    Session(app)

    from .views import views
    from .auth import auth
    from .upload import upload

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(upload, url_prefix='/')

    return app