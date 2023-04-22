from interaction import *
# from settings import *
from settings import bot, TOKEN, handler, debug

# bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)

bot.run(TOKEN, log_handler=handler, log_level=debug)
