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
import controller.database as database
import controller.UsuarioController as usuario

import globals

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app


async def MostrarSectoresPerdidosAction():
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT * FROM SECTORES_PERDIDOS;')
    result = cursor.fetchall()
    result_json = await database.ConvertirJSON(result, cursor)
    conexion.close()
    
    return result_json

async def GetSectorPerdido(id):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    
    cursor.execute(f"""
        SELECT * FROM SECTORES_PERDIDOS
        WHERE id = {id};                       
    """);
    result = cursor.fetchall()
    result_json = await database.ConvertirJSON(result, cursor)
    conexion.close()
    
    return result_json[0]

async def CrearSectorPerdidoAction(descripcion, planeta, imagen_name, activo, cord_x, cord_y, cord_z):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    
    if imagen_name:
        cursor.execute(f"""
            INSERT INTO SECTORES_PERDIDOS (descripcion, planeta, imagen, activo, cord_x, cord_y, cord_z)
            VALUES('{descripcion}', '{planeta}', '{imagen_name}', '{activo}', {cord_x}, {cord_y}, {cord_z});               
        """)
    else:
        cursor.execute(f"""
            INSERT INTO SECTORES_PERDIDOS (descripcion, planeta, activo, cord_x, cord_y, cord_z)
            VALUES('{descripcion}', '{planeta}', '{activo}', {cord_x}, {cord_y}, {cord_z});               
        """)
    conexion.commit()
    conexion.close()

async def EditarSectorPerdidoAction(id, descripcion, planeta, imagen_name, activo, cord_x, cord_y, cord_z):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    
    if imagen_name:
        cursor.execute(f"""
            UPDATE SECTORES_PERDIDOS
                SET descripcion = '{descripcion}',
                    planeta = '{planeta}',
                    imagen = '{imagen_name}',
                    activo = '{activo}',
                    cord_x = '{cord_x}',
                    cord_y = '{cord_y}',
                    cord_z = '{cord_z}'
            WHERE id = {id};            
        """)
    else:
        cursor.execute(f"""
            UPDATE SECTORES_PERDIDOS
                SET descripcion = '{descripcion}',
                    planeta = '{planeta}',
                    activo = '{activo}',
                    cord_x = '{cord_x}',
                    cord_y = '{cord_y}',
                    cord_z = '{cord_z}'
            WHERE id = {id};            
        """)
    
    conexion.commit()
    conexion.close()

async def DeleteSectorPerdidoAction(id):
    conexion = await database.AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        DELETE FROM SECTORES_PERDIDOS
        WHERE id = {id};                                  
    """)    
    conexion.commit()
    conexion.close()
