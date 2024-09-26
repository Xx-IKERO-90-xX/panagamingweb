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
from routes import auth_bp, minecraft_bp, user_bp

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

@app.route("/logout")
async def logout():
    session.clear()
    return redirect(url_for("Inicio"))

'''
    
'''
@app.route('/login', methods=['GET', 'POST'])
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
            errorMsg = "No existe el usuario introducido."
            return render_template("login.jinja", errorMsg = errorMsg)

@app.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == "GET":
        return render_template("registrar.jinja")
    else:
        idUser = request.form['idUser']
        username = request.form['username']
        passwd = request.form['passwd']
        descripcion = request.form['descripcion']

        user_repeate = await users.ComprobarUsuarioRepetido(idUser)
        
        if not user_repeate:
            user = await users.get_discord_user_by_username(int(idUser))
            passwd_encripted = await security.encrypt_passwd(passwd)
            await users.new_user(idUser, username, passwd_encripted, descripcion)
            
            session["id"] = idUser
            session["name"] = username
            session["imgUrl"] = user.avatar.url
                
            return redirect(url_for("index"))
        else:
            return render_template("registrar.jinja")
            

"""
-------------------------------------------------------------------------------------------------
"""

    
@app.route("/minecraft")
async def minecraft():
    if "id" in session:
        return render_template("/paginas/minecraft.jinja", session=session)
    else:
        return redirect(url_for('login'))

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

@app.route('/tiket', methods=['GET', 'POST'])
async def tiket():
    if "id" in session:
        if request.method == 'GET':
            return render_template('/paginas/tikets.jinja', session=session)
        else:
            userName = request.form["userName"]
            texto = request.form["texto"]
            channel = bot.get_channel(int(1180858213982273617))
            usuario = await discord_server.GetDiscordUserByName(userName)
    
            if usuario != 'null':
                embed = discord.Embed(
                    title=f"**TIKET DE {usuario.name}**",
                    description=f"{texto}",
                    color=discord.Color.random()
                )
                bot.loop.create_task(channel.send(embed=embed))
                return render_template("/paginas/tiketSended.jinja", usuario=usuario, texto=texto, session=session)  
    
            else:
                errorMsg = f"No se ha encontrado ningún usuario con el nombre {userName} en el servidor de Discord."
                return render_template("/paginas/tikets.jinja", errorMsg=errorMsg, session=session)
    else:
        return redirect(url_for("login"))


"""
    SOCKETS
"""

@socketio.on('send_message')
def hanbleData(data):
    app.logger.info(f"Message: {data['message']} from {data['username']}")
    data['id'] = f"/usuario/{data['id']}"
    emit('recieve_message', data, broadcast=True)


################################################################################################

if __name__ == '__main__':
    bot_thread = Thread(target=bot.run(datos['discord']['token']))
    bot_thread.start()
    