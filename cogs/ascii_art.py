import discord
from discord import app_commands
from discord.ext import commands

from typing import Optional
from art import art
import requests
from bs4 import BeautifulSoup
import re
import random
from settings import guild, base, bot


class AsciiArt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("AsciiArt cog loaded")


    # Commands

    @app_commands.command(name="ascii_art", description="return ascii art based on your text")
    async def ascii_art(self, interaction: discord.Interaction,
                    text: str,
                    ):
        """Sends an ascii drawing if found in the library."""
        try:
            result_art = art(text)
        except:
            result_art = "not found ascii art for your text"
        await interaction.response.send_message(f"{result_art}")


    # return None, typing only in console
    # Mb later try catch output and send here
    # @app_commands.command(name="ascii_text", description="return ascii text")
    # @app_commands.choices(font=[
    #     discord.app_commands.Choice(name="Random", value="random"),
    #     discord.app_commands.Choice(name="Random small", value="random_small"),
    #     discord.app_commands.Choice(name="Random medium", value="random_medium"),
    #     discord.app_commands.Choice(name="Random large", value="random_large"),       
    #     discord.app_commands.Choice(name="Block", value="block"),
    #     discord.app_commands.Choice(name="Cybermedium", value="cybermedium"),
    # ])
    # async def ascii_text(self, interaction: discord.Interaction,
    #                      text: str,
    #                      font: Optional[discord.app_commands.Choice[str]] = "random"
    #                     ):
    #     """Sends a text in ascii art format."""
    #     try:
    #         result_text = tprint(text, font=font)
    #     except:
    #         result_text = "can't generate ascii text as you requested, try changing the text"

    #     await interaction.response.send_message(f"{result_text}")


    @app_commands.command(name="large_ascii_art", description="uses twitchquotes.com")
    async def large_ascii_art(self, interaction: discord.Interaction,
                              query_search: str,
                              only_one: Optional[bool] = False):
        """Fetch ascii arts from twitchquotes.com"""
        
        await interaction.response.defer(ephemeral=True)

        # Custom functions

        # For correct get page
        def get_soup(url):
            response = requests.get(url, headers)
            return BeautifulSoup(response.text, "html.parser")
        
        # Check copypasta for ascii art tag
        def check_for_ascii_art(copypasta):
            parent = copypasta.parent.parent
            return 'twitch-copypasta-card-ascii_art' in parent['class']

        images = list()
        main_url = f"https://www.twitchquotes.com/copypastas/search"
        # HARDCODED
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}

        # If have pagination, get max page number
        page = get_soup(main_url + f"?page=1&query={query_search}")

        pagination = page.find('ul', {"class": "pagination"})
        pages = 1        

        if pagination:
            for child in pagination:
                if child.text.isnumeric():
                    pages = int(child.text)
       
        # For each page fetch ascii art and add to images list       
        # left commented code for DEBUG  
        for page_num in range(1, pages + 1):
            # print(f"Page_num = {page_num}")
            page = get_soup(main_url + f"?page={page_num}&query={query_search}")

            ascii_arts = page.findAll("div", {"id": re.compile(r'^clipboard_copy_content_\d{4}$')})
            
            for image in ascii_arts:
                if check_for_ascii_art(image):
                    # print(image.text)
                    images.append(image)
                    # await interaction.channel.send(image.text)

        if len(images) == 0:
            await interaction.followup.send("Not found any art with you query")
        else:
            await interaction.followup.send("Да начнется СПАМ")

        # Sends images in channel
        if only_one:
            random_image = random.choice(images)
            await interaction.channel.send(random_image.text)
        else:
            for image in images:
                await interaction.channel.send(image.text)

            await interaction.channel.send("That's all Folks!")

        
async def setup(bot):
    await bot.add_cog(AsciiArt(bot), guild=guild)
