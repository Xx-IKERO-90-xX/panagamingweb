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
from controller.PersonajesController import *
from controller.database import *
from controller.UsuarioController import *
import controller.DiscordServerController as DiscordServer
import controller.LoginController as Login
import controller.SectoresPerdidosController as SectoresPerdidos
from controller.DiarioController import *
from controller.ProfileController import *
from threading import Thread
import bot

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
        debug=True
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

#######################################################################################

async def ListUsers():
    list = []
    for m in globals.guild.members: 
        list.append(m)
    return list

async def ShowEjecutives(userList):
    ejecRole = globals.guild.get_role(datos["discord"]["roles"]["ejecutive"])
    ejec = []
    
    for user in userList:
        if ejecRole in user.roles:
            ejec.append(user)
    return ejec

async def ShowStaffMembers(userList, ejecList):
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

async def ShowMembers(userList, staffList, ejecList):
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

#######################################################################################
############## RUTAS SIN SESIÓN #######################################################
#######################################################################################

@app.route("/")
async def Inicio():
    if "id" in session:
        return render_template("/paginas/index2.jinja", session = session)
    else:
        return render_template("index.jinja")

@app.route("/cerrarSesion")
async def cerrarSesion():
    session.clear()
    return redirect(url_for("Inicio"))

@app.route('/comunidad')
async def comunidad1():
    userList = await ListUsers()
    ejecList = await ShowEjecutives(userList)
    staffList = await ShowStaffMembers(userList, ejecList)
    memberList = await ShowMembers(userList, staffList, ejecList)
    
    if "id" in session:
        return render_template("/paginas/comunidad.jinja", ejecList=ejecList, staffList=staffList, memberList=memberList, session=session)
    else:
        return render_template("comunidad1.jinja", ejecList=ejecList, staffList=staffList, memberList=memberList)


@app.route('/formLogin')
def formLogin():
    return render_template("login.jinja")

@app.route('/formRegister')
def formRegister():
    return render_template("registrar.jinja")

#######################################################################################
######################## PROCESAMIENTO DE SESION ######################################
#######################################################################################


@app.route('/CrearCuenta', methods=['GET', 'POST'])
async def CrearCuenta():
    idUser = request.form['idUser']
    passwd = request.form['passwd']
    passwd2 = request.form['passwd2']
    descripcion = request.form['descripcion']

    usuarioRepetido = await ComprobarUsuarioRepetido(idUser)
    if usuarioRepetido == False:
        if passwd == passwd2:
            user = await GetDiscordUser(idUser)
            await nuevoUsuario(idUser, passwd, descripcion)
            session["id"] = idUser
            session["name"] = user.name
            session["imgUrl"] = user.avatar.url
            return render_template("/paginas/index2.jinja", session=session)
    else:
        return redirect(url_for("formRegister"))
    

@app.route('/IniciarSesion', methods=['GET', 'POST'])
async def IniciarSesion():
    name = request.form["dName"]
    passwd = request.form["passwd"]
    valido = await Login.ValidarInicioSesion(passwd)
    
    if valido == True:
        if await ComprobarNombreDiscord(name) == True:
            user = await GetDiscordUserByName(name)
            session["id"] = str(user.id)
            session["name"] = user.name
            session["imgUrl"] = user.avatar.url
            session['role'] = await Login.DeducirRol(user.id)
            return render_template("/paginas/index2.jinja", session=session)
        else:
            errorMsg = "El nombre introducido no coincide con ningun usuario."
            return render_template("login.jinja", errorMsg=errorMsg)
    else:
        errorMsg = "No existe el usuario introducido."
        return render_template("login.jinja", errorMsg = errorMsg)
    
    
########################################################
######### PÁGINAS CON SESIÓN ###########################
########################################################

@app.route('/principal')
async def principal():
    if "id" in session:
        return render_template("/paginas/index2.jinja", session=session)
    else:
        return redirect(url_for('formLogin'))
    
