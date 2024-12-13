import os 
import discord
import sys
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for
from globals import guild
from entity.User import *

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app
from extensions import db

async def get_discord_user_by_username(username):
    discord_user = {}
    
    users_list = await app.get_discord_users()
    app_user = db.session.query(User).filter(username == username).first()


    for user in users_list:
        if user.id == int(app_user.id):
            discord_user = user
    
    return discord_user

async def UserInDiscordServer(idUser):
    listaUsuarios = []
    listaUsuarios = await app.get_discord_users()
    valido = False
    
    for user in listaUsuarios:
        if user.id == int(idUser):
            valido = True
            break
        
    return valido

async def get_discord_user_by_id(idUser):
    result = {}
    users_list = await app.get_discord_users()
    
    for user in users_list:
        if user.id == int(idUser):
            result = user
    
    return result
            

async def ComprobarNombreDiscord(nombre):
    valido = False
    listaUsuario = await app.get_discord_users()
    
    for user in listaUsuario:
        if user.name == nombre:
            valido = True
            
    return valido

async def IsEjecutive(idUser):
    isEjecutive = False
    listUsers = await app.get_discord_users()
    listEjecutives = await app.get_discord_ejecutives(listUsers)
    
    for ejec in listEjecutives:
        if idUser == ejec.id:
            isEjecutive = True
            break
        
    return isEjecutive

async def IsStaff(idUser):
    isStaff = False
    listUsers = await app.get_discord_users()
    listEjecutives = await app.get_discord_ejecutives(listUsers)
    listStaff = await app.get_discord_staff_users(listUsers, listEjecutives)
    
    for staff in listStaff:
        if idUser == staff.id:
            isStaff = True
            break
        
    return isStaff

async def IsMember(idUser):
    isMember = False 
    listUsers = await app.get_discord_users()
    listEjecutives = await app.get_discord_ejecutives(listUsers)
    listStaff = await app.get_discord_staff_users(listUsers, listEjecutives)
    listMembers = await app.get_discord_members(listUsers, listStaff, listEjecutives)
    
    for member in listMembers:
        if idUser == member.id:
            isMember = True
            break
        
    return isMember