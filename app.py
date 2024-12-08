import os 
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
import mysql.connector
import json
import random
import asyncio
import multiprocessing
import controller.DiscordServerController as discord_server
import controller.SecurityController as security
import controller.McServersController as mcservers
from threading import Thread
from mcrcon import MCRcon
from extensions import db, socketio
import globals

datos = {}
with open('settings.json') as archivo:
    datos = json.load(archivo)

app = None

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = discord.Client(intents=intents)

# Obtiene el listado de todos los usuarios de Discord.
async def get_discord_users():
    list = []

    for m in globals.guild.members: 
        list.append(m)

    return list


# Saca los Ejecutivos de Pana Gaming registrados en el servidor de Discord.
async def get_discord_ejecutives(userList):
    ejecRole = globals.guild.get_role(datos["discord"]["roles"]["ejecutive"])
    ejec = []
    
    for user in userList:
        if ejecRole in user.roles:
            ejec.append(user)

    return ejec


# Saca todos los miembros del Staff de Pana Gaming registrados en el servidor de Discord.
async def get_discord_staff_users(userList, ejecList):
    staffRole = globals.guild.get_role(datos["discord"]["roles"]["staff"])
    staff = []
    
    for user in userList:
        if staffRole in user.roles:
            encontrado = False
            for r in ejecList:
                if user == r:
                    encontrado = True
                    break

            if encontrado == False:
                staff.append(user)

    return staff


# Saca los Miembros de la comunidad de pana gaming registrados en el servidor de Discord.
async def get_discord_members(userList, staffList, ejecList):
    memberRole = globals.guild.get_role(datos["discord"]["roles"]["member"])
    members = []
    
    for user in userList:
        if memberRole in user.roles:
            encontrado = False
            for r in staffList:
                if user == r:
                    encontrado = True       
            for r in ejecList:
                if user == r:
                    encontrado = True           
            if encontrado == False:
                members.append(user)  

    return members


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    globals.guild = bot.get_guild(datos["discord"]["server"]["id"])
    run_flask()


def run_bot():
    bot.run(datos['discord']['token'])
    run_flask()


def create_app():
    app = Flask(__name__)
    app.secret_key = "a40ecfce592fd63c8fa2cda27d19e1dbc531e946"
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{datos['database']['user']}:{datos['database']['passwd']}@{datos['database']['host']}/{datos['database']['db']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    socketio.init_app(app)

    from routes import auth_bp, minecraft_bp, user_bp, index_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(minecraft_bp, url_prefix="/minecraft")
    app.register_blueprint(user_bp, url_prefix="/usuarios")
    app.register_blueprint(index_bp)

    with app.app_context():
        import sockets

    return app


def run_flask():
    app = create_app()
    with app.app_context():
        db.create_all()
    
    socketio.run(
        app, 
        port=5000, 
        host='0.0.0.0', 
        debug=True,
    )
 


if __name__ == "__main__":
    run_bot()