@app.route("/minecraft")
def minecraft():
    if "id" in session:
        return render_template("/paginas/minecraft.jinja", session=session)
    else:
        return redirect(url_for('formLogin'))

@app.route("/comunidad")
async def comunidad():
    if "id" in session:    
        userList = await ListUsers()
        ejecList = await ShowEjecutives(userList)
        staffList = await ShowStaffMembers(userList, ejecList)
        memberList = await ShowMembers(userList, staffList, ejecList)
        return render_template("/paginas/comunidad.jinja", ejecList=ejecList, staffList=staffList, memberList=memberList, session=session)    
    else:
        return redirect(url_for('formLogin'))

@app.route('/soporte')
async def soporte():
    if "id" in session:
        return render_template('/paginas/tikets.jinja', session=session)
    else:
        return redirect(url_for("formLogin"))

@app.route('/enviarTiket', methods=["GET", "POST"])
async def enviarTiket():
    userName = request.form["userName"]
    texto = request.form["texto"]
    channel = bot.get_channel(int(1180858213982273617))
    usuario = await GetDiscordUserByName(userName)
    
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


#####################################################################################
############ PORTAL PRINCIPAL DE MINECRAFT ##########################################
#####################################################################################

@app.route('/mineacraft/server')
async def portalServer():
    if "id" in session:
        return render_template('/paginas/minecraft_subpg/history/portalMc.jinja', session=session)
    else:
        return redirect(url_for('formLogin'))

@app.route("/mineacraft/personajes/NuevoPersonaje")
async def NuevoPersonaje():
    if "id" in session:
        return render_template("/paginas/minecraft_subpg/personajes/formPersonajes.jinja", session=session)
    else:
        return redirect(url_for('formLogin'))

@app.route("/mineacraft/personajes/CrearPersonaje", methods=["POST"])
async def CrearPersonaje():
    name = request.form['pjName']
    descripcion = request.form['pjDescription']
    imgUrl = request.form['pjImgUrl']
    color = request.form['color']
    raza = request.form['raza']
    edad = request.form['edad']
    sexo = request.form['sexo']

    if 'id' in session:
        codError = await ValidarPersonajeUsuario(session['id'], name)
        if codError == 0:
            if imgUrl or imgUrl == "":
                imgUrl = "/static/img/userlog.jpg"
            await NuevoPersonajePost(name, descripcion, color, imgUrl, session['id'], raza, edad, sexo)
            return redirect(url_for('PersonajesMinecraftPG'))
        
        elif codError == 1:
            errorMsg = "Solo puedes tener un solo personaje. Si quieres cambiar de personaje editalo para que sea distinto."
            return render_template("/paginas/minecraft_subpg/personajes/formPersonajes.jinja", errorMsg = errorMsg, session=session)   
        
        elif codError == 2:
            errorMsg = "El nombre del personajes que intentas implementar está ya en uso. Porfavor, escoja otro que esté en desuso en el servidor."
            return render_template("/paginas/minecraft_subpg/personajes/formPersonajes.jinja", errorMsg = errorMsg, session=session)
    else:
        return redirect(url_for('formLogin'))

@app.route("/minecraft/personajes")
async def PersonajesMinecraftPG():
    if "id" in session:
        listaPersonajes = []
        paginas = []  
        listaPersonajes = await GetCharacterList()
        paginas = await ObtenerPaginas()
        tienePersonaje = await comprobarSiTienePersonaje(session["id"])
        if tienePersonaje == True:
            return render_template("/paginas/minecraft_subpg/personajes/portalPersonajesMC2.jinja", listaPersonajes = listaPersonajes, session=session, paginas=paginas)
        else:
            return render_template("/paginas/minecraft_subpg/personajes/portalPersonajesMC.jinja", listaPersonajes = listaPersonajes, session=session, paginas=paginas)
    else:
        return redirect(url_for("formLogin"))

