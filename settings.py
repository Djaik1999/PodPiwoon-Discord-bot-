import os
import asyncio
import logging
import sqlite3

import string
import json
from typing import Optional

import re
from random import randint
from math import pi

import discord
from discord import app_commands
from discord.ext import commands

import requests
from dotenv import load_dotenv


# Logging
handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
debug = logging.DEBUG


# Secure Environment
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')
GUILD_ID = os.getenv('GUILD_ID')


# Initial variables
intents = discord.Intents.all()
guild = discord.Object(id=GUILD_ID)
game = discord.Game('with your API')


# Connect to DB
base = sqlite3.connect('info/PodPiwoon.db')
cur = base.cursor()
if base:
    print('DataBase connected... OK')


# Client (bot)
bot = commands.Bot(command_prefix="-", intents=intents, activity=game)
tree = bot.tree

# bot = discord.Client(intents=intents, activity=game)
bot.synced = False


# Create and sync CommandTree
# tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print("Ready!")

    # Sync tree for commands
    if not bot.synced:
        await tree.sync(guild=guild)
        bot.synced = True
    print(f"We have logged in as {bot.user} in {', '.join([str(g) for g in bot.guilds])}.")



# Old Client
# class aclient(discord.Client):
#     def __init__(self):
#         # activity нужно переместить из инициализации
#         super().__init__(intents=intents, activity=game)
#         self.synced = False
#
#     async def on_ready(self):
#         await self.wait_until_ready()
#
#         # Нужно либо выносить отсюда, либо переделывать логику, ибо программа не видит global
#         # (Второй вариант предпочтительней)
#         # Connect to DB
#         global base, cur
#         base = sqlite3.connect('info/PodPiwoon.db')
#         cur = base.cursor()
#         if base:
#             print('DataBase connected... OK')
#
#         # Sync tree for commands
#         if not self.synced:
#             await tree.sync(guild=guild)
#             self.synced = True
#         print(f"We have logged in as {self.user} in {', '.join([str(g) for g in self.guilds])}.")
# bot = aclient()

# tree = app_commands.CommandTree(bot)