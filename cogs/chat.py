import discord
from discord import app_commands
from discord.ext import commands

from typing import Optional
from settings import guild, bot
import json
import string
from math import pi


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Chat cog loaded")


    # Commands

    @app_commands.command(name="get_all_emojis", description="submit emojis from current server")
    @app_commands.describe(oneline="Send all emoji in one message or create a message for each emoji?",
                           animated="Animated or not?")
    async def get_all_emojis(self, interaction: discord.Interaction, 
                             oneline: Optional[bool] = False, 
                             animated: Optional[bool] = True
                            ):
        
        await interaction.response.defer()
        await interaction.channel.typing()
        counter = 0

        # Много ветвлений, но они убирают дупликацию кода
        if oneline:
            emoji_list = list()
            animated_arg = 'a' if animated else ''
            for emoji in interaction.guild.emojis:
                if animated and emoji.animated:
                    counter += 1
                    emoji_list.append(emoji)
                elif animated == False and emoji.animated == False:
                    counter += 1
                    emoji_list.append(emoji)


            await interaction.channel.send(" ".join(map(lambda em: f"<{animated_arg}:{em.name}:{em.id}>", emoji_list)))

        else:
            await interaction.channel.send("Да начнется спам")
            for emoji in interaction.guild.emojis:
                if animated and emoji.animated:
                    counter += 1
                    await interaction.channel.send(f"<a:{emoji.name}:{emoji.id}>")
                elif animated == False and emoji.animated == False:
                    counter += 1
                    await interaction.channel.send(f"<:{emoji.name}:{emoji.id}>")

        await interaction.followup.send(f"Sends {counter} emojis")


    # Events

    @commands.Cog.listener("on_message")
    async def get_emoji(self, message):
        """Отпраляет emoji; принимает имя; позволяет обойти Nitro (боты почему-то могут отправлять платные стикеры)"""
        if message.author == bot.user:
            return

        if message.content.casefold().startswith("::"):
            await message.channel.typing()

            clear_message = message.content.split(' ')[0].strip(': ')
            
            for emoji in message.channel.guild.emojis:
                if clear_message == emoji.name:

                    id = f" id = {emoji.id}" if message.content.casefold().endswith('id') else '' # Aded for developing
                    animated_arg = 'a' if emoji.animated else ''

                    await message.channel.send(content=f"<{animated_arg}:{emoji.name}:{emoji.id}>{id}")
                    break
            else:
                await message.channel.send(content="I'm didn't find the emoji")

            await message.delete()


    @commands.Cog.listener("on_message")
    async def alias_message(self, message):
        """Пиши слово из списка в чат и получай ответ"""

        if message.author == bot.user:
            return
        
        # Словарь с командными словами (Alias)
        approwed_words = {
            'задержка': bot.latency,
            'грац': 'Падите ниц гниль и будьте благодарны за возможность лицезреть меня',
            'стикеры': bot.stickers,
            'голосовые': bot.voice_clients,
            'users': bot.users,
            'ясно': 'хуясно, черт',
            'check_for_pi': ('число пи', 'пи', 'pi', 'число p', 'число п', 'число pi')
            }   # Извиняюсь за мат перед теми кто читает, но писал бота для своего сервера

        break_flag = False
        for approwed_word in approwed_words.keys():
            if break_flag:
                break
            if approwed_word == 'check_for_pi':
                for inner_word in approwed_words['check_for_pi']:
                    if message.content.casefold() == inner_word:
                        break_flag = True
                        await message.reply(pi)
            
            elif message.content.casefold() == approwed_word:
                break_flag = True
                await message.reply(approwed_words[approwed_word])

            # print(f"{approwed_word}")

        # !!! ПРОИСХОДИТ УТЕЧКА ВРЕМЕНИ КУДА-ТО НУЖНО ТЕТСИТЬ (или у меня затупил инет)

    
    @commands.Cog.listener("on_message")
    async def obscene_language_check(self, message):
        """Проверка мата"""

        # Нужно вынести в основной on_message
        # Видимо listener срабатывает раньше исполнения кода в on_message()
        if message.author == bot.user:
            return

        # VER 2: учитывает пробелы
        test = string.punctuation + ' '
        clean_message = message.content.lower().translate(str.maketrans('', '', test))
        for m in set(json.load(open('info/cenz.json'))):
            if clean_message.find(m) != -1:
                await message.channel.send(f' {message.author.mention}, ууу... кого погубам отшлёпать??')
                break

        # VER 1: разбивает по пробелам
        # clean_message = {i.lower().translate(str.maketrans('', '', string.punctuation)) \
        #                  for i in message.content.split(' ')}

        # if clean_message.intersection(set(json.load(open('info/cenz.json')))) != set():
        #     await message.channel.send(f' {message.author.mention}, ууу... кого погубам отшлёпать??')



async def setup(bot):
    await bot.add_cog(Chat(bot), guild=guild)
