from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from extensions import db

class PrivateRoom(db.Model):
    __tablename__ = 'PrivateRoom'

    id = db.Column(Integer, primary_key=True)
    user_1 = db.Column(Integer, ForeignKey('User.id'), nullable=False)
    user_2 = db.Column(Integer, ForeignKey('User.id'), nullable=False)
    name = db.Column(String(100), unique=True)

    def __init__(self, user_1, user_2, name):
        self.user_1 = user_1
        self.user_2 = user_2
        self.name = name
