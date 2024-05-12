import os 
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for
import mysql.connector
import json
import random
import asyncio
from app import *

async def AbrirConexionSQL():
    conection = mysql.connector.connect(
        host = datos["database"]["host"],
        user = datos["database"]["user"],
        password = datos["database"]["passwd"],
        database = datos["database"]["db"],
        auth_plugin = datos["database"]["auth_plugin"]
    )
    return conection

async def ConvertirJSON(result, cursor):
    columnas = [column[0] for column in cursor.description]
    resultados_json = []
    for fila in result:
        fila_json = dict(zip(columnas, fila))
        resultados_json.append(fila_json)
    return resultados_json