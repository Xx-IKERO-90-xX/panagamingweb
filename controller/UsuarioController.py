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
from controller.PersonajesController import *
from controller.database import *
from controller.DiscordServerController import *

import globals


sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

async def nuevoUsuario(idUser, passwd, descripcion):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        INSERT INTO USUARIO (idUser, passwd, descripcion)
        VALUES ('{idUser}', '{passwd}', '{descripcion}');                
    """)
    conexion.commit()
    cursor.execute(f"""
        INSERT INTO STYLE_USUARIO (idUser, main, banner)
        VALUES({idUser}, null, null);
    """)
    conexion.commit()
    conexion.close()

async def actualizarUsuario(idUser, descripcion, color):
    conexion = database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        UPDATE USUARIO
            SET descripcion = {descripcion},
                color = {color}
            WHERE idUser = {idUser};
    """)
    conexion.commit()
    conexion.close()

async def GetDiscordUser(idUser):
    listaUsuarios = await app.ListUsers()
    usuario = 'null'
    for user in listaUsuarios:
        if user.id == int(idUser):
            usuario = user
            break
    return usuario

async def HasCharacter(idUser):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM PERSONAJES;
    """)
    result = cursor.fetchall()
    resultados_json = await database.ConvertirJSON(result, cursor)
    tiene = False
    for personaje in resultados_json:
        if personaje['idUser'] == idUser:
            tiene = True
            break
    conexion.close()
    return tiene

async def ValidarUsuario(idUser):
    listaUsuarios = await app.ListUsers()
    valido = False
    for u in listaUsuarios:
        if idUser == u.id:
            valido = True
    return valido

async def comprobarSiTienePersonaje(idUser):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM PERSONAJES;
    """)
    result = cursor.fetchall()
    resultados_json = await database.ConvertirJSON(result, cursor)
    tiene = False
    for personaje in resultados_json:
        if personaje['idUser'] == idUser:
            tiene = True
            break
    conexion.close()
    return tiene

async def ComprobarUsuarioRepetido(idUser):
    conexion = await database.AbrirConexionSQL()
    repite = False
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM USUARIO;
    """)
    result = cursor.fetchall()
    resultados_json = await database.ConvertirJSON(result, cursor)
    for usuario in resultados_json:
        if str(usuario['idUser']) == idUser:
            repite = True
            break     
    conexion.close()
    return repite

async def ObtenerUsuario(idUser):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT USUARIO.descripcion AS descripcion, STYLE_USUARIO.main AS main, STYLE_USUARIO.banner
        FROM USUARIO INNER JOIN STYLE_USUARIO
            ON USUARIO.idUser = STYLE_USUARIO.idUser
        WHERE USUARIO.idUser = {idUser};
    """)
    result = cursor.fetchall()
    resultadoJson = await database.ConvertirJSON(result, cursor)
    conexion.close()
    print(resultadoJson)
    return resultadoJson[0]
