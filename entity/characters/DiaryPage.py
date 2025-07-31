from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from extensions import db


class DiaryPage(db.Model):
    __tablename__ = "DiaryPage"

    id = db.Column(Integer, primary_key=True)
    id_character = db.Column(Numeric)
    text = db.Column(String(1000))

    def __init__(self, id_character, text):
        self.id_character = id_character
        self.text = text