from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from extensions import db

class Character(db.Model):
    __tablename__ = "Character"

    id = db.Column(Integer, primary_key=True)
    idUser = db.Column(BigInteger, ForeignKey("Usuario.id"))
    name = db.Column(String(100), unique=True)
    gender = db.Column(String(30))
    specie = db.Column(String(50))
    image = db.Column(String(100))
    description = db.Column(String(400))
    character_level = db.Column(Numeric)

    def __init__(self, idUser, name, gender, specie, image, description, character_level):
        self.idUser = idUser
        self.name = name
        self.gender = gender
        self.specie = specie
        self.image = image
        self.description = description
        self.character_level = character_level