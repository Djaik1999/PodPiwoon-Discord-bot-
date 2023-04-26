import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import re
import requests

from settings import guild


class Numbers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Numbers cog loaded')

    @app_commands.command(name="facts", description="Returs fact about number (integer) or date")
    async def facts(self, 
                    interaction: discord.Interaction,
                    number: str = "1",
                    type: Optional[str] = "trivia"
                    ):
        if type == "date":
            if not re.match(r"^\d{2}/\d{2}$", number):
                await interaction.response.send_message(f"Строка для type='date', должна иметь вид месяц/день (пример: 09/11 - 11 сентября)")
            else:
                response = requests.get(f"http://numbersapi.com/{number}/{type}")
                embed = discord.Embed(description=response.text)
                await interaction.response.send_message(embed=embed)
        elif not number.isnumeric():
            await interaction.response.send_message("number - должен быть целым числом")
        else:
            print('Facts в конце')
            response = requests.get(f"http://numbersapi.com/{number}/{type}")
            embed = discord.Embed(description=response.text)
            await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Numbers(bot), guild=guild)
