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


@bot.event
async def on_ready():
    guild = bot.get_guild(793956939687133184)
    for m in guild.members: 
        print(m)

bot.run("OTY3NDI3OTY2NTQxOTE0MTUy.Gq5ubM.5669OrL9msRv5Y1R_z0zxaYkU-MKB_nHaTWl74")

