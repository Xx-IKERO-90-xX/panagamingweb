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
import controller.PersonajesController as characters
from controller.database import *
import controller.UsuarioController as users
import controller.DiscordServerController as discord_server
import controller.SecurityController as security
import controller.SectoresPerdidosController as lost_sectors
import controller.MisionesController as missions
import controller.DiarioController as diary
from controller.ProfileController import *
from threading import Thread
import bot

import globals

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

session = app.session

auth_bp = Blueprint('auth', __name__)
