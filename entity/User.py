from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from extensions import db


class User(db.Model):
    __tablename__ = 'Usuario'

    id = db.Column(Integer, primary_key=True)

    username = db.Column(String(100), unique=True)
    passwd = db.Column(String(100))
    descripcion = db.Column(String(300))
    mc_name = db.Column(String(100))


    def __init__(self, idUser, username, passwd, descripcion, mc_name):
        self.idUser = idUser
        self.username = username
        self.passwd = passwd
        self.descripcion = descripcion
        self.mc_name = mc_name