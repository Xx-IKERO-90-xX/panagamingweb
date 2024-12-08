import os 
import sys
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
import controller.DiscordServerController as discord_server
import controller.SecurityController as security
from threading import Thread
from entity.User import *
from entity.UserStyle import *

import globals
sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app
from extensions import db

session = app.session
auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/logout")
async def logout():
    session.clear()
    return redirect(url_for("index.index"))


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

            session["id"] = str(user.id)
            session["name"] = username
            session["imgUrl"] = user.avatar.url
            session['role'] = await security.deduce_role(user.id)
    
            return redirect(url_for('index.index'))

        else:
            errorMsg = "Hay datos erroneos en el formulario, revisalos bien."
            return render_template("login.jinja", errorMsg=errorMsg)

@auth_bp.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == "GET":
        return render_template("registrar.jinja")
    else:
        idUser = int(request.form['idUser'])
        username = request.form['username']
        passwd = request.form['passwd']
        descripcion = request.form['descripcion']
        
        passwd_encripted = await security.encrypt_passwd(passwd)
        discord_user = await discord_server.get_discord_user_by_id(idUser)

        new_user = User(idUser, username, passwd_encripted, descripcion, None)
        new_style_user = UserStyle(idUser, None, None)

        db.session.add(new_user)
        db.session.add(new_style_user)
        
        db.session.commit()

        session["id"] = idUser
        session["name"] = username
        session["imgUrl"] = discord_user.avatar.url
        session['role'] = await security.deduce_role(idUser)
                
        return redirect(url_for("index.index"))