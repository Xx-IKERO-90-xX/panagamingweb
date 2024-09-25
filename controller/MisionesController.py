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


async def get_all_missions():
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM MISIONES;")
    result = cursor.fetchall()
    
    resultado_json = await database.covert_to_json(result, cursor)
    connection.close()
    
    return resultado_json

async def get_mission_by_id(id):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    
    cursor.execute(f"""
        SELECT * FROM MISIONES
        WHERE id = {id};           
    """)
    
    result = cursor.fetchall()
    connection.close()
    resultado_json = await database.covert_to_json(result, cursor)
    
    return resultado_json[0]


async def create_mission(descripcion, tipo, imagen_name, dificultad, estado, grupo, guerrero, aventurero, hechicero):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    
    cursor.execute(f"""
        INSERT INTO MISIONES (descripcion, tipo, imagen, dificultad, num_personas, estado, guerrero, aventurero, hechicero)
        VALUES('{descripcion}', '{tipo}', '{imagen_name}', '{dificultad}', '{grupo}', '{estado}', '{guerrero}', '{aventurero}', '{hechicero}');               
    """)
    
    connection.commit()
    connection.close()

async def update_mission(id, descripcion, tipo, imagen_name, dificultad, estado, grupo, guerrero, aventurero, hechicero):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    
    if imagen_name != None:
        cursor.execute(f"""
            UPDATE MISIONES
            SET descripcion = '{descripcion}',
                tipo = '{tipo}',
                imagen = '{imagen_name}',
                dificultad = '{dificultad}',
                estado = '{estado}',
                num_personas = '{grupo}',
                guerrero = '{guerrero}',
                aventurero = '{aventurero}',
                hechicero = '{hechicero}'
            WHERE id = {id};       
        """)
    else:
        cursor.execute(f"""
            UPDATE MISIONES
            SET descripcion = '{descripcion}',
                tipo = '{tipo}',
                dificultad = '{dificultad}',
                estado = '{estado}',
                num_personas = '{grupo}',
                guerrero = '{guerrero}',
                aventurero = '{aventurero}',
                hechicero = '{hechicero}'
            WHERE id = {id};       
        """)
    
    connection.commit()
    connection.close()

async def delete_mission(id):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    
    cursor.execute(f"""
        DELETE FROM MISIONES
        WHERE id = {id};               
    """)
    
    connection.commit()
    connection.close()

async def change_to_requested(id, idUser):
    connection = await database.open_database_connection()
    cursor = connection.cursor()
    
    cursor.execute(f"""
        UPDATE MISIONES
            SET estado = 'Solicitado',
                idUserSolicitante = '{idUser}'               
        WHERE id = '{id}';
    """)
    
    connection.commit()
    connection.close()

        
        