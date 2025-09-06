import os 
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
import controller.SecurityController as security
from threading import Thread
from entity.User import *
from entity.UserStyle import *

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app
from extensions import db

session = app.session
auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/logout")
async def logout():
    session.clear()
    return redirect(url_for("index.index"))


@auth_bp.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == "GET":
        return render_template("login.jinja")
    else:
        username = request.form["username"]
        passwd = request.form["passwd"]
        
        valid = await security.validate_login(username, passwd)
    
        if valid:
            user = db.session.query(User).filter(User.username == username).first()

            session["id"] = user.id
            session["name"] = user.username
            session["image"] = user.image
            session['role'] = user.role
    
            return redirect(url_for('index.index'))

        else:
            errorMsg = "Hay datos erroneos en el formulario, revisalos bien."
            return render_template("login.jinja", errorMsg=errorMsg)

@auth_bp.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == "GET":
        return render_template("registrar.jinja")
    
    else:
        email = request.form['email']
        username = request.form['username']
        passwd = request.form['passwd']
        descripcion = request.form['descripcion']
        
        passwd_encripted = await security.encrypt_passwd(passwd)

        new_user = User(email, username, passwd_encripted, descripcion, None, None, 'Usuario')
        db.session.add(new_user)
        db.session.commit()

        new_style_user = UserStyle(new_user.id, None, None)
        db.session.add(new_style_user)
        db.session.commit()

        session["id"] = new_user.id
        session["name"] = new_user.username
        session["image"] = new_user.image
        session['role'] = new_user.role
                
        return redirect(url_for("index.index"))