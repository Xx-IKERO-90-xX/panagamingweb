import os
import sys
from flask import request, Flask, render_template, current_app, redirect, session, sessions, url_for, Blueprint
from werkzeug.utils import secure_filename

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app
from extensions import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Upload image function
async def upload_image(imagen):
    image_filename = secure_filename(imagen.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
    imagen.save(filepath)

    return image_filename

# Update image function
async def update_image(imagen, last_imagen):
    if last_imagen != None:
        old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], last_imagen)
        os.remove(old_image_path)
    image_filename = secure_filename(imagen.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
    imagen.save(filepath)

    return image_filename
