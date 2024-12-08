import discord
import globals
import json

datos = {}
with open('settings.json') as archivo:
    datos = json.load(archivo)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    globals.guild = bot.get_guild(datos["discord"]["server"]["id"])
    print(f"Bot conectado como {bot.user}")

# Define funciones relacionadas con Discord aquí

def run_bot():
    bot.run(datos['discord']['token'])