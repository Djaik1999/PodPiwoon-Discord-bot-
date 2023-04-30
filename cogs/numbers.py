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

    @app_commands.command(name="facts", description="Returns facts about numbers or dates")
    @app_commands.describe(number="09/11 (date format 11 september) if want get fact about date, else integer",
                           type_fact="What type of fact you want")
    @app_commands.choices(type_fact=[
        discord.app_commands.Choice(name="Trivial fact", value="trivia"),
        discord.app_commands.Choice(name="Math fact", value="math"),
        discord.app_commands.Choice(name="Fact about Year", value="year"),
        discord.app_commands.Choice(name="Fact about Date", value="date"),
    ])
    async def facts(self,
                    interaction: discord.Interaction,
                    number: str = "1",
                    type_fact: Optional[discord.app_commands.Choice[str]] = "trivia"
                    ):
        """Submit facts about numbers or dates, using 'numbersapi.com' API"""
        if type_fact.value == "date":
            if not re.match(r"^\d{2}/\d{2}$", number):
                await interaction.response.send_message(
                    f"Строка для type_fact='date', должна иметь вид месяц/день (пример: 09/11 - 11 сентября)")
            else:
                response = requests.get(f"http://numbersapi.com/{number}/{type_fact.value}")
                embed = discord.Embed(description=response.text)
                await interaction.response.send_message(embed=embed)
        elif not number.isnumeric():
            await interaction.response.send_message("number - должен быть целым числом")
        else:
            response = requests.get(f"http://numbersapi.com/{number}/{type_fact.value}")
            embed = discord.Embed(description=response.text)
            await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Numbers(bot), guild=guild)
