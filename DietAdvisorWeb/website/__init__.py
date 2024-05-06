from flask import Flask
from flask_session import Session
import os

UPLOAD_FOLDER = './website/data/pics'

def create_app():
    # Create upload folder recursively
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # app = Flask(__name__, static_folder=UPLOAD_FOLDER, static_url_path='/static')
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # app = Flask(__name__, static_folder=UPLOAD_FOLDER, static_url_path='/static')

    # Configuration for MongoDB
    app.config["MONGO_URI"] = "mongodb+srv://calorie:calorie@cluster0.mv5fa3v.mongodb.net/DietAdvisorWeb"

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