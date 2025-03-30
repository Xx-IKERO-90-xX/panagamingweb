import os 
import sys
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
import json
import random
import asyncio
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
user_bp = Blueprint('usuario', __name__)
db = app.db


@user_bp.route('/me', methods=['GET'])
async def my_profile():
    if 'id' in session:
        user = User.query.get(session['id'])
        user_style = db.session.query(UserStyle).filter(UserStyle.idUser == session['id']).first()
        
        result = {
            "avatar": session["imgUrl"],
            "name": user.username,
            "mc_name": user.mc_name,
            "descripcion": user.descripcion,
            "main": user_style.main,
            "banner": user_style.banner
        }

        return render_template(
            '/paginas/users/myProfile.jinja', 
            user=result, 
            session=session
        )
    
    else:
        return redirect(url_for("auth.login"))


@user_bp.route('/<int:id>', methods=['GET'])
async def UserProfile(id):
    if 'id' in session:
        user = User.query.get(id)
        user_style = db.session.query(UserStyle).filter(UserStyle.idUser == id).first()
        discord_user = await discord_server.get_discord_user_by_id(id)
        
        result = {
            "avatar": discord_user.avatar.url, 
            "name": user.username, 
            "mc_name": user.mc_name, 
            "descripcion": user.descripcion, 
            "main": user_style.main, 
            "banner": user_style.banner
        }

        return render_template(
            '/paginas/users/profile.jinja', 
            user=result, 
            session=session
        )
    
    else:
        return redirect(url_for('auth.login'))


@user_bp.route('/usuario/me/description/edit', methods=["POST"])
async def edit_user_description():
    if 'id' in session:
        description = request.form['description']
        user = db.session.query(User).filter(User.id == session['id']).first()
        print(user)
        user.descripcion = description
        db.session.commit()
        
        return redirect(url_for('usuario.my_profile', id=session['id']))
    
    else:
        return redirect(url_for('auth.login'))


@user_bp.route('/usuario/edit/style/<int:id>', methods=["GET"])
async def EditUserStyle(id):
    if 'id' in session:
        user = User.query.get(id)
        style_user = db.session.query(UserStyle).filter(UserStyle.idUser == id).first()
        
        result = {
            "avatar": session["imgUrl"], 
            "name": user.username, 
            "mc_name": user.mc_name, 
            "descripcion": user.descripcion, 
            "main": style_user.main, 
            "banner": style_user.banner 
        }

        return render_template(
            '/paginas/users/styleProfile.jinja', 
            user=result, 
            session=session
        )
        
    else:
        return redirect(url_for("auth.login"))


@user_bp.route('/usuario/edit/style/newMainBk/<int:id>', methods=["POST"])
async def set_main_style(id):
    if 'id' in session:
        main_bk = request.form["mainBk"]

        user_style = db.session.query(UserStyle).filter(UserStyle.idUser == id).first()
        user_style.main = main_bk
        db.session.commit()

        return redirect(url_for('usuario.EditUserStyle', id=id))
    else:
        return redirect(url_for('auth.login'))
