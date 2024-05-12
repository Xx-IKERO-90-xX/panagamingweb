import discord
from discord.ext import commands
from discord.utils import *
import sys
import mysql.connector
import json
import random

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

conection = mysql.connector.connect(
        host="192.168.1.66",
        user="root",
        password="ikero9090",
        database="MINECRAFTPG",
        auth_plugin="mysql_native_password"
)
cursor = conection.cursor()
cursor.execute("""
    SELECT idPersonaje
    FROM USUARIO;
""")
res = cursor.fetchall()
print(res)

