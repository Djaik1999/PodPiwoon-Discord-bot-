from settings import *



@tree.command(name="hello", description="Say Hello", guild=guild)
async def hello_test(interaction):
    await interaction.response.send_message("Hello pidor")


@tree.command(name="test", description="testing", guild=guild)
async def self(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello {name}! I was made with Discord.py!")


@tree.command(name="whoami", description="Return info about bot", guild=guild)
async def self(interaction):
    await interaction.response.send_message(f"I am Ботяня ({bot.user}) and now i am gonna быщ быщ!")


@tree.command(name='about_me', description="What do you think about me?", guild=guild)
async def self(interaction):
    await interaction.response.send_message('грязно выругался')


@tree.command(name='offline', description="Stop bot", guild=guild)
async def self(interaction):
    await interaction.response.send_message("Понял, зря быканул")
    await bot.close()


@tree.command(name="roll", description="return random num in range(a, b)", guild=guild)
async def self(interaction: discord.Interaction, a: int, b: int):
    await interaction.response.send_message(randint(a, b))


# @tree.command(name="db", description="db members", guild=guild)
# async def self(interaction: discord.Interaction):
#     for ch in interaction.guild.channels:
#         # Предотвращает создание записей типа: Голосовые каналы, Текстовые каналы - т.к. у них category None
#         if ch.category:
#             id = f"{interaction.guild.id}_{ch.name}_{interaction.guild.created_at}"
#             base.execute("INSERT OR IGNORE INTO channels VALUES(?, ?, ?, ?)",
#                          (id, ch.name, str(ch.category), interaction.guild.id)
#                          )
#             base.commit()
#             # print(f"Category: {ch.category}, Name: {ch.name}")
#             # print('выполнился channels')
#     await interaction.response.send_message('выполнился')


@tree.command(name='base', description='check sql connection', guild=guild)
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(str(base))


@tree.command(name='embed', description='return your name, test embed', guild=guild)
async def self(interaction: discord.Interaction):
    mbed = discord.Embed(
        description=f"{interaction.user.mention}"
    )
    await interaction.response.send_message(embed=mbed)


@tree.command(name='facts', description='Returs fact about number (integer) or date', guild=guild)
# @tree.describe(type="Type of fact")
# @tree.choices(type=['math', 'date', 'year'])
async def self(interaction: discord.Interaction,
               number: str = '1',
               type: Optional[str] = 'trivia' # math, date, or year
              ):
    if type == 'date':
        if not re.match(r'^\d{2}/\d{2}$', number):
            await interaction.response.send_message(f"Строка для type='date', должна иметь вид месяц/день (пример: 09/11 - 11 сентября)")
        else:
            response = requests.get(f"http://numbersapi.com/{number}/{type}")
            await interaction.response.send_message(response.text)
    elif not number.isnumeric():
        await interaction.response.send_message(f"number - должен быть целым числом")

    response = requests.get(f"http://numbersapi.com/{number}/{type}")
    await interaction.response.send_message(response.text)


# @tree.command(name='clear', description='Delete messages from a channel.', guild=guild)
# @commands.has_permissions(administrator=True)
# async def self(interaction: discord.Interaction,
#                number_of_messages: int = 1,
#                user: Optional[discord.Member] = None,
#                bots: Optional[discord.Member] = False
#                ):
#
#
# # Didnt WORK :  invalid default parameter type given (<class 'discord.ext.commands.parameters.Parameter'>), expected (<class 'int'>, <class 'NoneType'>)
# # async def self(interaction: discord.Interaction,
# #                number_of_messages: int = commands.parameter(description="How much messages will be fetched for check."),
# #                user: Optional[discord.Member] = commands.parameter(default=None, description="Delete User messages."),
# #                bots: Optional[discord.Member] = commands.parameter(default=False, description="Deleted Bots messages.")
# #                ):
#
#
#
#     # Discord wait 3 sec, before send error.
#     # If command didnt respond for 3 sec, discord send error
#     # Переписать комментарий
#     await interaction.response.defer()
#
#     # Need rework, to many duplications
#     if number_of_messages and user is None and bots == False:
#         deleted = await interaction.channel.purge(limit=number_of_messages)
#     else:
#         if user and bots:
#             filter = lambda message: message.author == user or message.author.bot
#         elif bot:
#             filter = lambda message: message.author.bot
#         elif user:
#             filter = lambda message: message.author == user
#
#         deleted = await interaction.channel.purge(limit=number_of_messages, check=filter)
#
#     author_names = {m.author.name for m in deleted}
#     await interaction.channel.send(f"Cleared {len(deleted)} messages by {', '.join(author_names)}")
#     # Need sleep 5 sec and delete this message (autodelete)



# @tree.command(name='slow', description='return slowmode status in channel', guild=guild)
# async def self(interaction):
#     await interaction.response.send_message(interaction.channel)


# Случайное число
# Нужно подумать нужны ли такие команды, если да, то разобраться как их настроить

@bot.command()
async def rand(ctx, a=0, b=100):
    await ctx.reply(randint(a, b))

# @bot.command()
# async def facts(ctx, number):
#     await ctx.reply(randint(0, 100))


@bot.command()
async def test(ctx):
    print('test')
    await ctx.send('грязно выругался')


# @bot.command()
# async def kick(ctx, user: discord.User(), *args, reason='Причина не указана', **kwargs):
#     await bot.kick(user)
#     await ctx.send('Пользователь {user.name} был изгнан по причине {reason}')
