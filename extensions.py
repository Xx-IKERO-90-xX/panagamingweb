from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from pymongo import MongoClient
import json

db = SQLAlchemy()
socketio = SocketIO()

with open('settings.json') as archivo:
    datos = json.load(archivo)

client = MongoClient(f"mongodb://{datos['database']['mongodb']['user']}:{datos['database']['mongodb']['passwd']}@{datos['database']['mongodb']['host']}:{datos['database']['mongodb']['port']}/")
mongodb = client[datos['database']['mongodb']['db']]