import os 
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for
import mysql.connector
import json
import random
import asyncio
from Personajes import *
from database import *
from UsuarioController import *

datos = {}
with open('settings.json') as archivo:
    datos = json.load(archivo)

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.message_content = True
bot = discord.Client(intents=intents)

async def ListUsers():
    guild = bot.get_guild(int(datos["discord"]["server"]["id"]))
    list = []
    print(guild)
    for m in guild.members: 
        list.append(m)
    return list

async def MostrarEjecutivos(userList):
    guild = bot.get_guild(int(datos["discord"]["server"]["id"]))
    ejecRole = guild.get_role(datos["discord"]["roles"]["ejecutive"])
    ejec = []
    for user in userList:
        if ejecRole in user.roles:
            ejec.append(user)
    return ejec

async def MostrarStaff(userList, ejecList):
    guild = bot.get_guild(int(datos["discord"]["server"]["id"]))
    staffRole = guild.get_role(datos["discord"]["roles"]["staff"])
    staff = []
    for user in userList:
        if staffRole in user.roles:
            encontrado = False
            for r in ejecList:
                if user == r:
                    encontrado = True
            if encontrado == False:
                staff.append(user)
    return staff

async def MostrarMiembros(userList, staffList, ejecList):
    guild = bot.get_guild(int(datos["discord"]["server"]["id"]))
    memberRole = guild.get_role(datos["discord"]["roles"]["member"])
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

async def ObtenerObjetoUsuario(idUser):
    listaUsuarios = await ListUsers()
    usuario = 'null'
    for user in listaUsuarios:
        if user.id == int(idUser):
            usuario = user
            break
    return usuario

async def ComprobarNombreDiscord(nombre):
    valido = False
    listaUsuario = await ListUsers()
    for user in listaUsuario:
        if user.name == nombre:
            valido = True
    return valido

async def UsuarioEnElServidor(idUser):
    listaUsuarios = []
    listaUsuarios = await ListUsers()
    valido = False
    for user in listaUsuarios:
        if user.id == int(idUser):
            valido = True
            break
    return valido

async def ObtenerObjetoUsuarioNombre(nombre):
    listaUsuarios = await ListUsers()
    usuario = 'null'
    for user in listaUsuarios:
        if nombre == user.name:
            usuario = user
            break
    return usuario

async def ObtenerObjetoUsuario(idUser):
    listaUsuarios = await ListUsers()
    usuario = 'null'
    for user in listaUsuarios:
        if user.id == int(idUser):
            usuario = user
            break
    return usuario

async def comprobarSiTienePersonaje(idUser):
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM PERSONAJES;
    """)
    result = cursor.fetchall()
    resultados_json = await ConvertirJSON(result, cursor)
    tiene = False
    for personaje in resultados_json:
        if personaje['idUser'] == idUser:
            tiene = True
            break
    conexion.close()
    return tiene

async def ValidarUsuario(idUser):
    listaUsuarios = await ListUsers()
    valido = False
    for u in listaUsuarios:
        if idUser == u.id:
            valido = True
    return valido

async def ComprobarUsuarioRepetido(idUser):
    conexion = await AbrirConexionSQL()
    repite = False
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM USUARIO;
    """)
    result = cursor.fetchall()
    resultados_json = await ConvertirJSON(result, cursor)
    for usuario in resultados_json:
        if str(usuario['idUser']) == idUser:
            repite = True
            break     
    conexion.close()
    return repite

async def ValidarInicioSesion(passwd):
    conexion = await AbrirConexionSQL()
    valido = False
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM USUARIO;
    """)
    result = cursor.fetchall()
    resultados_json = await ConvertirJSON(result, cursor)
    for usuario in resultados_json:
        if usuario['passwd'] == passwd:
            valido = True
            break
    conexion.close()
    return valido

async def ObtenerUsuario(idUser):
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT USUARIO.descripcion AS descripcion, STYLE_USUARIO.main AS main, STYLE_USUARIO.banner
        FROM USUARIO INNER JOIN STYLE_USUARIO
            ON USUARIO.idUser = STYLE_USUARIO.idUser
        WHERE USUARIO.idUser = {idUser};
    """)
    result = cursor.fetchall()
    resultadoJson = await ConvertirJSON(result, cursor)
    conexion.close()
    print(resultadoJson)
    return resultadoJson[0]


guild = bot.get_guild(793956939687133184)

app = Flask(__name__)
app.secret_key = "tr4rt34t334yt"

#######################################################################################
# Funciones y eventos del bot del Discord de pana Gaming ##############################
#######################################################################################

@bot.event
async def on_ready():
    app.run(
        port = datos["flask"]["port"], 
        host = datos["flask"]["host"]
    )

#######################################################################################

#######################################################################################
# Paginas de respuesta con procesamiento en el Servidor ###############################
#######################################################################################

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
    userList = await ListUsers()
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


