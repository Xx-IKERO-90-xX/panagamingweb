import os 
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for
import mysql.connector
import json
import random
import asyncio
from Personajes import *
from database import *
from app import *

async def ObtenerListaPersonajes():
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM PERSONAJES;
    """)
    result = cursor.fetchall()
    resultados_json = await ConvertirJSON(result, cursor)
    conexion.close()
    return resultados_json

async def ObtenerPersonaje(name):
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT PERSONAJES.id, PERSONAJES.name, PERSONAJES.descripcion, PERSONAJES.color, PERSONAJES.imgUrl, PERSONAJES.idUser, PERSONAJES.idDiario, USUARIO.name AS userNAme
        FROM PERSONAJES INNER JOIN USUARIO
            ON PERSONAJES.idUser = USUARIO.idUser
        WHERE USUARIO.name = '{name}';
    """)
    result = cursor.fetchall()
    resultados_json = await ConvertirJSON(result, cursor)
    conexion.close()
    return resultados_json

async def ValidarPersonajeUsuario(idUser, name):
    listaPersonajes = await ObtenerListaPersonajes()
    codError = 0
    for personaje in listaPersonajes:
        if personaje["idUser"] == idUser:        
            codError = 1
        elif personaje["name"] == name:
            codError = 2
    return codError

async def ValidarPersonajeEditado(idUser, name):
    listaPersonajes = await ObtenerListaPersonajes()
    errorCod = 0
    for personaje in listaPersonajes:
        if personaje["name"] == name and personaje["idUser"] != idUser:
            errorCod = 1
    return errorCod

async def ObtenerPersonajePorIdUser(idUser):
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT * FROM PERSONAJES
        WHERE PERSONAJES.idUser = '{idUser}';
    """)
    result = cursor.fetchall()
    resultados_json = await ConvertirJSON(result, cursor)
    conexion.close()
    return resultados_json
    

async def ObtenerPaginas():
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM DIARIO;")
    result = cursor.fetchall()
    resultados_json = await ConvertirJSON(result, cursor)
    cursor.close()
    return resultados_json

async def ObtenerPersonajePorId(id):
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
       SELECT * FROM PERSONAJES
        WHERE PERSONAJES.id = {id}; 
    """)
    result = cursor.fetchall()
    resultado_json = await ConvertirJSON(result, cursor)
    return resultado_json