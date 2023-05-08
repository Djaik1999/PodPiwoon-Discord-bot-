import discord
from discord import app_commands
from discord.ext import commands

from typing import Optional
from math import ceil
import requests
from bs4 import BeautifulSoup

from settings import guild


class ImgBoards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    commands.Cog.listener()
    async def on_ready(self):
        print("ImgBoards cog loaded")

    
    # Functions

    @app_commands.command(name="rule34", description="write tags, get images, videos")
    @app_commands.describe(query_search="what you looking for",
                           score_sort="Sort by rating (best first)?",
                           file_format="Images, videos or all")
    @app_commands.choices(file_format=[
        discord.app_commands.Choice(name="Videos", value="+video"),
        discord.app_commands.Choice(name="Images", value="+-video"),
        discord.app_commands.Choice(name="All", value=""),
    ])
    async def rule34(self, interaction: discord.Interaction,
                     query_search: str,
                     amount: Optional[int] = 1,
                     score_sort: Optional[bool] = False,
                     file_format: Optional[discord.app_commands.Choice[str]] = ""):

        await interaction.response.defer(ephemeral=True)

        # Variables

        main_url = "https://api.rule34.xxx/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}

        limit = 100
        if amount <= limit:
            pages = 1
            limit = amount
        else:
            # на последней странице нужно пересчитать limit !!!!
            pages = ceil(amount / limit)

        # pages = 1 if amount <= limit else ceil(amount / limit)
        sort_tag = "+sort%3Ascore" if score_sort else '+sort:random'
        file_format_tag = '' if isinstance(file_format, str) else file_format.value

        counter = 0

                
        for pid in range(0, pages):             # pid = Page id
            print(f"!!! PAGE № {pid + 1} !!!")

            page_url = f"{main_url}index.php?page=dapi&s=post&q=index&tags={query_search}{file_format_tag}{sort_tag}&limit={limit}&pid={pid}"
            print(f"URL: {page_url}")
            response = requests.get(page_url, headers=headers)

            page = BeautifulSoup(response.text, features="xml")
            all_posts = page.findAll("post")
            if not all_posts:
                print(f"Posts not found: {pid - 1} was last page.")
                break
            
            for post in all_posts:
                counter += 1
                id = post.get("id")
                file = post.get("file_url")
                tags = post.get("tags")
                source = post.get("source")
                
                # await interaction.channel.send(f"{counter}. {file} \nID: {id} \nTags: {tags} \nSource: {source}", suppress_embeds=True)
                await interaction.channel.send(file)
                # await interaction.channel.send(source)

        if counter == 0:        
            await interaction.followup.send("Not found")
        else:
            await interaction.followup.send(f"Let's go")

        await interaction.channel.send(f"That's all Folks! Send {counter} files")


async def setup(bot):
    await bot.add_cog(ImgBoards(bot), guild=guild)
