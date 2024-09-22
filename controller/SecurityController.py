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
import controller.DiscordServerController as DiscordServer
import controller.database as database
import controller.UsuarioController as users
from passlib.hash import pbkdf2_sha256

import globals

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

async def validate_login(username, passwd):
    valid = False
    users_list = await users.get_all_users()
    for user in users_list:
        if username == user['username'] and await verify_passwd(passwd, user['passwd']):
            valid = True
            break
        
    return valid

async def deduce_role(idUser):
    if await DiscordServer.IsEjecutive(idUser):
        return "Ejecutivo"
    
    if await DiscordServer.IsStaff(idUser):
        return "Staff"

    if await DiscordServer.IsMember(idUser):
        return "Miembro"
    
    return "Usuario"
        

async def user_in_discord_server(idUser):
    in_server = False
    list_users = await app.get_discord_users()

    for user in list_users:
        if user['id'] == idUser:
            in_server = True
            break
    
    return in_server
        
        
async def encrypt_passwd(passwd):
    hash_passwd = pbkdf2_sha256.hash(passwd)
    return hash_passwd

async def verify_passwd(passwd, hash):
    return pbkdf2_sha256.verify(passwd, hash)
