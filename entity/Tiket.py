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

class Ticket:
    def __init__(self, id, texto, idUser):
        self.id = id
        self.texto = texto
        self.idUser = idUser