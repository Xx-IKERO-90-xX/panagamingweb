import os 
import sys
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
import controller.SecurityController as security
from threading import Thread
from entity.User import *

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app
from extensions import db

session = app.session
index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
async def index():
    if 'id' in session:
        return render_template(
            '/paginas/index.jinja', 
            session=session
        )
    else:
        return render_template('index.jinja')