import os 
import discord
import sys
from discord.ext import commands
from discord.utils import *
import controller.DiscordServerController as DiscordServer
from passlib.hash import pbkdf2_sha256
from entity.User import *
from extensions import db


import globals

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

# Valida los datos del login
async def validate_login(name, passwd):
    users = User.query.all()
    print(users)
    for u in users:
        if await verify_passwd(passwd, u.passwd):
            return True
        else:
            return False

# Deduce el rol del usuario al iniciar sesión
async def deduce_role(idUser):
    if await DiscordServer.IsEjecutive(idUser):
        return "Ejecutivo"
    
    if await DiscordServer.IsStaff(idUser):
        return "Staff"

    if await DiscordServer.IsMember(idUser):
        return "Miembro"
    
    return "Usuario"
        
# Comprueba si el usuario está dentro del servidor de Discord
async def user_in_discord_server(idUser):
    in_server = False
    list_users = await app.get_discord_users()

    for user in list_users:
        if user.id == idUser:
            in_server = True
            break
    
    return in_server
        

# Encripta la contraseña
async def encrypt_passwd(passwd):
    hash_passwd = pbkdf2_sha256.hash(passwd)
    return hash_passwd

# Verifica si la contraseña concuerda con la del hash
async def verify_passwd(passwd, hash):
    return pbkdf2_sha256.verify(passwd, hash)
