import discord
from discord.ext import commands
import asyncio
import globals
import app

intents = discord.Intents.default()
intents.guilds = True
intents.members = True


bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    globals.guild = bot.get_guild(app.datos["discord"]["server"]["id"])
    if globals.guild is not None:
        print(f"El bot se ha conectado con el servidor: {globals.guild.name}")
    else:
        print("El bot no pudo conectarse con el servidor")

    app.app.run(
        port = app.datos["flask"]["port"], 
        host = app.datos["flask"]["host"],
        debug=True
    )
    
def run_discord_bot():
    bot.run(app.datos["discord"]["token"])

def start_discord_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(run_discord_bot())

