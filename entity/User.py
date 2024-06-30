import os 
import discord
from discord.ext import commands
from discord.utils import *
from flask import request, Flask, render_template, redirect, session, sessions, url_for
import mysql.connector
import json
import random
import asyncio
from controller.PersonajesController import *
from controller.database import *
from controller.UsuarioController import *

class User:
    def __init__(self, idUser, passwd, descripcion, mithrilCoins):
        self.idUser = idUser
        self.passwd = passwd
        self.descripcion = descripcion
        self.mithrilCoins = mithrilCoins