import os 
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
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

import globals

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

session = app.session

minecraft_bp = Blueprint('minecraft', __name__)


@minecraft_bp.route("/characters")
async def characters_mc():
    if "id" in session:
        listaPersonajes = []
        paginas = []  
        listaPersonajes = await characters.GetCharacterList()

        has_character = await users.comprobarSiTienePersonaje(session["id"])
        if has_character:
            return render_template("/paginas/minecraft_subpg/personajes/portalPersonajesMC2.jinja", listaPersonajes = listaPersonajes, session=session, paginas=paginas)
        else:
            return render_template("/paginas/minecraft_subpg/personajes/portalPersonajesMC.jinja", listaPersonajes = listaPersonajes, session=session, paginas=paginas)
    else:
        return redirect(url_for("login"))


@minecraft_bp.route("characters/me/new", methods=['GET', 'POST'])
async def new_character():
    if "id" in session:
        if request.method == 'POST':
            name = request.form['pjName']
            descripcion = request.form['pjDescription']
            color = request.form['color']
            raza = request.form['raza']
            edad = request.form['edad']
            sexo = request.form['sexo']
            tipo = request.form['type']
            
            imagen_name = None
            
            if 'imagen' not in request.files or request.files['imagen'].filename == '':
                imagen_name = None
            else:
                imagen = request.files['imagen']
                imagen_name = secure_filename(imagen.filename)
                imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_name))
        
            await characters.new_character(name, descripcion, color, imagen_name, session['id'], raza, edad, sexo, tipo)
            return redirect(url_for('minecraft.characters_mc'))
        else:
            return render_template("/paginas/minecraft_subpg/personajes/formPersonajes.jinja", session=session)
    else:
        return redirect(url_for('login'))
    
    
@minecraft_bp.route("/character/me/edit", methods=['GET', 'POST'])
async def edit_character():
    if "id" in session:
        if request.method == 'POST':
            name = request.form["name"]
            color = request.form["color"]
            descripcion = request.form["pjDescription"]
            raza = request.form['raza']
            edad = request.form['edad']
            
            imagen_name = None
            
            if 'imagen' not in request.files or request.files['imagen'].filename == '':
                imagen_name = None
            else:
                imagen = request.files['imagen']
                imagen_name = secure_filename(imagen.filename)
                imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_name))
            
            await characters.edit_character(name, color, descripcion, imagen_name, session['id'], raza, edad)
            personaje = await characters.get_character_by_id_user(str(session['id']))
            return render_template('/paginas/minecraft_subpg/personajes/editPersonaje.jinja', personaje=personaje, session=session)
        else:
            personaje = await characters.get_character_by_id_user(str(session['id']))
            return render_template("/paginas/minecraft_subpg/personajes/editPersonaje.jinja", personaje=personaje, session=session)
    else:
        return redirect(url_for("login"))
    
    
@minecraft_bp.route("/character/me", methods=["GET"])
async def my_character():
    if 'id' in session:
        personaje = await characters.get_character_by_id_user(session['id'])
        return render_template('/paginas/minecraft_subpg/personajes/miPersonaje.jinja', personaje=personaje[0], session=session)
    
    else:
        return redirect(url_for("login"))



@minecraft_bp.route("/characters/<int:id>", methods=["GET"])
async def character_details(id):
    if 'id' in session:
        paginas = []
        personaje = await characters.GetCharacterById(id)
        paginas = await diary.get_character_diario_pages(id)

        return render_template("/paginas/minecraft_subpg/personajes/personaje.jinja", personaje=personaje, paginas=paginas, session=session) 
    else:
        return redirect(url_for('login'))


@minecraft_bp.route('/character/me/diario/edit', methods=['POST'])
async def EditarPagina():
    if "id" in session:
        idPagina = request.form["idPagina"]
        contenido = request.form["contenido"]
        await diary.update_diario_page(idPagina, contenido)
        return redirect(url_for("minecraft.MiDiario"))
    else:
        return redirect(url_for("login"))

@minecraft_bp.route('/character/me/diario', methods=['GET'])
async def MiDiario():
    if "id" in session:
        personaje = await characters.get_character_by_id_user(session['id'])
        pages = await diary.get_character_diario_pages(int(personaje['id']))
        
        return render_template("/paginas/minecraft_subpg/personajes/miDiario.jinja", paginas=pages, personaje=personaje, session=session)
    else:
        return redirect(url_for("login"))

@minecraft_bp.route('/character/me/diario/newPage/<int:idPersonaje>', methods=['GET'])
async def NewPage(idPersonaje):
    if 'id' in session:
        await diary.create_page(idPersonaje)
        return redirect(url_for("minecraft.MiDiario"))
    else:
        return redirect(url_for("login"))

@minecraft_bp.route('/character/me/diario/deletePage/<int:idPagina>', methods=["GET"])
async def DeletePage(idPagina):
    if 'id' in session:
        await diary.delete_page(idPagina)
        return redirect(url_for("minecraft.MiDiario"))
    else:
        return redirect(url_for("login"))

    
@minecraft_bp.route('/server', methods=['GET'])
async def minecraftServer():
    if 'id' in session:
        sectoresPerdidos = await lost_sectors.get_all_lost_sectors()
        misiones = await missions.get_all_missions()
        return render_template('/paginas/minecraft_subpg/server/minecraftServer.jinja', sectoresPerdidos=sectoresPerdidos, misiones=misiones, session=session)
    else:
        return redirect(url_for('login'))






