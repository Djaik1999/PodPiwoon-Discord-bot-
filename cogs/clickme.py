from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

from settings import guild


class Buttons(discord.ui.View):
    def __init__(self, *, timeout= 180):
        super().__init__(timeout=timeout)


    @discord.ui.button(label="clickme", style=discord.ButtonStyle.gray)
    async def my_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"You clicked me! <a:boobsbounce:1083115954810142740>")


class Clickme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Clickme cog loaded")

    @commands.command()
    async def click(self, ctx):
        await ctx.send("A message with a button", view=Buttons())


async def setup(bot):
    await bot.add_cog(Clickme(bot), guild=guild)
