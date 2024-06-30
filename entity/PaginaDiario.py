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

class PaginaDiario:
    def __init__(self, idPagina, idPersonaje, contenido):
        self.idPagina = idPagina
        self.idPersonaje = idPersonaje
        self.contenido = contenido