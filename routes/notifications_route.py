import os 
import sys
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
import mysql.connector
import json
import random
import asyncio
import controller.NotificationController as notifications

import globals

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

session = app.session

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/list', methods=['GET'])
async def index():
    if 'id' in session:
        if session['role'] == 'Ejecutivo' or session['role'] == 'Staff':
            notifiactions_list = await notifications.get_all_notifications()
            
            return render_template(
                'paginas/notifications/index.jinja', 
                notifications=notifiactions_list, 
                session=session
            )
        
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('auth.login'))
    

@notifications_bp.route('/create', methods=['GET', 'POST'])
async def create():
    if 'id' in session:
        if session['role'] == 'Ejecutivo' or session['role'] == 'Staff':
            return render_template(
                'paginas/notificaciones/create.jinja',
                session=session
            )
        
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('auth.login'))