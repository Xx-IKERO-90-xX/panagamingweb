from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from extensions import db


class User(db.Model):
    __tablename__ = 'Usuario'

    id = db.Column(Integer, primary_key=True)
    email = db.Column(String(400), unique=True)
    username = db.Column(String(100), unique=True)
    passwd = db.Column(String(100))
    descripcion = db.Column(String(400))
    mc_name = db.Column(String(100))
    image = db.Column(String(100))
    role = db.Column(String(100))

    def __init__(self, email, username, passwd, descripcion, mc_name, image, role):
        self.email = email 
        self.username = username
        self.passwd = passwd
        self.descripcion = descripcion
        self.mc_name = mc_name
        self.image = image
        self.role = role