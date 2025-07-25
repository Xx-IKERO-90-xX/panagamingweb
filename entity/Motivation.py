from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from extensions import db

class Motivation(db.Model):
    __tablename__ = "Motivation"
    
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    id_character = db.Column(Numeric)
    motivation_text = db.Column(String(500))

    def __init__(self, id_character, motivation_text):
        self.id_character = id_character
        self.motivation_text = motivation_text