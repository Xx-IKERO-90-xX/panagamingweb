import os 
import sys
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for
import mysql.connector
import json
import random
import asyncio
from globals import guild


sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)
import app

async def AbrirConexionSQL():
    conection = mysql.connector.connect(
        host = app.datos["database"]["host"],
        user = app.datos["database"]["user"],
        password = app.datos["database"]["passwd"],
        database = app.datos["database"]["db"],
        auth_plugin = app.datos["database"]["auth_plugin"]
    )
    return conection

async def ConvertirJSON(result, cursor):
    columnas = [column[0] for column in cursor.description]
    resultados_json = []
    for fila in result:
        fila_json = dict(zip(columnas, fila))
        resultados_json.append(fila_json)
    return resultados_json