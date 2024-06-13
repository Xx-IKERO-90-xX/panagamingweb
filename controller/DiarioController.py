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
import controller.PersonajesController as personaje
import controller.database as database
import controller.UsuarioController as usuario
import globals


sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

async def ObtenerPaginas():
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM DIARIO;")
    result = cursor.fetchall()
    resultados_json = await database.ConvertirJSON(result, cursor)
    cursor.close()
    return resultados_json

async def UpdateDiarioPageAction(idPagina, contenido):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        UPDATE DIARIO
            SET contenido = '{contenido}'
        WHERE idPagina = {idPagina};
    """)
    conexion.commit()
    conexion.close()

async def ShowDiarioPages(idPersonaje):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT * FROM DIARIO
        WHERE idPersonaje = {idPersonaje};
    """)
    result = cursor.fetchall()
    paginas = await database.ConvertirJSON(result, cursor)    
    conexion.close()
    return paginas
    
async def NewPageAction(idPersonaje):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        INSERT INTO DIARIO (idPersonaje, contenido)
        VALUES ({idPersonaje}, null);           
    """)
    conexion.commit()
    conexion.close()

async def DeletePageAction(idPage):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        DELETE FROM DIARIO
        WHERE idPagina = {idPage};               
    """)
    conexion.commit()
    conexion.close()
