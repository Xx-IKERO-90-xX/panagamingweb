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

# Get all pages from all characters diary.
async def get_pages():
    connection = await database.open_database_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM DIARIO;")
    result = cursor.fetchall()

    resultados_json = await database.covert_to_json(result, cursor)
    
    connection.close()
    return resultados_json



# Update a diary page.
async def update_diario_page(idPagina, contenido):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        UPDATE DIARIO
            SET contenido = '{contenido}'
        WHERE idPagina = {idPagina};
    """)
    connection.commit()
    connection.close()


#
async def get_character_diario_pages(idPersonaje):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT * FROM DIARIO
        WHERE idPersonaje = {idPersonaje};
    """)
    result = cursor.fetchall()
    result_json = await database.covert_to_json(result, cursor)  
    connection.close()
    return result_json

#
async def create_page(idPersonaje):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        INSERT INTO DIARIO (idPersonaje, contenido)
        VALUES ({idPersonaje}, "");           
    """)
    connection.commit()
    connection.close()

#
async def delete_page(idPage):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        DELETE FROM DIARIO
        WHERE idPagina = {idPage};               
    """)
    connection.commit()
    connection.close()
