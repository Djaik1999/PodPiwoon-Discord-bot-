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


# Bot (bot)
bot = commands.Bot(command_prefix=commands.when_mentioned_or("-"), intents=intents, activity=game)
bot.synced = False
tree = bot.tree


# Client
# bot = discord.Client(intents=intents, activity=game)
# bot.synced = False
# tree = app_commands.CommandTree(bot)


# Create and sync CommandTree
# @bot.event
# async def on_ready():
#     await bot.wait_until_ready()
#     print("Ready!")
#
#     # Sync tree for commands
#     if not bot.synced:
#         await tree.sync(guild=guild)
#         bot.synced = True
#     print(f"We have logged in as {bot.user} in {', '.join([str(g) for g in bot.guilds])}.")


# Run
async def load():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

# async def start():
#     await
#     await bot.start(TOKEN)
    # await bot.run(TOKEN, log_handler=handler, log_level=debug)
