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

user_bp = Blueprint('usuario', __name__)

@user_bp.route('/me/<int:id>', methods=['GET'])
async def MiPerfil(id):
    if 'id' in session:
        appUser = await users.get_user_by_id(id)
        discord_user = await discord_server.get_discord_user_by_id(session["id"])
        print(discord_user)
        result = {"avatar": discord_user.avatar.url, "name":discord_user.name, "mote":discord_user.nick, "descripcion":appUser["descripcion"], "main":appUser["main"], "banner":appUser["banner"]}
        
        return render_template('/paginas/users/myProfile.jinja', user=result, session=session)
    else:
        return redirect(url_for("auth.login"))

@user_bp.route('/<int:id>', methods=['GET'])
async def UserProfile(id):
    if 'id' in session:
        print("Usuario ID: ", id)
        if id != session['id']:
            appUser = await users.get_user_by_id(id)
            dUser = await users.GetDiscordUser(id)
            result = {"avatar": dUser.avatar.url, "name":dUser.name, "mote":dUser.nick, "descripcion":appUser["descripcion"], "main":appUser["main"], "banner":appUser["banner"]}
            return render_template('/paginas/users/profile.jinja', user=result, session=session)
        else:
            return redirect(url_for('usuario.MiPerfil', id=session['id']))
    else:
        return redirect(url_for('auth.login'))

@user_bp.route('/edit/descripcion/<int:id>', methods=["GET","POST"])
async def EditMyDescription(id):
    if 'id' in session:
        descripcion = request.form["descripcion"]
        
        await EditMyDescriptionPost(id, descripcion)
        return redirect(url_for('usuario.MiPerfil', id=id))
    else:
        return redirect(url_for("auth.login"))

@user_bp.route('/edit/style/<int:id>', methods=["GET"])
async def EditUserStyle(id):
    if 'id' in session:
        appUser = await users.get_user_by_id(id)
        dUser = await users.GetDiscordUser(id)
        result = {"avatar": dUser.avatar.url, "name":dUser.name, "mote":dUser.nick, "descripcion":appUser["descripcion"], "main":appUser["main"], "banner":appUser["banner"] }
        return render_template('/paginas/users/styleProfile.jinja', user=result, session=session)
    else:
        return redirect(url_for("auth.login"))

@user_bp.route('/usuario/edit/style/newMainBk/<int:id>', methods=["POST"])
async def SetUserBackground(id):
    if 'id' in session:
        mainBk = request.form["mainBk"]
        await SetMainUserTheme(id, mainBk)
        return redirect(url_for('usuario.EditUserStyle', id=id))
    else:
        return redirect(url_for('auth.login'))
