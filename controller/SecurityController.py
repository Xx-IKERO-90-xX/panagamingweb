import os 
import sys
from passlib.hash import pbkdf2_sha256
from entity.User import *
from extensions import db

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

# Valida los datos del login
async def validate_login(username, passwd):
    user = db.session.query(User).filter(User.username == username).first()
    if user:
        if await verify_passwd(passwd, user.passwd):
            return True
        else:
            return False
    else:
        return False
    

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
