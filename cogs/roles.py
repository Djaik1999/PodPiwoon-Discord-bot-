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
        # Пожалуй не самый лучший подход, можно переделать (как миниму название "ending_za")
        guild_info = {
            "Альянс": {"color": discord.Colour.gold(), "ending_za": "за Альянс"},
            "Орда": {"color": discord.Colour.red(), "ending_za": "за Орду"},
            "Пандарен": {"color": discord.Colour.green(), "ending_za": "Пандарен"}
        }

        user_choice = self.values[0]
        user = interaction.user
        guild = interaction.guild
        guild_roles = interaction.guild.roles
        
        # Если вызвать меню по новой, то удалит старую роль (нельзя быть и за орду, и за альянс одновременно)
        for user_role in user.roles:
            if user_role.name in guild_info.keys:
                print(f"Delete role {user_role.name} in {interaction.guild}")
                await user.remove_roles(user_role)
                break
        
        # Если существует на сервере - выбрать её
        for role_in_guild in guild_roles:
            if role_in_guild.name == user_choice:
                role = role_in_guild
                break
        # Иначе сделать новую
        else:
            print(f"role create in {interaction.guild}")
            role = await guild.create_role(name=user_choice, colour=guild_info[user_choice]['color'])

        await user.add_roles(role)
        await interaction.response.send_message(f"{user.mention} теперь {guild_info[user_choice]['ending_za']}")



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