import os 
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
import json
import random
import asyncio
import controller.SecurityController as security
from threading import Thread
from entity.User import *
from entity.UserStyle import *
import controller.StaticsController as statics


sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)
import app
from extensions import db

session = app.session
user_bp = Blueprint('usuario', __name__)
db = app.db

# User profile from session
@user_bp.route('/me', methods=['GET'])
async def my_profile():
    if 'id' in session:
        user = User.query.get(session['id'])
        user_style = db.session.query(UserStyle).filter(UserStyle.idUser == session['id']).first()
        
        result = {
            "avatar": session["image"],
            "name": user.username,
            "mc_name": user.mc_name,
            "descripcion": user.descripcion,
            "main": user_style.main,
            "banner": user_style.banner
        }

        return render_template(
            '/paginas/users/myProfile.jinja', 
            user=result, 
            session=session
        )
    
    else:
        return redirect(url_for("auth.login"))

# User profile page
@user_bp.route('/<int:id>', methods=['GET'])
async def UserProfile(id):
    if 'id' in session:
        user = User.query.get(id)
        user_style = db.session.query(UserStyle).filter(UserStyle.idUser == id).first()
        print('Userstyle: ', user_style)

        if user.id != session['id']:
            result = {
                "avatar": id,
                "avatar": user.image,
                "name": user.username,
                "mc_name": user.mc_name,
                "descripcion": user.descripcion,
                "main": user_style.main,
                "banner": user_style.banner
            }

            return render_template(
                '/paginas/users/profile.jinja', 
                user=result, 
                session=session
            )
        
        else:
            return redirect(url_for('usuario.my_profile'))
    else:
        return redirect(url_for('auth.login'))

# Edit user description
@user_bp.route('/usuario/me/description/edit', methods=["POST"])
async def edit_user_description():
    if 'id' in session:
        description = request.form['description']
        user = db.session.query(User).filter(User.id == session['id']).first()
        print(user)
        user.descripcion = description
        db.session.commit()
        
        return redirect(url_for('usuario.my_profile', id=session['id']))
    else:
        return redirect(url_for('auth.login'))

# Edit user style
@user_bp.route('/usuario/edit/style/<int:id>', methods=["GET"])
async def EditUserStyle(id):
    if 'id' in session:
        user = User.query.get(id)
        style_user = db.session.query(UserStyle).filter(UserStyle.idUser == id).first()
        
        result = {
            "avatar": user.image, 
            "name": user.username, 
            "mc_name": user.mc_name, 
            "descripcion": user.descripcion, 
            "main": style_user.main, 
            "banner": style_user.banner 
        }

        return render_template(
            '/paginas/users/styleProfile.jinja', 
            user=result, 
            session=session
        )
        
    else:
        return redirect(url_for("auth.login"))

# Set new main background style
@user_bp.route('/usuario/edit/style/newMainBk/<int:id>', methods=["POST"])
async def set_main_style(id):
    if 'id' in session:
        main_bk = request.form["mainBk"]

        user_style = db.session.query(UserStyle).filter(UserStyle.idUser == id).first()
        user_style.main = main_bk
        db.session.commit()

        return redirect(url_for('usuario.EditUserStyle', id=id))
    
    else:
        return redirect(url_for('auth.login'))

# Update user avatar
@user_bp.route('/usuario/edit/avatar/<int:id>', methods=["POST"])
async def update_avatar(id):
    if 'id' in session:
        user = db.session.query(User).filter(User.id == id).first()

        last_image = user.image
        image_filename = None
        new_image = request.files["new_avatar"]

        if new_image:
            image_filename = await statics.update_image(new_image, last_image)
            user.image = image_filename
            db.session.commit()

            session['image'] = image_filename
        
        return redirect(url_for('usuario.my_profile'))
    
    else:
        return redirect(url_for('auth.login'))
