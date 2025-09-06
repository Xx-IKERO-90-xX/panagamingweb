from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from extensions import db

class Friendship(db.Model):
    __tablename__ = 'Friendship'

    id = db.Column(Integer, primary_key=True)
    id_user1 = db.Column(Integer, ForeignKey('Usuario.id'), nullable=False)
    id_user2 = db.Column(Integer, ForeignKey('Usuario.id'), nullable=False)
    status = db.Column(String(50), nullable=False)  # e.g., 'pending', 'accepted', 'declined'
    last_message_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, id_user1, id_user2, status, last_message_date):
        self.id_user1 = id_user1
        self.id_user2 = id_user2
        self.status = status
        self.last_message_date = last_message_date