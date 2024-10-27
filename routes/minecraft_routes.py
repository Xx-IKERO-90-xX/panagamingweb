import os 
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
from controller.database import *
import controller.UsuarioController as users
import controller.DiscordServerController as discord_server
import controller.SecurityController as security
import controller.McServersController as mcservers
from controller.ProfileController import *
from threading import Thread
import multiprocessing
import bot

import globals

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

session = app.session

minecraft_bp = Blueprint('minecraft', __name__)

@minecraft_bp.route('/', methods=['GET'])
async def index():
    if 'id' in session:
        return render_template(
            '/paginas/minecraft.jinja', 
            session=session
        )
    else:
        return redirect(url_for('auth.login'))
    
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

@minecraft_bp.route("/admin", methods=['GET'])
async def admin_pannel():
    if 'id' in session:
        if session['role'] == 'Staff' or session['role'] == 'Ejecutivo':
            return render_template(
                'paginas/minecraft_subpg/admin/pannel.jinja',
                session=session
            )
        
        else:
            return redirect(url_for('minecraft.index'))
    else:
        return redirect(url_for('auth.login'))