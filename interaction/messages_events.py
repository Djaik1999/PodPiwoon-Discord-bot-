from settings import bot, base, json, string
from .custom_functions import check_word_for_event_typing


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message[0] == bot.command_prefix:
        return

    # prevent looping bot (answer at self messages)
    if message.author != bot.user:
        # Проверки на определённые слова
        if message.content.casefold().startswith('ты '):
            m = message.content[3:]
            await message.reply(f"Сам {m}")

        # Проверка мата
        # VER 1
        # clean_message = {i.lower().translate(str.maketrans('', '', string.punctuation)) \
        #                  for i in message.content.split(' ')}

        # if clean_message.intersection(set(json.load(open('info/cenz.json')))) != set():
        #     await message.channel.send(f' {message.author.mention}, ууу... кого погубам отшлёпать?? И не пиши в {message.channel} больше, от тебя говной ваняет!')

        # VER 2
        test = string.punctuation + ' '
        clean_message = message.content.lower().translate(str.maketrans('', '', test))
        for m in set(json.load(open('info/cenz.json'))):
            if clean_message.find(m) != -1:
                await message.channel.send(f' {message.author.mention}, ууу... кого погубам отшлёпать?? И не пиши в {message.channel} больше, от тебя говной ваняет!')
                break


        # # Проверки на определённые слова
        # if message.content.casefold().startswith('ты '):
        #     m = message.content[3:]
        #     await message.reply(f"Сам {m}")
        #
        # # Переписать через словарь или классы, функцию
        # elif message.content.casefold() == "грац":
        #     await message.channel.send(
        #         f"Падите ниц гниль и будьте благодарны за возможность лицезреть меня"
        #     )
        # elif message.content.casefold().startswith('я '):
        #     await message.reply(f'{message.author.mention} {message.content[2:]}')
        #
        # elif message.content.casefold() == 'отвали':
        #     await message.channel.send("Понял, зря быканул")
        #     await bot.close()
        #
        # word = check_word_for_event_typing(message.content)
        # elif word:
        #     await message.channel.send(word)
        #
        # elif message.content.lower() in ['число пи', 'пи', 'pi', 'число p', 'число п', 'число pi']:
        #     await message.channel.send(pi)
        #
        # # Пример с wait_for
        # if message.content.startswith('$thumb'):
        #     channel = message.channel
        #     await channel.send('Send me that 👍 reaction, mate')
        #
        #     def check(reaction, user):
        #         return user == message.author and str(reaction.emoji) == '👍'
        #
        #     try:
        #         reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        #     except asyncio.TimeoutError:
        #         await channel.send('👎')
        #     else:
        #         await channel.send('👍')

        # передаёт сообщение дальше для обработки комманд (которые через PREFIX)
        # await bot.process_commands(message)


# @bot.event
# async def on_message_delete(message):
#     await message.channel.send(f'Было удалено сообщение "{message.content}" by "{message.author}"')



# @bot.event
# async def on_typing(channel, user, when):
#     await channel.send(f"Посторонись, {user.mention} печатает... Не торопись, собирись с мыслями, никто тебя не подгоняет")


@bot.event
async def on_reaction_add(reaction, user):
    print(f"{user.dm_channel} dm_channel")
    print(f"{user} add {reaction}")
    await user.send('content')