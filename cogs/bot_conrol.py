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

    @commands.command()
    async def help_me(self, ctx):
        """Submit commands list"""

        # Need rework
        admin_message = """Admin commands:
        Testing
        1) test - submit trivial message
        2) base_connection - check sql connection
        Commands
        3) go_offline - disable bot
        4) sync - synchronize commands on this server
        """
        user_message = """List of commands:
        1) whoami - info about bot
        2) rand a b - return random integer in range from a to b (default a=0, b=100)
        """
        slash_commands = """Slash commands (/command):
        1)
        2)
        3)
        4)        
        """

        if ctx.message.author.guild_permissions.administrator:
            message = admin_message + '\n' + user_message
        else:
            message = user_message

        await ctx.message.reply(f"{message}")


    # Testing
    @app_commands.command(name="test", description="testing")
    async def test(self, interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"Hello {name}! I was made with Discord.py!")

    
    @app_commands.command(name="whoami", description="Return info about bot")
    async def whoami(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"I am Ботяня ({bot.user}) and now i am gonna быщ быщ!")


    @app_commands.command(name='base_connection', description='check sql connection')
    @commands.has_permissions(administrator=True)
    async def base_connection(self, interaction: discord.Interaction):
        await interaction.response.send_message(str(base))

    # Commands
    @app_commands.command(name='go_offline', description="Stop bot")
    @commands.has_permissions(administrator=True)
    async def go_offline(self, interaction: discord.Interaction):
        await interaction.response.send_message("Понял, зря быканул")
        await bot.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx):
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(fmt)} commands.")


async def setup(bot):
    await bot.add_cog(BotConrol(bot), guild=guild)
