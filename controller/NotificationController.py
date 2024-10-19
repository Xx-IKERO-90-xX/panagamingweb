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

import globals

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

async def get_all_notifications():
    connection = await database.open_database_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM NOTIFICATIONS;")
    result = cursor.fetchall()
    json_result = await database.covert_to_json(result, cursor)
    
    connection.close()
    return json_result

