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
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM PERSONAJES;
    """)
    result = cursor.fetchall()
    resultados_json = await database.ConvertirJSON(result, cursor)
    conexion.close()
    return resultados_json

async def ObtenerPersonaje(name):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT PERSONAJES.id, PERSONAJES.name, PERSONAJES.descripcion, PERSONAJES.color, PERSONAJES.imgUrl, PERSONAJES.idUser, PERSONAJES.idDiario, USUARIO.name AS userNAme
        FROM PERSONAJES INNER JOIN USUARIO
            ON PERSONAJES.idUser = USUARIO.idUser
        WHERE USUARIO.name = '{name}';
    """)
    result = cursor.fetchall()
    resultados_json = await database.ConvertirJSON(result, cursor)
    conexion.close()
    return resultados_json

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

async def ObtenerPersonajePorIdUser(idUser):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT * FROM PERSONAJES
        WHERE PERSONAJES.idUser = {idUser};
    """)
    result = cursor.fetchall()
    resultados_json = await database.ConvertirJSON(result, cursor)
    conexion.close()
    return resultados_json

async def GetCharacterById(id):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT * FROM PERSONAJES
        WHERE PERSONAJES.id = {id};
    """)
    result = cursor.fetchall()
    resultados_json = await database.ConvertirJSON(result, cursor)
    conexion.close()
    return resultados_json[0]

async def NuevoPersonajePost(name, descripcion, color, imgUrl, idUser, raza, edad, sexo, tipo):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        INSERT INTO PERSONAJES (name, descripcion, color, imgUrl, idUser, raza, edad, sexo, tipo, reputacion)
        VALUES ('{name}', '{descripcion}', '{color}', '{imgUrl}', '{idUser}', '{raza}', '{edad}', '{sexo}', '{tipo}', 0);
    """)
    conexion.commit()
    conexion.close()
    

async def EditarPersonajePost(name, color, descripcion, imgUrl, idUser, raza, edad, sexo):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        UPDATE PERSONAJES
        SET name = '{name}', 
            color = '{color}', 
            descripcion = '{descripcion}', 
            imgUrl = '{imgUrl}', 
            raza = '{raza}', 
            edad = {edad}, 
            sexo = '{sexo}'
        WHERE idUser = '{idUser}';
    """)
    conexion.commit() 
    conexion.close()
    