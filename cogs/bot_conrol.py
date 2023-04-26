import discord
from discord import app_commands
from discord.ext import commands

from settings import guild, base, bot


class BotConrol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("BotConrol cog loaded")

    # Testing
    @app_commands.command(name="test", description="testing")
    async def test(self, interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"Hello {name}! I was made with Discord.py!")

    
    @app_commands.command(name="whoami", description="Return info about bot")
    async def whoami(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"I am Ботяня ({bot.user}) and now i am gonna быщ быщ!")


    @app_commands.command(name='base_connection', description='check sql connection')
    async def base_connection(self, interaction: discord.Interaction):
        await interaction.response.send_message(str(base))

    # Commands
    @app_commands.command(name='go_offline', description="Stop bot")
    async def go_offline(self, interaction: discord.Interaction):
        await interaction.response.send_message("Понял, зря быканул")
        await bot.close()

    @commands.command()
    async def sync(self, ctx):
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(fmt)} commands.")


async def setup(bot):
    await bot.add_cog(BotConrol(bot), guild=guild)
