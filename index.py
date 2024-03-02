import os 
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for
import mysql.connector
import json
import random
import asyncio

BOT_TOKEN = "OTY3NDI3OTY2NTQxOTE0MTUy.GipCDy.wTD5b3vCMW-GGqo9RaCkQ9jS_GH-lwPnlEtBoA"

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = discord.Client(intents=intents)

app = Flask(__name__)
app.secret_key = "tr4rt34t334yt"

async def AbrirConexionSQL():
    conection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ikero9090",
        database="MINECRAFTPG",
        auth_plugin="mysql_native_password"
    )
    return conection

##########################################################################################
######## Funciones del código lógico del procesamiento en el servidor ####################
##########################################################################################

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
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM PERSONAJES;
    """)
    result = cursor.fetchall()
    columnas = [column[0] for column in cursor.description]
    resultados_json = []
    for fila in result:
        fila_json = dict(zip(columnas, fila))
        resultados_json.append(fila_json)    
    conexion.close()
    return resultados_json

async def ObtenerPersonaje(name):
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT PERSONAJES.id, PERSONAJES.name, PERSONAJES.descripcion, PERSONAJES.color, PERSONAJES.imgUrl, PERSONAJES.idUser, PERSONAJES.idDiario, USUARIO.name AS userNAme
        FROM PERSONAJES INNER JOIN USUARIO
            ON PERSONAJES.idUser = USUARIO.idUser
        WHERE USUARIO.name = '{name}';
    """)
    result = cursor.fetchall()
    columnas = [column[0] for column in cursor.description]
    resultados_json = []
    for fila in result:
        fila_json = dict(zip(columnas, fila))
        resultados_json.append(fila_json)
    conexion.close()
    return resultados_json

async def ValidarDatosLogin(idUser, passwd):
    listaPersonajes = await ObtenerListaPersonajes()
    valido = False
    for personaje in listaPersonajes:
        if personaje["idUser"] == idUser and personaje["passwd"] == passwd:
            valido = True
    return valido

async def ValidarUsuario(idUser):
    listaUsuarios = await ListUsers()
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

async def ObtenerObjetoUsuario(idUser):
    listaUsuarios = await ListUsers(bot)
    usuario = 'null'
    for user in listaUsuarios:
        if user.id == int(idUser):
            usuario = user
            break
    return usuario

async def ObtenerObjetoUsuarioNombre(nombre):
    listaUsuarios = await ListUsers(bot)
    usuario = 'null'
    for user in listaUsuarios:
        if nombre == user.name:
            usuario = user
            break
    return usuario

async def ObtenerPersonajePorIdUser(idUser):
    listaPersonajes = await ObtenerListaPersonajes()
    result = {}
    for personaje in listaPersonajes:
        if personaje["idUser"] == idUser:
            result = personaje
            break
    return result


async def ObtenerPaginas():
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM DIARIO;")
    result = cursor.fetchall()
    columnas = [column[0] for column in cursor.description]
    resultados_json = []
    for fila in result:
        fila_json = dict(zip(columnas, fila))
        resultados_json.append(fila_json)
    conexion.close()
    return resultados_json

async def UsuarioEnElServidor(idUser):
    listaUsuarios = []
    listaUsuarios = await ListUsers(bot)
    valido = False
    for user in listaUsuarios:
        if user.id == int(idUser):
            valido = True
            break
    return valido
        

#######################################################################################

#######################################################################################
# Funciones y eventos del bot del Discord de pana Gaming ##############################
#######################################################################################
@bot.event
async def on_ready():
    app.run(port=8001)

#######################################################################################

#######################################################################################
# Paginas de respuesta con procesamiento en el Servidor ###############################
#######################################################################################


######### PAGINAS SIN SESIÓN ##########################
@app.route("/")
def Inicio():
    if "id" in session:
        return render_template("/paginas/index2.html", session = session)
    else:
        return render_template("index.html")

@app.route("/contacto")
def contacto():
    return render_template("/paginas/contact.html")

@app.route("/cerrarSesion")
async def cerrarSesion():
    session.clear()
    return redirect(url_for("Inicio"))

@app.route('/comunidad')
async def comunidad1():
    userList = await ListUsers(bot)
    ejecList = await MostrarEjecutivos(userList)
    staffList = await MostrarStaff(userList, ejecList)
    memberList = await MostrarMiembros(userList, staffList, ejecList)
    if "id" in session:
        return render_template("/paginas/comunidad.html", ejecList=ejecList, staffList=staffList, memberList=memberList, session=session)
    else:
        return render_template("comunidad1.html", ejecList=ejecList, staffList=staffList, memberList=memberList)