@app.route("/minecraft/personajes/FormEditPersonaje")
async def FormEditPersonaje():
    if "id" in session:
        personaje = await ObtenerPersonajePorIdUser(str(session['id']))
        print(personaje)
        return render_template("/paginas/minecraft_subpg/personajes/editPersonaje.jinja", personaje=personaje[0], session=session)
    else:
        return redirect(url_for("Inicio"))


@app.route("/minecraft/miPersonaje/<int:idUser>", methods=["GET"])
async def miPersonaje(idUser):
    if 'id' in session:
        personaje = await personajes.ObtenerPersonajePorIdUser(session['id'])
        print(personaje)
        return render_template('/paginas/minecraft_subpg/personajes/miPersonaje.jinja', personaje=personaje[0], session=session)
    else:
        return redirect(url_for("formLogin"))

@app.route("/minecraft/personajes/detalles/<int:idPersonaje>", methods=["GET"])
async def VerInfoPersonaje(idPersonaje):
    if 'id' in session:
        paginas = []
        personaje = await GetCharacterById(idPersonaje)
        paginas = await ShowDiarioPages(idPersonaje)
        print(personaje)
        return render_template("/paginas/minecraft_subpg/personajes/personaje.jinja", personaje=personaje, paginas=paginas, session=session) 
    else:
        return redirect(url_for('formLogin'))

@app.route("/mineacraft/personajes/EditPersonaje", methods=["GET", "POST"])
async def EditPersonaje():
    name = request.form["pjName"]
    color = request.form["color"]
    descripcion = request.form["pjDescription"]
    imgUrl = request.form["pjImgUrl"]
    idUser = request.form["idUser"]

    raza = request.form['raza']
    edad = request.form['edad']
    sexo = request.form['sexo']

    userValid = await ValidarPersonajeEditado(idUser, name)
    
    if userValid == 0:
        await EditarPersonajePost(name, color, descripcion, imgUrl, idUser, raza, edad, sexo)
        return redirect(url_for("FormEditPersonaje"))
    else:
        errorMsg = "El nombre introducido esta ya en uso, escoja otro porfavor."
        personaje = await ObtenerPersonajePorIdUser(idUser)
        return render_template("/paginas/minecraft_subpg/personajes/editPersonaje.jinja", personaje=personaje, errorMsg=errorMsg, session=session)


@app.route('/mineacraft/personajes/diario/nuevaPagina')
async def nuevaPagina():
    if "id" in session:
        return render_template("/paginas/minecraft_subpg/personajes/diarios/nuevaPagina.jinja", session=session)
    else:
        return redirect(url_for("formLogin"))

@app.route('/minecraft/personajes/diario/crearPagina', methods=["GET", "POST"])
async def crearPagina():
    if "id" in session:
        personaje = await ObtenerPersonajePorIdUser(session["id"])
        contenido = request.form["content"]
        conexion = await AbrirConexionSQL()
        cursor = conexion.cursor()
        cursor.execute(f"""
            INSERT INTO DIARIO (idPersonaje, contenido)
            VALUES ({personaje["id"]}, '{contenido}');
        """)
        conexion.commit()
        conexion.close()
        return redirect(url_for("PersonajesMinecraftPG"))  
    else:
        return redirect(url_for("formLogin"))


@app.route('/EditarPagina', methods=['POST'])
async def EditarPagina():
    if "id" in session:
        idPagina = request.form["idPagina"]
        contenido = request.form["contenido"]
        await UpdateDiarioPageAction(idPagina, contenido)
        return redirect(url_for("MiDiario"))
    else:
        return redirect(url_for("formLogin"))

@app.route('/minecraft/personajes/me/diario', methods=['GET'])
async def MiDiario():
    if "id" in session:
        personaje = await ObtenerPersonajePorIdUser(session['id'])
        print(personaje)
        paginas = await ShowDiarioPages(int(personaje[0]['id']))
        return render_template("/paginas/minecraft_subpg/personajes/miDiario.jinja", paginas=paginas, personaje=personaje[0], session=session)
    else:
        return redirect(url_for("formLogin"))

