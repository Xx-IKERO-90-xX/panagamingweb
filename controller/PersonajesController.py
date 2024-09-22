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
import controller.database as database
import controller.UsuarioController as usuario
from globals import guild

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

async def GetCharacterList():
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM PERSONAJES;
    """)
    result = cursor.fetchall()
    json_result = await database.covert_to_json(result, cursor)
    connection.close()
    return json_result

async def ValidarPersonajeUsuario(idUser, name):
    listaPersonajes = await GetCharacterList()
    codError = 0
    for personaje in listaPersonajes:
        if personaje["idUser"] == idUser:        
            codError = 1
        elif personaje["name"] == name:
            codError = 2
    return codError

async def ValidarPersonajeEditado(idUser, name):
    listaPersonajes = await GetCharacterList()
    errorCod = 0
    for personaje in listaPersonajes:
        if personaje["name"] == name and personaje["idUser"] != idUser:
            errorCod = 1
    return errorCod

async def get_character_by_id_user(idUser):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT * FROM PERSONAJES
        WHERE PERSONAJES.idUser = {idUser};
    """)
    result = cursor.fetchall()
    json_result = await database.covert_to_json(result, cursor)
    connection.close()
    return json_result[0]

async def GetCharacterById(id):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT * FROM PERSONAJES
        WHERE PERSONAJES.id = {id};
    """)
    result = cursor.fetchall()
    json_result = await database.covert_to_json(result, cursor)
    connection.close()
    return json_result[0]

async def new_character(name, descripcion, color, imgUrl, idUser, raza, edad, sexo, tipo):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        INSERT INTO PERSONAJES (name, descripcion, color, imgUrl, idUser, raza, edad, sexo, tipo, reputacion)
        VALUES ('{name}', '{descripcion}', '{color}', '{imgUrl}', '{idUser}', '{raza}', '{edad}', '{sexo}', '{tipo}', 0);
    """)
    connection.commit()
    connection.close()
    

async def edit_character(name, color, descripcion, imagen, idUser, raza, edad):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        UPDATE PERSONAJES
        SET name = '{name}', 
            color = '{color}', 
            descripcion = '{descripcion}', 
            imgUrl = '{imagen}', 
            raza = '{raza}', 
            edad = {edad}
        WHERE idUser = '{idUser}';
    """)
    connection.commit() 
    connection.close()
    