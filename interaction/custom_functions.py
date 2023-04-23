from settings import *


approwed_words = {
    'задержка': bot.latency,
    'стикеры': bot.stickers,
    'голосовые': bot.voice_clients,
    'users': bot.users,
    'ясно': 'хуясно, черт'

}   # Извиняюсь за мат пред теми кто читает, но писал бота для своего сервера

def check_word_for_event_typing(word):
    if word.casefold() in approwed_words:
        return approwed_words[word]
