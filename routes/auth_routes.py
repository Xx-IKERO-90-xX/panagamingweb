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

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/logout")
async def logout():
    session.clear()
    return redirect(url_for("index"))


@auth_bp.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == "GET":
        return render_template("login.jinja")
    else:
        username = request.form["username"]
        passwd = request.form["passwd"]
        
        valid = await security.validate_login(username, passwd)
    
        if valid:
            user = await discord_server.get_discord_user_by_username(username)
            print(user)
            session["id"] = str(user.id)
            session["name"] = username
            session["imgUrl"] = user.avatar.url
            session['role'] = await security.deduce_role(user.id)
    
            return render_template("/paginas/index2.jinja", session=session)

        else:
            errorMsg = "Hay datos erroneos en el formulario, revisalos bien."
            return render_template("login.jinja", errorMsg=errorMsg)

@auth_bp.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == "GET":
        return render_template("registrar.jinja")
    else:
        idUser = request.form['idUser']
        username = request.form['username']
        passwd = request.form['passwd']
        descripcion = request.form['descripcion']
        
        if not await users.ComprobarUsuarioRepetido(idUser):
            passwd_encripted = await security.encrypt_passwd(passwd)
            await users.new_user(idUser, username, passwd_encripted, descripcion)
                
            return redirect(url_for("index"))
        
        else:
            errorMsg = f"El usuario {username} ya existe."
            return render_template("registrar.jinja", errorMsg=errorMsg)