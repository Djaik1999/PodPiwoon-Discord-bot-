import discord
from discord.ext import commands

from settings import bot, tree, guild


class SelectRole(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Альянс", emoji="🐓", description="This is the first role!"),
            discord.SelectOption(label="Орда", emoji="🐷", description="This is the second role!"),
            discord.SelectOption(label="Пандарен", emoji="🐼", description="This is the third role!"),
        ]
        super().__init__(placeholder="Choose your team", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Если добавляются роли, этой прийдется редактировать !!!!!!!!
        guild_color = {
            "Альянс": discord.Colour.gold(),
            "Орда": discord.Colour.red(),
            "Пандарен": discord.Colour.green()
        }

        user = interaction.user
        guild = interaction.guild
        roles = interaction.guild.roles
        
        for r in user.roles:
            print(r.name)
            # Если добавляются роли, этой прийдется редактировать !!!!!!!!
            if r.name in ["Альянс", "Орда", "Пандарен"]:
                print(f"Delete role {r.name}")
                await user.remove_roles(r)
                break

        for r in roles:
            if r.name == self.values[0]:
                role = r
                print("role break")
                break

        else:
            print("role create")
            role = await guild.create_role(name=self.values[0], colour=guild_color[self.values[0]])

        await user.add_roles(role)
        await interaction.response.send_message(f"{user.mention} теперь за {role.name}")



class SelectRoleView(discord.ui.View):
    def __init__(self, *, timeout=30):
        super().__init__(timeout=timeout)
        self.add_item(SelectRole())


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Roles cog loaded')

    @commands.command()
    async def role_menu(self, ctx):
        await ctx.send("Pick a role", view=SelectRoleView(), delete_after=20)


async def setup(bot):
    await bot.add_cog(Roles(bot))


# Регистрация в дерево команд
@tree.command(name="role_menu", description="Choose your side!", guild=guild)
async def role_menu(interaction: discord.Interaction):
    await interaction.response.send_message("Pick a role", view=SelectRoleView(), delete_after=20)