@app.route('/formLogin')
def formLogin():
    return render_template("login.html")

@app.route('/formRegister')
def formRegister():
    return render_template("registrar.html")
########################################################

########### PROCESAMIENTO DE SESION ####################

async def ComprobarUsuarioRepetido(idUser):
    conexion = await AbrirConexionSQL()
    repite = False
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM USUARIO;
    """)
    result = cursor.fetchall()
    columnas = [column[0] for column in cursor.description]
    resultados_json = []
    for fila in result:
        fila_json = dict(zip(columnas, fila))
        resultados_json.append(fila_json)
    for usuario in resultados_json:
        if str(usuario['idUser']) == idUser:
            repite = True
            break     
    conexion.close()
    return repite

async def ValidarInicioSesion(name, passwd):
    conexion = await AbrirConexionSQL()
    valido = False
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM USUARIO;
    """)
    result = cursor.fetchall()
    columnas = [column[0] for column in cursor.description]
    resultados_json = []
    for fila in result:
        fila_json = dict(zip(columnas, fila))
        resultados_json.append(fila_json) 
    for usuario in resultados_json:
        if usuario['name'] == name and usuario['passwd'] == passwd:
            valido = True
            break
    conexion.close()
    return valido

async def comprobarSiTienePersonaje(idUser):
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM PERSONAJES;
    """)
    result = cursor.fetchall()
    columnas = [column[0] for column in cursor.description]
    resultados_json = []
    for fila in result:
        fila_json = dict(zip(columnas, fila))
        resultados_json.append(fila_json) 
    print(resultados_json)
    tiene = False
    for personaje in resultados_json:
        if personaje['idUser'] == idUser:
            tiene = True
            break
    return tiene


@app.route('/CrearCuenta', methods=['GET', 'POST'])
async def CrearCuenta():
    idUser = request.form['idUser']
    passwd = request.form['passwd']
    passwd2 = request.form['passwd2']
    usuarioRepetido = await ComprobarUsuarioRepetido(idUser)
    if usuarioRepetido == False:
        if passwd == passwd2:
            conexion = await AbrirConexionSQL()
            cursor = conexion.cursor()
            cursor.execute(f"""
                INSERT INTO USUARIO (idUser, passwd)
                VALUES ('{idUser}', '{passwd}');                  
            """)
            user = await ObtenerObjetoUsuario(idUser)
            conexion.commit()
            conexion.close()
            session["id"] = idUser
            session["name"] = user.name
            session["imgUrl"] = user.avatar.url
            return render_template("/paginas/index2.html", session=session)
    else:
        return redirect(url_for("formRegister"))
    

@app.route('/IniciarSesion', methods=['GET', 'POST'])
async def IniciarSesion():
    name = request.form["dName"]
    passwd = request.form["passwd"]
    valido = await ValidarInicioSesion(name, passwd)
    if valido == True:
        user = await ObtenerObjetoUsuarioNombre(name)
        session["id"] = str(user.id)
        session["name"] = user.name
        session["imgUrl"] = user.avatar.url
        return render_template("/paginas/index2.html", session=session)
    else:
        errorMsg = "No existe el usuario introducido."
        return render_template("login.html", errorMsg = errorMsg)

#####################################################

###### PÁGINAS CON SESIÓN ##########################
@app.route('/principal')
async def principal():
    if "id" in session:
        return render_template("/paginas/index2.html", session=session)
    else:
        return redirect(url_for('formLogin'))
    
@app.route("/minecraft")
def minecraft():
    if "id" in session:
        return render_template("/paginas/minecraft.html", session=session)
    else:
        return redirect(url_for('formLogin'))

@app.route("/comunidad")
async def comunidad():
    if "id" in session:
        userList = await ListUsers(bot)
        ejecList = await MostrarEjecutivos(userList)
        staffList = await MostrarStaff(userList, ejecList)
        memberList = await MostrarMiembros(userList, staffList, ejecList)
        return render_template("/paginas/comunidad.html", ejecList=ejecList, staffList=staffList, memberList=memberList, session=session)    
    else:
        return redirect(url_for('formLogin'))

@app.route('/mineacraft/gameplay')
async def portalServer():
    if "id" in session:
        return render_template('/paginas/minecraft_subpg/history/portalMc.html', session=session)
    else:
        return redirect(url_for('formLogin'))

@app.route("/mineacraft/personajes/NuevoPersonaje")
async def NuevoPersonaje():
    if "id" in session:
        return render_template("/paginas/minecraft_subpg/personajes/formPersonajes.html", session=session)
    else:
        return redirect(url_for('formLogin'))

@app.route("/mineacraft/personajes/CrearPersonaje", methods=["GET","POST"])
async def CrearPersonaje():
    name = request.form['pjName']
    descripcion = request.form['pjDescription']
    imgUrl = request.form['pjImgUrl']
    color = request.form['color']
    if 'id' in session:
        codError = await ValidarPersonajeUsuario(session['id'], name)
        if codError == 0:
            conexion = await AbrirConexionSQL()
            cursor = conexion.cursor()
            cursor.execute(f"""
                INSERT INTO PERSONAJES (name, descripcion, color, imgUrl, idUser)
                VALUES ('{name}', '{descripcion}', '{color}', '{imgUrl}', '{session['id']}');
            """)
            conexion.commit()
            conexion.close()
            return render_template("/paginas/minecraft_subpg/personajes/personajeCreated.html", name=name, descripcion=descripcion, imgUrl=imgUrl, session=session)
        elif codError == 1:
            errorMsg = "Solo puedes tener un solo personaje. Si quieres cambiar de personaje editalo para que sea distinto."
            return render_template("/paginas/minecraft_subpg/personajes/formPersonajes.html", errorMsg = errorMsg, session=session)   
        elif codError == 2:
            errorMsg = "El nombre del personajes que intentas implementar está ya en uso. Porfavor, escoja otro que esté en desuso en el servidor."
            return render_template("/paginas/minecraft_subpg/personajes/formPersonajes.html", errorMsg = errorMsg, session=session)
    else:
        return redirect(url_for('formLogin'))

@app.route("/minecraft/PersonajesMinecraftPG")
async def PersonajesMinecraftPG():
    if "id" in session:
        listaPersonajes = []
        paginas = []  
        listaPersonajes = await ObtenerListaPersonajes()
        paginas = await ObtenerPaginas()
        tienePersonaje = await comprobarSiTienePersonaje(session["id"])
        if tienePersonaje == True:
            return render_template("/paginas/minecraft_subpg/personajes/portalPersonajesMC2.html", listaPersonajes = listaPersonajes, session=session, paginas=paginas)
        else:
            return render_template("/paginas/minecraft_subpg/personajes/portalPersonajesMC.html", listaPersonajes = listaPersonajes, session=session, paginas=paginas)
    else:
        return redirect(url_for("formLogin"))

@app.route("/LoginEditPersonaje")
async def LoginEditPersonaje():
    return render_template("/paginas/minecraft_subpg/personajes/loginEditPersonaje.html")

@app.route("/minecraft/personajes/FormEditPersonaje")
async def FormEditPersonaje():
    if "id" in session:
        conexion = await AbrirConexionSQL()
        cursor = conexion.cursor()
        cursor.execute(f"""
            SELECT PERSONAJES.id, PERSONAJES.name, PERSONAJES.descripcion, PERSONAJES.color, PERSONAJES.imgUrl, PERSONAJES.idUser
            FROM PERSONAJES INNER JOIN USUARIO
                ON PERSONAJES.idUser = USUARIO.idUser;
        """)
        result = cursor.fetchall()
        columnas = [column[0] for column in cursor.description]
        resultados_json = []  
        for fila in result:
            fila_json = dict(zip(columnas, fila))
            resultados_json.append(fila_json)
        personaje = {}
        for per in resultados_json:
            if per["idUser"] == session["id"]:
                personaje = per
        conexion.close()
        return render_template("/paginas/minecraft_subpg/personajes/editPersonaje.html", personaje=personaje, session=session)
    
    else:
        return redirect(url_for("Inicio"))

@app.route("/mineacraft/personajes/EditPersonaje", methods=["GET", "POST"])
async def EditPersonaje():
    name = request.form["pjName"]
    color = request.form["color"]
    descripcion = request.form["pjDescription"]
    imgUrl = request.form["pjImgUrl"]
    idUser = request.form["idUser"]
    userValid = await ValidarPersonajeEditado(idUser, name)
    if userValid == 0:
        conexion = await AbrirConexionSQL()
        cursor = conexion.cursor()
        cursor.execute(f"""
            UPDATE PERSONAJES
            SET name = '{name}', color = '{color}', descripcion = '{descripcion}', imgUrl = '{imgUrl}'
            WHERE idUser = '{idUser}';
        """)
        conexion.commit() 
        #conexion.commit()
        conexion.close()
        #personaje = await ObtenerPersonajePorIdUser(idUser)
        return redirect(url_for("FormEditPersonaje"))
    else:
        errorMsg = "El nombre introducido esta ya en uso, escoja otro porfavor."
        personaje = await ObtenerPersonajePorIdUser(idUser)
        return render_template("/paginas/minecraft_subpg/personajes/editPersonaje.html", personaje=personaje, errorMsg=errorMsg, session=session)

@app.route('/soporte')
async def soporte():
    if "id" in session:
        return render_template('/paginas/tikets.html', session=session)
    else:
        return redirect(url_for("formLogin"))

@app.route('/enviarTiket', methods=["GET", "POST"])
async def enviarTiket():
    userName = request.form["userName"]
    texto = request.form["texto"]
    channel = bot.get_channel(int(1180858213982273617))
    usuario = await ObtenerObjetoUsuario(userName)
    if usuario != 'null':
        embed = discord.Embed(
            title=f"**TIKET DE {usuario.name}**",
            description=f"{texto}",
            color=discord.Color.random()
        )
        bot.loop.create_task(channel.send(embed=embed))
        return render_template("/paginas/tiketSended.html", usuario=usuario, texto=texto, session=session)  
    else:
        errorMsg = f"No se ha encontrado ningún usuario con el nombre {userName} en el servidor de Discord."
        return render_template("/paginas/tikets.html", errorMsg=errorMsg, session=session)


@app.route('/mineacraft/personajes/diario/nuevaPagina')
async def nuevaPagina():
    if "id" in session:
        return render_template("/paginas/minecraft_subpg/personajes/diarios/nuevaPagina.html", session=session)
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


@app.route('/mineacraft/personajes/diario/VerDiario', methods=["GET", "POST"])
async def VerDiario():
    if "id" in session:
        idPersonaje = request.form["idPersonaje"]
        nombre = request.form["nombre"]
        imgUrl = request.form["imgUrl"]
        color = request.form["color"]
        conexion = await AbrirConexionSQL()
        cursor = conexion.cursor()
        cursor.execute(f"""
            SELECT * FROM DIARIO
            WHERE idPersonaje = {idPersonaje};
        """)
        result = cursor.fetchall()
        columnas = [column[0] for column in cursor.description]
        paginas = []
        for fila in result:
            fila_json = dict(zip(columnas, fila))
            paginas.append(fila_json)    
        conexion.close()
        return render_template("/paginas/minecraft_subpg/personajes/diarios/diario.html", paginas=paginas, nombre=nombre, imgUrl=imgUrl, color=color)
    else:
        return redirect(url_for('formLogin'))

@app.route('/mineacraft/personajes/diario/EditarDiario')
async def EditarDiario():
    if "id" in session:
        personaje = await ObtenerPersonajePorIdUser(session['id'])
        listaPaginas = await ObtenerPaginas()
        paginas = []
        for page in listaPaginas:
            if page['idPersonaje'] == personaje['id']:
                paginas.append(page)
        return render_template("/paginas/minecraft_subpg/personajes/diarios/editDiario.html", paginas=paginas, nombre=personaje['name'], imgUrl=personaje['imgUrl'], color=personaje['color'])
    else:
        return redirect(url_for('formLogin'))


@app.route('/EditarPagina', methods=['GET', 'POST'])
async def EditarPagina():
    if "id" in session:
        idPagina = request.form["idPagina"]
        contenido = request.form["contenido"]
        conexion = await AbrirConexionSQL()
        cursor = conexion.cursor()
        cursor.execute(f"""
            UPDATE DIARIO
                SET contenido = '{contenido}'
            WHERE idPagina = {idPagina};
        """)
        conexion.commit()
        conexion.close()
        return redirect(url_for("EditarDiario"))
    else:
        return redirect(url_for("formLogin"))
    
    
###########################################################################################################################################


if __name__ == '__main__':
    bot.run(BOT_TOKEN)