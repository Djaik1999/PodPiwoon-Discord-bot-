from interaction import *
from settings import TOKEN, handler, load
import asyncio


# bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)

asyncio.run(load())
bot.run(TOKEN, log_handler=handler, log_level=debug)