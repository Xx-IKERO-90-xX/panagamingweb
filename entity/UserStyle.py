from extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base


class UserStyle(db.Model):
    __tablename__ = 'UserStyle'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    idUser = db.Column(BigInteger, ForeignKey('Usuario.id'))
    main = db.Column(String(100))
    banner = db.Column(String(100))

    def __init__(self, idUser, main, banner):
        self.idUser = idUser
        self.main = main
        self.banner = banner