import os 
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for
import mysql.connector
import json
import random
import asyncio
from controller.PersonajesController import *
from controller.database import *
from controller.UsuarioController import *

class Personaje:
    def __init__(self, id, name, descripcion, color, imgUrl, idUser, raza, edad, sexo):
        self.id = id
        self.name = name
        self.descripcion = descripcion
        self.color = color
        self.imgUrl = imgUrl
        self.idUser = idUser 
        self.raza = raza
        self.edad = edad
        self.sexo = sexo