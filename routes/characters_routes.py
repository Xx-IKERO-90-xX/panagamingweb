import os 
import sys
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
import controller.DiscordServerController as discord_server
import controller.SecurityController as security
from threading import Thread
from entity.User import *
from entity.Character import *
from controller.StaticsController import *

import globals
sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app
from extensions import db

session = app.session

characters_bp = Blueprint('characters', __name__)


async def user_has_character(idUser):
    character = db.session.query(Character).filter(Character.idUser == idUser).first()

    if character != None:
        return True
    else:
        return False


@characters_bp.route('/', methods=["GET"])
async def index():
    if 'id' in session:
        characters = Character.query.all()

        if not user_has_character(session['id']):
            return render_template(
                '/paginas/minecraft_subpg/characters/nocharacter/index.jinja',
                characters=characters, 
                session=session
            )
        
        else:
            return render_template(
                '/paginas/minecraft_subpg/characters/withcharacter/index.jinja',
                characters=characters, 
                session=session
            )
    else:
        return redirect(url_for('auth.login'))

@characters_bp.route('/new', methods=["GET", "POST"])
async def create():
    if 'id' in session:
        if request.method == "GET":
            return render_template(
                '/paginas/minecraft_subpg/characters/nocharacter/create.jinja',
                session=session
            )     
        else:
            name = request.form['nombre']
            specie = request.form['especie']
            gender = request.form['sexo']
            description = request.form["descripcion"]

            image_filename = None
            
            if "file" in request.files:
                imagen = request.file["image"]
                image_filename = secure_filename(imagen.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                imagen.save(filepath)
            
            new_character = Character(session['id'], name, gender, specie, image_filename, description, 0)
            db.session.add(new_character)
            db.session.commit()

            return redirect(url_for('characters.index'))
    else:
        return redirect(url_for('auth.login'))


@characters_bp.route('/my', methods=['GET'])
async def my_character():
    if 'id' in session:
        character = db.session.query(Character).filter(Character.idUser == session['id']).first()
        
        if character:
            return render_template(
                '/paginas/minecraft_subpg/characters/withcharacter/my_character.jinja',
                character=character,
                session=session
            )
        else:
            return redirect(url_for('characters.index')) 
    else:
        return redirect(url_for('auth.login'))

@characters_bp.route('/edit/description/<int:id>', methods=['POST'])
async def edit_character_description(id):
    if 'id' in session:
        character = db.session.query(Character).filter(Character.id == id).first()

        if character:
            description = request.form['descripcion']
            character.description = description
            db.session.commit()

            return redirect(url_for('characters.my_character'))
        else:
            return redirect(url_for('characters.indexs'))
    
    else:
        return redirect(url_for('auth.login'))

