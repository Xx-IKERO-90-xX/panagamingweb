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
from controller.database import *
import controller.UsuarioController as users
import controller.DiscordServerController as discord_server
import controller.SecurityController as security
import controller.McServersController as mcservers
from controller.ProfileController import *
from threading import Thread
from mcrcon import MCRcon
import bot
from routes import auth_bp, minecraft_bp, user_bp, notifications_bp

import globals

datos = {}
with open('settings.json') as archivo:
    datos = json.load(archivo)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    globals.guild = bot.get_guild(datos["discord"]["server"]["id"])
    if globals.guild is not None:
        print(f"El bot se ha conectado con el servidor: {globals.guild.name}")
    else:
        print("El bot no pudo conectarse con el servidor")

    socketio.run(
        app,
        port = datos["flask"]["port"], 
        host = datos["flask"]["host"],
        debug = True
    )
    
def run_discord_bot():
    bot.run(app.datos["discord"]["token"])

def start_discord_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(run_discord_bot())

app = Flask(__name__)
app.secret_key = "tr4rt34t334yt"
socketio = SocketIO(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(minecraft_bp, url_prefix="/minecraft") 
app.register_blueprint(user_bp, url_prefix="/usuarios")
app.register_blueprint(notifications_bp, url_prefix='/notifications')




#######################################################################################


async def get_discord_users():
    list = []
    for m in globals.guild.members: 
        list.append(m)
    return list

async def get_discord_ejecutives(userList):
    ejecRole = globals.guild.get_role(datos["discord"]["roles"]["ejecutive"])
    ejec = []
    
    for user in userList:
        if ejecRole in user.roles:
            ejec.append(user)
    return ejec

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

'''
------------------------------------------------------------
Rutas iniciales de la aplicacion
------------------------------------------------------------
'''

@app.route("/")
async def index():
    if "id" in session:
        return render_template("/paginas/index2.jinja", session = session)
    else:
        return render_template("index.jinja")

@app.route("/community")
async def community():
    userList = await get_discord_users()
    ejecList = await get_discord_ejecutives(userList)
    staffList = await get_discord_staff_users(userList, ejecList)
    memberList = await get_discord_members(userList, staffList, ejecList)
    
    if "id" in session:         
        return render_template("/paginas/comunidad.jinja", ejecList=ejecList, staffList=staffList, memberList=memberList, session=session)    
    else:
        return render_template("comunidad1.jinja", ejecList=ejecList, staffList=staffList, memberList=memberList)




"""
    SOCKETS
"""

# Maneja los mensajes enviados desde el chat publico de la pagina del servidor de Minecraft
@socketio.on('send_message')
def handle_public_chat_message(data):
    app.logger.info(f"Message: {data['message']} from {data['username']}")
    data['id'] = f"/usuario/{data['id']}"
    emit('receive_message', data, broadcast=True)


#Terminal de los servidores de minecraft
@socketio.on('send_vanilla_command')
def handle_send_command(cmd):
    
    result_queue = multiprocessing.Queue()
    
    print(cmd['command'])

    process = multiprocessing.Process(
        target=mcservers.execute_vanilla_command, 
        args=(cmd['command'], result_queue)
    )
    
    process.start()
    process.join()

    response = result_queue.get()

    print(response)
    emit('server_output', {'output': response})



################################################################################################

if __name__ == '__main__':
    bot_thread = Thread(target=bot.run(datos['discord']['token']))
    bot_thread.start()
    