"""
    SECTORES PERDIDOS
"""
@minecraft_bp.route('/SectoresPerdidos', methods=["GET"])
async def GestionarSectoresPerdidos():
    if 'id' in session:
        if session['role'] == 'Ejecutivo' or session['role'] == 'Staff':
           sectoresPerdidosList = await lost_sectors.get_all_lost_sectors()
           return render_template('/paginas/minecraft_subpg/server/sectoresPerdidos/sectorsIndex.jinja', sectoresPerdidos=sectoresPerdidosList, session=session)
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('login'))

@minecraft_bp.route('/SectoresPerdidos/create', methods=['GET'])
async def NewSectorPerdido():
    if 'id' in session:
        if session['role'] == 'Ejecutivo' or session['role'] == 'Staff':
            return render_template('/paginas/minecraft_subpg/server/sectoresPerdidos/create.jinja', session=session)
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('login'))

@minecraft_bp.route('/SectoresPerdidos/new', methods=['POST'])
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
            
            await lost_sectors.create_lost_sector(descripcion, planeta, imagen_name, activo, cord_x, cord_y, cord_z) 
            return redirect(url_for('minecraft.GestionarSectoresPerdidos'))
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('login'))


@minecraft_bp.route('/SectoresPerdidos/edit/<int:id>', methods=['GET'])
async def EditSectorPerdido(id):
    if 'id' in session:
        if session['role'] == 'Ejecutivo' or session['role'] == 'Staff':
            sectorPerdido = await lost_sectors.get_lost_sector_by_id(id)
            return render_template('/paginas/minecraft_subpg/server/sectoresPerdidos/edit.jinja', sectorPerdido=sectorPerdido, session=session)
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('login'))

@minecraft_bp.route('/SectoresPerdidos/editing/<int:id>', methods=['POST'])
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
            
            await lost_sectors.edit_lost_sector(id, descripcion, planeta, imagen_name, activo, cord_x, cord_y, cord_z)
            return redirect(url_for('minecraft.GestionarSectoresPerdidos'))
        
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('login'))

@minecraft_bp.route('/SectoresPerdidos/delete/<int:id>', methods=['GET'])
async def DeleteSectorPerdido(id):
    if 'id' in session:
        if session['role'] == 'Ejecutivo' or session['role'] == 'Staff':
            await lost_sectors.delete_lost_sector(id)
            return redirect(url_for('minecraft.GestionarSectoresPerdidos'))
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('login'))








################## [MISIONES] ##########################

#### [ ADMIN ] ######
@minecraft_bp.route('/misiones', methods=['GET'])
async def GestionarMisiones():
    if 'id' in session:
        if session['role'] == 'Staff' or session['role'] == 'Ejecutivo':
            misiones = await missions.get_all_missions()
            return render_template('/paginas/minecraft_subpg/server/misiones/indexMisiones.jinja', misiones=misiones, session=session)            
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('login'))

@minecraft_bp.route('/misiones/new', methods=['GET', 'POST'])
async def NuevaMision():
    if 'id' in session:
        if session['role'] == 'Staff' or session['role'] == 'Ejecutivo':
            if request.method == 'GET':
                return render_template('/paginas/minecraft_subpg/server/misiones/create.jinja', session=session)
            else:
                descripcion = request.form['descripcion']
                tipo = request.form['tipo']
                dificultad = request.form['dificultad']
                estado = request.form['estado']
                grupo = request.form['grupo']
                guerrero = request.form['allowGuerrero']
                aventurero = request.form['allowAventurero']
                hechicero = request.form['allowHechicero']
                
                imagen_name = None
                
                if 'imagen' not in request.files or request.files['imagen'].filename == '':
                    imagen_name = None
                else:
                    imagen = request.files['imagen']
                    imagen_name = secure_filename(imagen.filename)
                    imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_name))
                
                await missions.create_mission(descripcion, tipo, imagen_name, dificultad, estado, grupo, guerrero, aventurero, hechicero)
                
                return redirect(url_for('minecraft.GestionarMisiones'))
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('login'))
    

@minecraft_bp.route('/misiones/edit/<int:id>', methods=['GET', 'POST'])
async def EditarMision(id):
    if 'id' in session:
        if session['role'] == 'Staff' or session['role'] == 'Ejecutivo':
            if request.method == 'GET':
                mision = await missions.get_mission_by_id(id)
                return render_template('/paginas/minecraft_subpg/server/misiones/edit.jinja', mision=mision, session=session)
            else:
                descripcion = request.form['descripcion']
                tipo = request.form['tipo']
                dificultad = request.form['dificultad']
                estado = request.form['estado']
                grupo = request.form['grupo']
                guerrero = request.form['allowGuerrero']
                aventurero = request.form['allowAventurero']
                hechicero = request.form['allowHechicero']
                
                imagen_name = None
                
                if 'imagen' not in request.files or request.files['imagen'].filename == '':
                    imagen_name = None
                else:
                    imagen = request.files['imagen']
                    imagen_name = secure_filename(imagen.filename)
                    imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_name))

                await missions.update_mission(id, descripcion, tipo, imagen_name, dificultad, estado, grupo, guerrero, aventurero, hechicero)
                return redirect(url_for('minecraft.GestionarMisiones'))
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('login'))
    
@minecraft_bp.route('/misiones/delete/<int:id>', methods=['GET'])
async def BorrarMision(id):
    if 'id' in session:
        if  session['role'] == 'Staff' or session['role'] == 'Ejecutivo':
            await missions.delete_mission(id)
            return redirect(url_for('minecraft.GestionarMisiones'))
        
        else:
            return redirect(url_for('minecraft'))
    else:
        return redirect(url_for('login'))

@minecraft_bp.route('/misiones/solicitar/<int:id>', methods=['GET'])
async def request_mission(id):
    if 'id' in session:
        await missions.change_to_requested(id, int(session['id']))
        return redirect(url_for('minecraft.minecraftServer'))
    else:
        return redirect(url_for('login'))
