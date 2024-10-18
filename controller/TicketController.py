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
import controller.database as database
import controller.UsuarioController as users
import controller.DiscordServerController as discord
from globals import guild

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

DISCORD_BOT = app.bot

async def create_tiket(texto, idUser, estado):
    connection = await database.open_database_connection()
    cursor = connection.cursor()

    cursor.execute(f"""
        INSERT INTO TIKET (texto, idUser, estado)
        VALUES ('{texto}', '{idUser}', '{estado}');
    """)

    connection.commit()
    connection.close()

async def send_discord_notification(idUser, username, texto):
    channel = await DISCORD_BOT.get_channel(app.datos['discord']['channels']['ch_tikets_id'])
    user = await discord.get_discord_user_by_id(int(idUser))
    embed = discord.Embed(
        title=f"**TIKET DE {username}**"
    )