import os 
import sys
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, current_app, redirect, session, sessions, url_for, Blueprint
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
import controller.SecurityController as security
import controller.StaticsController as statics
from threading import Thread
from entity.User import *
from entity.Character import *
from entity.DiaryPage import *
from controller.CharacterController import *
from entity.Characteristic import *
from entity.Motivation import *

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
        page = request.args.get('page', 1, type=int)
        characters = db.session.query(Character).paginate(page=page, per_page=6)

        if not await user_has_character(session['id']):
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
            
            if not name or not specie or not gender or not description:
                return redirect(url_for('characters.create'))
            
            if await character_name_in_use(name):
                error_msg = "El nombre del personaje ya esta en uso."
                return render_template(
                    '/paginas/minecraft_subpg/characters/nocharacter/create.jinja', 
                    session=session, 
                    error_msg=error_msg
                )
            
            if len(description) > 400:
                error_msg = "La descripcion del personaje no puede tener mas de 400 caracteres."
                return render_template(
                    '/paginas/minecraft_subpg/characters/nocharacter/create.jinja', 
                    session=session, 
                    error_msg=error_msg
                )
            
            if len(name) > 100 or len(gender) > 30 or len(specie) > 50:
                error_msg = "El nombre, el sexo o la especie del personaje no pueden tener mas de 100, 30 o 50 caracteres respectivamente."
                return render_template(
                    '/paginas/minecraft_subpg/characters/nocharacter/create.jinja', 
                    session=session, 
                    error_msg=error_msg
                )
            
            image_filename = None
            
            try:
                imagen = request.files["image"]
                image_filename = statics.upload_image(imagen)
            except:
                pass
                        
            new_character = Character(session['id'], name, gender, specie, image_filename, description, 0)
            db.session.add(new_character)
            db.session.commit()

            new_diary = DiaryPage(new_character.id, f'Diario de {new_character.name}')
            db.session.add(new_diary)
            db.session.commit()

            return redirect(url_for('characters.index'))
    else:
        return redirect(url_for('auth.login'))


