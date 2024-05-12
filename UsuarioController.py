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
from Personajes import *
from database import *

async def nuevoUsuario(idUser, passwd, descripcion, color):
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        INSERT INTO USUARIO (idUser, passwd, descripcion, color)
        VALUES ('{idUser}', '{passwd}', '{descripcion}', '{color}');                  
    """)
    conexion.commit()
    cursor.execute(f"""
        INSERT INTO STYLE_USUARIO (idUser, className)
        VALUES ('{idUser}', null);
    """)
    conexion.commit()
    conexion.close()

async def actualizarUsuario(idUser, descripcion, color):
    conexion = await AbrirConexionSQL()
    cursor = conexion.cursor()
    cursor.execute(f"""
        UPDATE USUARIO
            SET descripcion = {descripcion},
                color = {color}
            WHERE idUser = {idUser};
    """)
    conexion.commit()
    conexion.close()
