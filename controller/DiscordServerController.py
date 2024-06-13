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
import controller.PersonajesController as personajes
import controller.database as database
import controller.UsuarioController as usuarios
from globals import guild

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

async def GetDiscordUserByName(name):
    listaUsuarios = await app.ListUsers()
    usuario = 'null'
    for user in listaUsuarios:
        if name == user.name:
            usuario = user
            break
    return usuario

async def UserInDiscordServer(idUser):
    listaUsuarios = []
    listaUsuarios = await app.ListUsers()
    valido = False
    for user in listaUsuarios:
        if user.id == int(idUser):
            valido = True
            break
    return valido

async def ComprobarNombreDiscord(nombre):
    valido = False
    listaUsuario = await app.ListUsers()
    for user in listaUsuario:
        if user.name == nombre:
            valido = True
    return valido