@app.route('/minecraft/personajes/me/diario/newPage/<int:idPersonaje>', methods=['GET', 'POST'])
async def NewPage(idPersonaje):
    if 'id' in session:
        await NewPageAction(idPersonaje)
        return redirect(url_for("MiDiario"))
    else:
        return redirect(url_for("formLogin"))

@app.route('/minecraft/personajes/me/diario/deletePage/<int:idPagina>', methods=["GET"])
async def DeletePage(idPagina):
    if 'id' in session:
        await DeletePageAction(idPagina)
        return redirect(url_for("MiDiario"))
    else:
        return redirect(url_for("formLogin"))



#-----------------------------------------------------------------------#
#-------------------- USUARIOS -----------------------------------------#
#-----------------------------------------------------------------------#


@app.route('/usuario/me/<int:id>', methods=['GET'])
async def MiPerfil(id):
    if 'id' in session:
        appUser = await ObtenerUsuario(id)
        dUser = await GetDiscordUser(id)
        result = {"avatar": dUser.avatar.url, "name":dUser.name, "mote":dUser.nick, "descripcion":appUser["descripcion"], "main":appUser["main"], "banner":appUser["banner"]}
        return render_template('/paginas/users/myProfile.jinja', user=result, session=session)
    else:
        return redirect(url_for("formLogin"))

@app.route('/usuario/<int:id>', methods=['GET'])
async def UserProfile(id):
    if 'id' in session:
        appUser = await ObtenerUsuario(id)
        dUser = await GetDiscordUser(id)
        result = {"avatar": dUser.avatar.url, "name":dUser.name, "mote":dUser.nick, "descripcion":appUser["descripcion"], "main":appUser["main"], "banner":appUser["banner"]}
        return render_template('/paginas/users/profile.jinja', user=result, session=session)
    else:
        return redirect(url_for('formLogin'))

@app.route('/usuario/edit/descripcion/<int:id>', methods=["GET","POST"])
async def EditMyDescription(id):
    if 'id' in session:
        descripcion = request.form["descripcion"]
        await EditMyDescriptionPost(id, descripcion)
        return redirect(url_for('MiPerfil', id=id))
    else:
        return redirect(url_for("formLogin"))


@app.route('/usuario/edit/style/<int:id>', methods=["GET"])
async def EditUserStyle(id):
    if 'id' in session:
        appUser = await ObtenerUsuario(id)
        dUser = await GetDiscordUser(id)
        result = {"avatar": dUser.avatar.url, "name":dUser.name, "mote":dUser.nick, "descripcion":appUser["descripcion"], "main":appUser["main"], "banner":appUser["banner"] }
        return render_template('/paginas/users/styleProfile.jinja', user=result, session=session)
    else:
        return redirect(url_for("formLogin"))

@app.route('/usuario/edit/style/newMainBk/<int:id>', methods=["POST"])
async def SetUserBackground(id):
    mainBk = request.form["mainBk"]
    await SetMainUserTheme(id, mainBk)
    return redirect(url_for('EditUserStyle', id=id))

############################################################################################
############# SERVIDOR DE MINECRAFT ########################################################
############################################################################################

@app.route('/minecraft/server', methods=['GET'])
async def minecraftServer():
    if 'id' in session:
        return render_template('/paginas/minecraft_subpg/server/minecraftServer.jinja', session=session)
    else:
        return redirect(url_for('formLogin'))

@socketio.on('send_message')
def handleMessage(data):
    app.logger.info(f"Message: {data['message']} from {data['username']}")
    data['id'] = f"/usuario/{data['id']}"
    emit('receive_message', data, broadcast=True)

###########################################################################################################################################



###############################################################################################
################### PANEL ADMINISTRADOR #######################################################
###############################################################################################


