import discord
from discord.ext import commands
from discord.utils import *
import sys
import mysql.connector
import json
import random


letras = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
numeros = "0123456789"

unir = f'{letras}{numeros}'
length = 10
passwd = random.sample(unir, length)

passwd_final = "".join(passwd)

print(f"Nueva contraseña: {passwd_final}")

