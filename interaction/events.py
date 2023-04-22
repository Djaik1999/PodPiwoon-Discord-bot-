from settings import bot, base


# @bot.event
# async def on_ready():
#     await bot.wait_until_ready()
#     print("Ready!")
#
#     # Connect to DB
#     # Нужно сделать так чтобы передавало в другие файлы при импорте
#     global base, cur
#     base = sqlite3.connect('info/PodPiwoon.db')
#     cur = base.cursor()
#     if base:
#         print('DataBase connected... OK')
#
#     # Sync tree for commands
#     if not bot.synced:
#         await tree.sync(guild=guild)
#         bot.synced = True
#     print(f"We have logged in as {bot.user} in {', '.join([str(g) for g in bot.guilds])}.")


# Вход и выход пользователя
@bot.event
async def on_member_join(member):
    bot.get_channel
    for ch in bot.get_guild(member.guild.id).channels:
        if ch.position == 0:
            main_channel = ch
            # нужно сделать прерывание !!!!!!!!!!!!!!!!

    # for ch in :
    #     if ch.name == 'spam-bordы' or ch.name == 'основной':
    print(f"{member} join in server!")
    if member.bot:
        print(f"{member} bot")
        role = discord.utils.get(member.guild.roles, name='Боты')
        await member.add_roles(role)
        await main_channel.send('Хто позвал сюда другого бота???? Вы что решили меня заменить?? Побойтесь кары господней!!')
    else:
        await bot.get_channel(ch.id).send(f"Поприветствуйте {member} на сервере, быстро!!")


@bot.event
async def on_member_remove(member):
    if member.bot:
        await main_channel.send(f"Туда его, етого {member}. Я тут главный!")
    else:
        await main_channel.send(f"У меня печальные новости, нас покинул {member}. Мы тебя не забудем.")


# Голосовые события
@bot.event
async def on_voice_server_update(data, /):
    await print(data)


@bot.event
async def on_voice_state_update(data, /):
    await print(data)


# Подключение бота к серверу, первоначальная настройка
@bot.event
async def on_guild_join(guild):
    await bot.wait_until_ready()

    # OR IGNORE - игнорирует, если существует
    base.execute('INSERT OR IGNORE INTO guilds VALUES(?, ?, ?)', (guild.id, str(guild.name), str(guild.owner.name)))
    base.commit()
    print('выполнился guilds')

    for ch in guild.channels:
        # явно передаю null для автогенерации id, иначе выдаёт error (требует передачи 3 аргументов)
        # base.execute("INSERT OR IGNORE INTO channels VALUES(null, ?, ?)", (str(ch.name), guild.id))

        # Предотвращает создание записей типа: Голосовые каналы, Текстовые каналы - т.к. у них category None
        if ch.category:
            id = f"{guild.id}_{ch.name}_{guild.created_at}"
            base.execute("INSERT OR IGNORE INTO channels VALUES(?, ?, ?, ?)",
                         (id, ch.name, str(ch.category), guild.id)
                         )
            base.commit()
            print(f"Category: {ch.category}, Name: {ch.name} - выполнился channels")

    for member in guild.members:
        # 0 четвёртым аргументом - это default значение для новой записи (можно переделать?)
        base.execute("INSERT OR IGNORE INTO members VALUES(?, ?, ?, ?, ?) ", \
            (member.id, str(member.name), str(member.nick), 0, member.guild.id)
                     )
        base.commit()
        print(f' {member.name} - выполнился')


