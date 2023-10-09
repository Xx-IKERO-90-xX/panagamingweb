import os 
import discord
from discord.ext import commands
from discord.utils import *
from flask import *
import mysql.connector
import json
import random


intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)

app = Flask(__name__)

conection = mysql.connector.connect(
    host="192.168.1.66",
    user="root",
    password="ikero9090",
    database="MINECRAFTPG"
)

cursor = conection.cursor()


async def ListUsers(bot):
    guild = bot.get_guild(793956939687133184)
    list = []
    for m in guild.members: 
        list.append(m)

    return list

async def MostrarEjecutivos(userList):
    guild = bot.get_guild(793956939687133184)
    role = guild.get_role(889578160495140898)
    ejec = []

    for user in userList:
        if role in user.roles:
            ejec.append(user)

    return ejec

async def MostrarStaff(userList, ejecList):
    guild = bot.get_guild(793956939687133184)
    role = guild.get_role(856835937816674314)
    staff = []

    for user in userList:
        if role in user.roles:
            encontrado = False
            for r in ejecList:
                if user == r:
                    encontrado = True

            if encontrado == False:
                staff.append(user)
    
    return staff

async def MostrarMiembros(userList, staffList, ejecList):
    guild = bot.get_guild(793956939687133184)
    role = guild.get_role(852500184662409216)
    members = []
    for user in userList:
        if role in user.roles:
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

async def ObtenerListaPersonajes():
    cursor.execute("SELECT * FROM PERSONAJES;")
    result = cursor.fetchall()
    columnas = [column[0] for column in cursor.description]
    resultados_json = []
    for fila in result:
        fila_json = dict(zip(columnas, fila))
        resultados_json.append(fila_json)
    
    return resultados_json

async def ValidarDatosLogin(idUser, passwd):
    listaPersonajes = await ObtenerListaPersonajes()
    valido = False
    for personaje in listaPersonajes:
        if personaje["idUser"] == idUser and personaje["passwd"] == passwd:
            valido = True
    
    return valido


def GenerarContraseña():
    letras = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    numeros = "0123456789"

    unir = f'{letras}{numeros}'
    length = 10
    passwd = random.sample(unir, length)

    passwd_final = "".join(passwd)

    return passwd_final

async def ObtenerPersonajePorIdUser(idUser):
    listaPersonajes = await ObtenerListaPersonajes()
    result = "null"
    for personaje in listaPersonajes:
        if personaje["idUser"] == idUser:
            result = personaje
            break
    
    return result


@bot.event
async def on_ready():
    app.run()

@app.route("/")
def Inicio():
    return render_template("index.html")

@app.route("/minecraft")
def minecraft():
    return render_template("/paginas/minecraft.html")

@app.route("/contacto")
def contacto():
    return render_template("/paginas/contact.html")

@app.route("/comunidad")
async def comunidad():
    userList = await ListUsers(bot)
    ejecList = await MostrarEjecutivos(userList)
    staffList = await MostrarStaff(userList, ejecList)
    memberList = await MostrarMiembros(userList, staffList, ejecList)

    return render_template("/paginas/comunidad.html", ejecList=ejecList, staffList=staffList, memberList=memberList)

@app.route('/historyMC')
async def historyMC():
    return render_template('/paginas/minecraft_subpg/history/portalMc.html')

@app.route("/NuevoPersonaje")
async def NuevoPersonaje():
    return render_template("/paginas/minecraft_subpg/personajes/formPersonajes.html")

@app.route("/CrearPersonaje", methods=["GET","POST"])
async def CrearPersonaje():

    idUser = request.form['idUser']
    passwd = request.form['passwd']
    name = request.form['pjName']
    descripcion = request.form['pjDescription']
    imgUrl = request.form['pjImgUrl']
    color = request.form['color']

    cursor.execute(f"""
        INSERT INTO PERSONAJES (name, descripcion, color, imgUrl, passwd, idUser)
        VALUES ('{name}', '{descripcion}', '{color}', '{imgUrl}', '{passwd}', '{idUser}');
    """)

    conection.commit()
    
    return render_template("/paginas/minecraft_subpg/personajes/personajeCreated.html", name=name, descripcion=descripcion, imgUrl=imgUrl)

@app.route("/PersonajesMinecraftPG")
async def PersonajesMinecraftPG():
    listaPersonajes = []
    listaPersonajes = await ObtenerListaPersonajes()
    return render_template("/paginas/minecraft_subpg/personajes/portalPersonajesMC.html", listaPersonajes = listaPersonajes)

@app.route("/LoginEditPersonaje")
async def LoginEditPersonaje():
    return render_template("/paginas/minecraft_subpg/personajes/loginEditPersonaje.html")

@app.route("/FormEditPersonaje", methods=["GET", "POST"])
async def FormEditPersonaje():
    idUser = request.form["idUser"]
    passwd = request.form["passwd"]

    loginValido = await ValidarDatosLogin(idUser, passwd)

    if loginValido == True:
        personaje = await ObtenerPersonajePorIdUser(idUser)
        return render_template("/paginas/minecraft_subpg/personajes/editPersonaje.html", personaje = personaje)

    else:
        return render_template("/paginas/minecraft_subpg/personajes/portalPersonajesMC.html")

@app.route("/EditPersonaje", methods=["GET", "POST"])
async def EditPersonaje():

    name = request.form["pjName"]
    color = request.form["color"]
    descripcion = request.form["pjDescription"]
    imgUrl = request.form["pjImgUrl"]
    idUser = request.form["idUser"]

    cursor.execute(f"""
        UPDATE PERSONAJES
        SET name = '{name}', color = '{color}', descripcion = '{descripcion}', imgUrl = '{imgUrl}'
        WHERE idUser = '{idUser}';
    """)
    conection.commit()

    personaje = await ObtenerPersonajePorIdUser(idUser)

    return render_template("/paginas/minecraft_subpg/personajes/personajeEdited.html", personaje = personaje)

bot.run("")