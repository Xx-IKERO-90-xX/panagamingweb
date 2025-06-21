import os 
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
import json
import random
import sys
import asyncio
import controller.SecurityController as security
import controller.McServersController as mcservers
from threading import Thread
import multiprocessing


sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)
import app
from extensions import db

session = app.session
minecraft_bp = Blueprint('minecraft', __name__)

# Ruta inicial de minecraft
@minecraft_bp.route('/index', methods=['GET'])
async def index():
    if 'id' in session:
        return render_template(
            '/paginas/minecraft.jinja', 
            session=session
        )
    else:
        return redirect(url_for('auth.login'))

#Ruta que te lleva a la pagina del servidor de minecraft
@minecraft_bp.route('/server', methods=['GET'])
async def minecraftServer():
    if 'id' in session:
        dynmap_host = app.datos['minecraft']['archlight']['ip']
        dynmap_port = app.datos['minecraft']['archlight']['dynmap']['port']

        return render_template(
            '/paginas/minecraft_subpg/server/minecraftServer.jinja', 
            dynmap_host=dynmap_host, 
            dynmap_port=dynmap_port,
            session=session
        )
    
    else:
        return redirect(url_for('auth.login'))

# Ruta que te permite llevar al panel del administrador del servidor de minecraft
@minecraft_bp.route("/admin/mcconsole", methods=['GET'])
async def mc_console():
    if 'id' in session:
        if session['role'] == 'Staff' or session['role'] == 'Ejecutivo':
            return render_template(
                'paginas/minecraft_subpg/admin/console.jinja',
                session=session
            )
        else:
            return redirect(url_for('minecraft.index'))
    else:
        return redirect(url_for('auth.login'))