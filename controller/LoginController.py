import os 
import discord
import sys
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for
import mysql.connector
import json
import random
import asyncio
import controller.PersonajesController as personaje
import controller.DiscordServerController as DiscordServer
import controller.database as database

import globals

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

async def ValidarInicioSesion(passwd):
    conexion = await database.AbrirConexionSQL()
    valido = False
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM USUARIO;
    """)
    result = cursor.fetchall()
    resultados_json = await database.ConvertirJSON(result, cursor)
    for usuario in resultados_json:
        if usuario['passwd'] == passwd:
            valido = True
            break
    conexion.close()
    return valido