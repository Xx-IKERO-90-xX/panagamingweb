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
import controller.PersonajesController as characters
from controller.database import *
from controller.DiscordServerController import *

import globals


sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

async def get_all_users():
    connection = await database.open_database_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM USUARIO;")    
    result = cursor.fetchall()

    json_result = await database.covert_to_json(result, cursor)
    connection.close()

    return json_result

async def new_user(idUser, username, passwd, descripcion):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        INSERT INTO USUARIO (idUser, passwd, descripcion, username)
        VALUES ('{idUser}', '{passwd}', '{descripcion}', '{username}');                
    """)
    connection.commit()
    cursor.execute(f"""
        INSERT INTO STYLE_USUARIO (idUser, main, banner)
        VALUES({idUser}, null, null);
    """)
    connection.commit()
    connection.close()

async def actualizarUsuario(idUser, descripcion, color):
    connection = database.open_database_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        UPDATE USUARIO
            SET descripcion = {descripcion},
                color = {color}
            WHERE idUser = {idUser};
    """)
    connection.commit()
    connection.close()

async def GetDiscordUser(idUser):
    listaUsuarios = await app.get_discord_users()
    usuario = 'null'
    for user in listaUsuarios:
        if user.id == int(idUser):
            usuario = user
            break
        
    return usuario

async def HasCharacter(idUser):
    characters_list = await characters.get_all_characters()
    has_character = False
    for personaje in characters_list:
        if personaje['idUser'] == idUser:
            has_character = True
            break

    return has_character

async def ValidarUsuario(idUser):
    listaUsuarios = await app.ListUsers()
    valido = False
    for u in listaUsuarios:
        if idUser == u.id:
            valido = True
    return valido

async def comprobarSiTienePersonaje(idUser):
    has_character = False
    character_list = await characters.GetCharacterList()
    for character in character_list:
        if character['idUser'] == idUser:
            has_character = True
            break

    return has_character

async def ComprobarUsuarioRepetido(idUser):
    repeate = False
    users = await get_all_users()
    for user in users:
        if str(user['idUser']) == idUser:
            repeate = True
            break
             
    return repeate

async def get_user_by_id(idUser):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT USUARIO.descripcion AS descripcion, STYLE_USUARIO.main AS main, STYLE_USUARIO.banner
        FROM USUARIO INNER JOIN STYLE_USUARIO
            ON USUARIO.idUser = STYLE_USUARIO.idUser
        WHERE USUARIO.idUser = {idUser};
    """)
    result = cursor.fetchall()
    
    resultadoJson = await database.covert_to_json(result, cursor)
    connection.close()
    
    return resultadoJson[0]


async def get_user_by_username(username):
    connection = await database.open_database_connection()
    cursor = connection.cursor()

    cursor.execute(f"""
        SELECT * FROM USUARIO
        WHERE username = '{username}';
    """)

    result = cursor.fetchall()
    result_json = await database.covert_to_json(result, cursor)

    connection.close()
    return result_json[0]

