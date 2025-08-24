import os 
from flask import request, Flask, render_template, redirect, session, sessions, url_for
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
import json
import random
import asyncio
import multiprocessing
import controller.SecurityController as security
import controller.McServersController as mcservers
from threading import Thread
from mcrcon import MCRcon
from extensions import db, socketio, mongodb
from pymongo import MongoClient

datos = {}
with open('settings.json') as archivo:
    datos = json.load(archivo)


app = Flask(__name__)
app.secret_key = "a40ecfce592fd63c8fa2cda27d19e1dbc531e946"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{datos['database']['mysql']['user']}:{datos['database']['mysql']['passwd']}@{datos['database']['mysql']['host']}/{datos['database']['mysql']['db']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
socketio = SocketIO(app)

from routes import auth_bp, minecraft_bp, user_bp, index_bp, characters_bp, chat_bp

app.register_blueprint(chat_bp, url_prefix="/chat")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(minecraft_bp, url_prefix="/minecraft")
app.register_blueprint(user_bp, url_prefix="/usuarios")
app.register_blueprint(characters_bp, url_prefix="/minecraft/characters")
app.register_blueprint(index_bp)

app.app_context()


# Maneja los mensajes enviados desde el chat publico de la pagina del servidor de Minecraft
@socketio.on('send_message')
def handle_public_chat_message(data):
    app.logger.info(f"Message: {data['message']} from {data['username']}")
    data['id'] = f"/usuarios/{data['id']}"
    emit('receive_message', data, broadcast=True)


#Terminal de los servidores de minecraft
@socketio.on('send_vanilla_command')
def handle_send_command(cmd):  
    result_queue = multiprocessing.Queue()

    process = multiprocessing.Process(
        target=mcservers.execute_mc_command, 
        args=(cmd['command'], result_queue)
    )
    
    process.start()
    process.join()

    response = result_queue.get()

    emit('server_output', {'output': response})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    socketio.run(
        app, 
        port=datos["flask"]["port"], 
        host=datos["flask"]["host"], 
        debug=True,
    )
