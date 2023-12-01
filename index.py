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
    host="192.168.1.39",
    user="root",
    password="ikero9090",
    database="MINECRAFTPG",
    auth_plugin="mysql_native_password"
)

cursor = conection.cursor()

##################################################################################
# Funciones del código lógico del procesamiento en el servidor ###################
##################################################################################

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

async def ValidarPersonajeEditado(idUser, name):
    listaPersonajes = await ObtenerListaPersonajes()
    errorCod = 0
    for personaje in listaPersonajes:
        if personaje["name"] == name and personaje["idUser"] != idUser:
            errorCod = 1
    
    return errorCod


async def ObtenerListaPersonajes():
    cursor.execute("""
        SELECT PERSONAJES.id, PERSONAJES.name, PERSONAJES.descripcion, PERSONAJES.color, PERSONAJES.imgUrl, PERSONAJES.passwd, PERSONAJES.idUser,
            CONFIGURACION_PERSONAJE.idPersonaje, CONFIGURACION_PERSONAJE.fontTit, CONFIGURACION_PERSONAJE.imgBackground 
        FROM PERSONAJES INNER JOIN CONFIGURACION_PERSONAJE
            ON PERSONAJES.id = CONFIGURACION_PERSONAJE.idPersonaje;
    """)
    result = cursor.fetchall()
    columnas = [column[0] for column in cursor.description]
    resultados_json = []
    for fila in result:
        fila_json = dict(zip(columnas, fila))
        resultados_json.append(fila_json)
    
    return resultados_json

async def ObtenerPersonaje(idUser):
    cursor.execute("""
        SELECT * FROM PERSONAJES;
    """)
    result = cursor.fetchall()
    columnas = [column[0] for column in cursor.description]
    resultados_json = []
    for fila in result:
        fila_json = dict(zip(columnas, fila))
        resultados_json.append(fila_json)
    
    for personaje in resultados_json:
        if personaje['idUser'] == idUser:
            res = personaje
            break
    return res

async def ValidarDatosLogin(idUser, passwd):
    listaPersonajes = await ObtenerListaPersonajes()
    valido = False
    for personaje in listaPersonajes:
        if personaje["idUser"] == idUser and personaje["passwd"] == passwd:
            valido = True
    
    return valido

async def ValidarUsuario(idUser):
    listaUsuarios = await ListUsers(bot)
    valido = False
    for u in listaUsuarios:
        if idUser == u.id:
            valido = True
    
    return valido

async def ValidarPersonajeUsuario(idUser, name):
    listaPersonajes = await ObtenerListaPersonajes()
    codError = 0
    for personaje in listaPersonajes:
        if personaje["idUser"] == idUser:        
            codError = 1

        elif personaje["name"] == name:
            codError = 2
    return codError


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
#######################################################################################

#######################################################################################
# Funciones y eventos del bot del Discord de pana Gaming ##############################
#######################################################################################
@bot.event
async def on_ready():
    app.run()

#######################################################################################

#######################################################################################
# Paginas de respuesta con procesamiento en el Servidor ###############################
#######################################################################################
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

    userValid = await ValidarUsuario(idUser)

    if userValid == True:
        codError = ValidarPersonajeUsuario(idUser, name)
        if codError == 0:
            cursor.execute(f"""
                INSERT INTO PERSONAJES (name, descripcion, color, imgUrl, passwd, idUser)
                VALUES ('{name}', '{descripcion}', '{color}', '{imgUrl}', '{passwd}', '{idUser}');
            """)
            conection.commit()
            newPersonaje = await ObtenerPersonaje(idUser)
            idPersonaje = newPersonaje['id']
            cursor.execute(f"""
                INSERT INTO CONFIGURACION_PERSONAJE (idPersonaje, fontTit, fontDesc, imgBackground)
                VALUES ({int(idPersonaje)}, 'null', 'null', 'null')
            """)
            conection.commit()
            return render_template("/paginas/minecraft_subpg/personajes/personajeCreated.html", name=name, descripcion=descripcion, imgUrl=imgUrl)
    
        elif codError == 1:
            errorMsg = "Solo puedes tener un solo personaje. Si quieres cambiar de personaje editalo para que sea distinto."
            return render_template("/paginas/minecraft_subpg/personajes/formPersonajes.html", errorMsg = errorMsg)
        
        elif codError == 2:
            errorMsg = "El nombre del personajes que intentas implementar está ya en uso. Porfavor, escoja otro que esté en desuso en el servidor."
            return render_template("/paginas/minecraft_subpg/personajes/formPersonajes.html", errorMsg = errorMsg)

    else:
        errorMsg = "Para poder crear un personaje en nuestro servidor tienes que ser oficialmente miembro de Pana Gaming."
        return render_template("/paginas/minecraft_subpg/personajes/formPersonajes.html", errorMsg = errorMsg)

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
        errorMsg = "Los datos introducidos son incorrectos, comprueba si has introducido los datos correctamente.<br>Pero si usted perdió su contraseña, contactanos y le ayudaremos."
        return render_template("/paginas/minecraft_subpg/personajes/loginEditPersonaje.html", errorMsg = errorMsg)

@app.route("/EditPersonaje", methods=["GET","POST"])
async def EditPersonaje():

    name = request.form["pjName"]
    color = request.form["color"]
    descripcion = request.form["pjDescription"]
    imgUrl = request.form["pjImgUrl"]
    idUser = request.form["idUser"]
    idPersonaje = request.form["idPersonaje"]
    titStyle = request.form["titleStyle"]
    fondo = request.form["aspecto"]

    userValid = await ValidarPersonajeEditado(idUser, name)

    if userValid == 0:
        cursor.execute(f"""
            UPDATE PERSONAJES
            SET name = '{name}', color = '{color}', descripcion = '{descripcion}', imgUrl = '{imgUrl}'
            WHERE idUser = '{idUser}';
        """)
        conection.commit()
        cursor.execute(f"""
            UPDATE CONFIGURACION_PERSONAJE
            SET fontTit = '{titStyle}', imgBackground = '{fondo}'
            WHERE idPersonaje = {idPersonaje};
        """)
        conection.commit()
        personaje = await ObtenerPersonajePorIdUser(idUser)
        return render_template("/paginas/minecraft_subpg/personajes/editPersonaje.html", personaje = personaje)

    else:
        errorMsg = "El nombre introducido esta ya en uso, escoja otro porfavor."
        personaje = await ObtenerPersonajePorIdUser(idUser)
        return render_template("/paginas/minecraft_subpg/personajes/editPersonaje.html", personaje=personaje, errorMsg=errorMsg)
    
###########################################################################################################################################

bot.run("OTY3NDI3OTY2NTQxOTE0MTUy.GF0UK1.HPCb5XwCwadRaToV8kAkcDuMx6_FK5LlkL3LFw")