@app.route('/CrearCuenta', methods=['GET', 'POST'])
async def CrearCuenta():
    idUser = request.form['idUser']
    passwd = request.form['passwd']
    passwd2 = request.form['passwd2']
    descripcion = request.form['descripcion']

    usuarioRepetido = await ComprobarUsuarioRepetido(idUser)
    if usuarioRepetido == False:
        if passwd == passwd2:
            user = await ObtenerObjetoUsuario(idUser)
            conexion = await AbrirConexionSQL()
            cursor = conexion.cursor()
            cursor.execute(f"""
                INSERT INTO USUARIO (idUser, passwd, descripcion)
                VALUES ('{idUser}', '{passwd}', '{descripcion}');                
            """)
            conexion.commit()
            cursor.execute(f"""
                INSERT INTO STYLE_USUARIO (idUser, main, banner)
                VALUES({idUser}, null, null);
            """)
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
    valido = await ValidarInicioSesion(passwd)
    if valido == True:
        if await ComprobarNombreDiscord(name) == True:
            user = await ObtenerObjetoUsuarioNombre(name)
            session["id"] = str(user.id)
            session["name"] = user.name
            session["imgUrl"] = user.avatar.url
            return render_template("/paginas/index2.html", session=session)
        else:
            errorMsg = "El nombre introducido no coincide con ningun usuario."
            return render_template("login.html", errorMsg=errorMsg)
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
        userList = await ListUsers()
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
            conexion = await AbrirConexionSQL()
            cursor = conexion.cursor()
            cursor.execute(f"""
                INSERT INTO PERSONAJES (name, descripcion, color, imgUrl, idUser, raza, edad, sexo)
                VALUES ('{name}', '{descripcion}', '{color}', '{imgUrl}', '{session['id']}', '{raza}', '{edad}', '{sexo}');
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

@app.route("/minecraft/personajes")
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

@app.route("/minecraft/personajes/FormEditPersonaje")
async def FormEditPersonaje():
    if "id" in session:
        personaje = await ObtenerPersonajePorIdUser(str(session['id']))
        print(personaje)
        return render_template("/paginas/minecraft_subpg/personajes/editPersonaje.html", personaje=personaje[0], session=session)
    else:
        return redirect(url_for("Inicio"))

@app.route("/minecraft/personajes/detalles/<int:idPersonaje>", methods=["GET"])
async def VerInfoPersonaje(idPersonaje):
    if 'id' in session:
        personaje = await ObtenerPersonajePorId(idPersonaje)
        print(personaje)
        return render_template("/paginas/minecraft_subpg/personajes/detalles.html", personaje=personaje[0], session=session) 
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
        conexion = await AbrirConexionSQL()
        cursor = conexion.cursor()
        cursor.execute(f"""
            UPDATE PERSONAJES
            SET name = '{name}', 
                color = '{color}', 
                descripcion = '{descripcion}', 
                imgUrl = '{imgUrl}', raza = '{raza}', 
                edad = {edad}, 
                sexo = '{sexo}'
            WHERE idUser = '{idUser}';
        """)
        conexion.commit() 
        conexion.close()
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
        paginas = await ConvertirJSON(result, cursor)    
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

@app.route('/usuario/me/<int:id>', methods=['GET'])
async def MiPerfil(id):
    if 'id' in session:
        appUser = await ObtenerUsuario(id)
        dUser = await ObtenerObjetoUsuario(id)
        result = {"avatar": dUser.avatar.url, "name":dUser.name, "mote":dUser.nick, "descripcion":appUser["descripcion"], "main":appUser["main"], "banner":appUser["banner"]}
        return render_template('/paginas/users/myProfile.html', user=result, session=session)
    else:
        return redirect(url_for("formLogin"))



#-----------------------------------------------------------------------#
#-------------------- USUARIOS -----------------------------------------#
#-----------------------------------------------------------------------#


@app.route('/usuario/edit/descripcion/<int:id>', methods=["GET","POST"])
async def EditMyDescription(id):
    if 'id' in session:
        descripcion = request.form["descripcion"]
        conexion = await AbrirConexionSQL()
        cursor = conexion.cursor()
        cursor.execute(f"""
            UPDATE USUARIO
                SET descripcion = '{descripcion}'
            WHERE idUser = {id};
        """)
        conexion.commit()
        conexion.close()
        return redirect(url_for('MiPerfil', id=id))
    else:
        return redirect(url_for("formLogin"))

@app.route('/usuario/edit/style/<int:id>', methods=["GET"])
async def EditUserStyle(id):
    if 'id' in session:
        appUser = await ObtenerUsuario(id)
        dUser = await ObtenerObjetoUsuario(id)
        print(appUser["main"])
        result = {"avatar": dUser.avatar.url, "name":dUser.name, "mote":dUser.nick, "descripcion":appUser["descripcion"], "main":appUser["main"], "banner":appUser["banner"] }
        return render_template('/paginas/users/styleProfile.html', user=result, session=session)
    else:
        return redirect(url_for("formLogin"))


@app.route('/usuario/edit/style/newMainBk/<int:id>', methods=["POST"])
async def SetUserBackground(id):
    mainBk = request.form["mainBk"]
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        UPDATE STYLE_USUARIO
            SET main = '{mainBk}'
        WHERE idUser = {id};
    """)
    conexion.commit()
    conexion.close()
    return redirect(url_for('EditUserStyle', id=id))
###########################################################################################################################################

if __name__ == '__main__':
    bot.run(datos["discord"]["token"])