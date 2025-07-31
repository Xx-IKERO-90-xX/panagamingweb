from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from extensions import db

class Characteristic(db.Model):
    __tablename__ = "Characteristic"
    
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    id_character = db.Column(Numeric)
    rasgo = db.Column(String(100))

    def __init__(self, id_character, rasgo):
        self.id_character = id_character
        self.rasgo = rasgo