########### [SECTORES PERDIDOS ]###########################

@app.route('/minecraft/SectoresPerdidos', methods=["GET"])
async def GestionarSectoresPerdidos():
    if 'id' in session:
        if session['role'] == 'Ejecutivo' or session['role'] == 'Staff':
           sectoresPerdidosList = await SectoresPerdidos.MostrarSectoresPerdidosAction()
           return render_template('/paginas/minecraft_subpg/server/sectoresPerdidos/sectorsIndex.jinja', sectoresPerdidos=sectoresPerdidosList, session=session)
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('formLogin'))

@app.route('/minecraft/SectoresPerdidos/create', methods=['GET'])
async def NewSectorPerdido():
    if 'id' in session:
        if session['role'] == 'Ejecutivo' or session['role'] == 'Staff':
            return render_template('/paginas/minecraft_subpg/server/sectoresPerdidos/create.jinja', session=session)
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('formLogin'))

@app.route('/minecraft/SectoresPerdidos/new', methods=['POST'])
async def CrearSectorPerdido():
    if 'id' in session:
        if session['role'] == 'Ejecutivo' or session['role'] == 'Staff':
            descripcion = request.form['descripcion']
            imagen_name = None
            
            if 'imagen' not in request.files or request.files['imagen'].filename == '':
                imagen_name = None
            else:
                imagen = request.files['imagen']
                imagen_name = secure_filename(imagen.filename)
                imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_name))
                
            activo = request.form['activo']
            planeta = request.form['planeta']
            cord_x = request.form['cord_x']
            cord_y = request.form['cord_y']
            cord_z = request.form['cord_z']
            
            await SectoresPerdidos.CrearSectorPerdidoAction(descripcion, planeta, imagen_name, activo, cord_x, cord_y, cord_z) 
            return redirect(url_for('GestionarSectoresPerdidos'))
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('formLogin'))


@app.route('/minecraft/sectoresPerdidos/edit/<int:id>', methods=['GET'])
async def EditSectorPerdido(id):
    if 'id' in session:
        if session['role'] == 'Ejecutivo' or session['role'] == 'Staff':
            sectorPerdido = await SectoresPerdidos.GetSectorPerdido(id)
            return render_template('/paginas/minecraft_subpg/server/sectoresPerdidos/edit.jinja', sectorPerdido=sectorPerdido, session=session)
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('formLogin'))

@app.route('/minecraft/sectoresPerdidos/editing/<int:id>', methods=['POST'])
async def EditarSectorPerdido(id):
    if 'id' in session:
        if session['role'] == 'Ejecutivo' or session['role'] == 'Staff':
            descripcion = request.form['descripcion']
            imagen_name = None
            
            if 'imagen' not in request.files or request.files['imagen'].filename == '':
                imagen_name = None
            else:
                imagen = request.files['imagen']
                imagen_name = secure_filename(imagen.filename)
                imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_name))
                
            activo = request.form['activo']
            planeta = request.form['planeta']
            cord_x = request.form['cord_x']
            cord_y = request.form['cord_y']
            cord_z = request.form['cord_z']
            
            await SectoresPerdidos.EditarSectorPerdidoAction(id, descripcion, planeta, imagen_name, activo, cord_x, cord_y, cord_z)
            
            return redirect(url_for('GestionarSectoresPerdidos'))
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('formLogin'))

@app.route('/minecraft/sectoresPerdidos/delete/<int:id>', methods=['GET'])
async def DeleteSectorPerdido(id):
    if 'id' in session:
        if session['role'] == 'Ejecutivo' or session['role'] == 'Staff':
            await SectoresPerdidos.DeleteSectorPerdidoAction(id)
            return redirect(url_for('GestionarSectoresPerdidos'))
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('formLogin'))
################################################################################################


if __name__ == '__main__':
    bot_thread = Thread(target=bot.run(datos['discord']['token']))
    bot_thread.start()
    