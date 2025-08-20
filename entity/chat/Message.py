from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from extensions import db

class Message(db.Model):
    __tablename__ = 'Message'

    id = db.Column(Integer, primary_key=True)
    content = db.Column(String(500), nullable=False)
    sender_id = db.Column(Integer, ForeignKey('User.id'), nullable=False)
    room_id = db.Column(Integer, ForeignKey('PrivateRoom.id'), nullable=False)
    timestamp = db.Column(BigInteger, nullable=False)

    def __init__(self, content, sender_id, room_id):
        self.content = content
        self.sender_id = sender_id
        self.room_id = room_id