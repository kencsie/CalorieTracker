from flask import Flask
import os

UPLOAD_FOLDER = './website/data/pics'

def create_app():
    # Create upload folder recursively
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from .views import views
    from .auth import auth
    from .upload import upload

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(upload, url_prefix='/')

    return app