@characters_bp.route('/my', methods=['GET'])
async def my_character():
    if 'id' in session:
        character = db.session.query(Character).filter(Character.idUser == session['id']).first()
        characteristics = db.session.query(Characteristic).filter(Characteristic.id_character == character.id).all()
        motivations = db.session.query(Motivation).filter(Motivation.id_character == character.id).all()

        if character:
            return render_template(
                '/paginas/minecraft_subpg/characters/withcharacter/my_character.jinja',
                character=character,
                characteristics=characteristics,
                motivations=motivations,
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



@characters_bp.route('/edit/image/<int:id>', methods=['POST'])
async def update_character_image(id):
    if 'id' in session:
        character = db.session.query(Character).filter(Character.id == id).first()
        
        last_image = character.image
        image_filename = None

        new_imagen = request.files["update_image"]
        
        if new_imagen:
            image_filename = await statics.update_image(new_imagen, last_image)
            character.image = image_filename
            db.session.commit()

        return redirect(url_for('characters.my_character'))
    else:
        return redirect(url_for('auth.login'))


@characters_bp.route('/<int:id>', methods=['GET'])
async def details_character(id):
    if 'id' in session:
        character = db.session.query(Character).filter(Character.id == id).first()
        motivations = db.session.query(Motivation).filter(Motivation.id_character == character.id).all()
        characteristics = db.session.query(Characteristic).filter(Characteristic.id_character == character.id).all()

        if character:
            return render_template(
                '/paginas/minecraft_subpg/characters/withcharacter/details.jinja',
                character=character,
                motivations=motivations,
                characteristics=characteristics,
                session=session
            )
        else:
            return redirect(url_for('characters.index'))
    else:
        return redirect(url_for('auth.login'))


@characters_bp.route('/my/diary', methods=["GET"])
async def my_diary():
    if 'id' in session:
        character = db.session.query(Character).filter(
            Character.idUser == session['id']
        ).first()
        
        page = request.args.get('page', 1, type=int)
        
        pagination = db.session.query(DiaryPage).filter(
            DiaryPage.id_character == character.id
        ).paginate(page=page, per_page=1)

        return render_template(
            '/paginas/minecraft_subpg/characters/withcharacter/my_diary.jinja',
            pagination=pagination,
            character=character,
            session=session
        )
    else:
        return redirect(url_for('auth.login'))

@characters_bp.route('/<int:id>/diary', methods=["GET"])
async def character_diary(id):
    if 'id' in session:
        character = db.session.query(Character).filter(
            Character.id == id
        ).first()
        
        page = request.args.get('page', 1, type=int)
        
        pagination = db.session.query(DiaryPage).filter(
            DiaryPage.id_character == character.id
        ).paginate(page=page, per_page=1)

        return render_template(
            '/paginas/minecraft_subpg/characters/withcharacter/diary.jinja',
            pagination=pagination,
            character=character,
            session=session
        )
    else:
        return redirect(url_for('auth.login'))



@characters_bp.route('/my/diary/newpage', methods=['POST'])
async def new_diary_page():
    if 'id' in session:
        text = request.form['text']

        character = db.session.query(Character).filter(
            Character.idUser == session['id']
        ).first()

        new_page = DiaryPage(character.id, text)
        db.session.add(new_page)
        db.session.commit()

        pages = db.session.query(DiaryPage).filter(
            DiaryPage.id_character == character.id
        ).all()

        last_page = len(pages)

        return redirect(url_for('characters.my_diary', page=last_page))
    
    else:
        return redirect(url_for('auth.login'))

@characters_bp.route('/my/diary/edit/<int:id>', methods=['POST'])
async def edit_diary_page(id):
    if 'id' in session:
        text = request.form['text']
        current_page = request.form['current_page']

        if not text or not id:
            return redirect(url_for('characters.my_diary', page=current_page))

        page = db.session.query(DiaryPage).filter(
            DiaryPage.id == id
        ).first()

        page.text = text
        db.session.commit()

        return redirect(url_for('characters.my_diary', page=current_page))
    else:
        return redirect(url_for('auth.login'))

@characters_bp.route('/my/diary/delete/<int:id>', methods=['GET'])
async def delete_diary_page(id):
    if 'id' in session:
        page = db.session.query(DiaryPage).filter(
            DiaryPage.id == id
        ).first()

        db.session.delete(page)
        db.session.commit()

        return redirect(url_for('characters.my_diary', page=1))
    else:
        return redirect(url_for)


'''
Rasgos y Motivaciones de los personajes.
'''
@characters_bp.route('/characteristic/add/<int:id>', methods=['POST'])
async def add_characteristic(id):
    if 'id' in session:
        rasgo = request.form['rasgo']

        if not rasgo or not id:
            return redirect(url_for('characters.my_character'))

        new_characteristic = Characteristic(id, rasgo)
        db.session.add(new_characteristic)
        db.session.commit()

        return redirect(url_for('characters.my_character'))
    else:
        return redirect(url_for('auth.login'))

@characters_bp.route('/motivation/add/<int:id>', methods=['POST'])
async def add_motivation(id):
    if 'id' in session:
        motivation_text = request.form['motivation']

        if not motivation_text or not id:
            return redirect(url_for('characters.my_character'))

        new_motivation = Motivation(id, motivation_text)
        db.session.add(new_motivation)
        db.session.commit()

        return redirect(url_for('characters.my_character'))
    else:
        return redirect(url_for('auth.login'))

@characters_bp.route('/motivation/edit/<int:id>', methods=['POST'])
async def edit_motivation(id):
    if 'id' in session:
        motivation_text = request.form['motivation']

        if not motivation_text or not id:
            return redirect(url_for('characters.my_character'))

        motivation = db.session.query(Motivation).filter(
            Motivation.id == id
        ).first()

        motivation.motivation_text = motivation_text
        db.session.commit()

        return redirect(url_for('characters.my_character'))
    else:
        return redirect(url_for('auth.login'))

@characters_bp.route('motivation/delete/<int:id>', methods=['GET'])
async def delete_motivation(id):
    if 'id' in session:
        motivation = db.session.query(Motivation).filter(
            Motivation.id == id
        ).first()

        db.session.delete(motivation)
        db.session.commit()

        return redirect(url_for('characters.my_character'))
    else:
        return redirect(url_for('auth.login'))