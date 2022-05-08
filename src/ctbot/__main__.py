import logging
from . import CTBot

slash_logger = logging.getLogger('discord_slash')
slash_logger.addHandler(logging.StreamHandler())
slash_logger.setLevel(logging.INFO)

ctbot_logger = logging.getLogger('ctbot')
ctbot_logger.addHandler(logging.StreamHandler())
ctbot_logger.setLevel(logging.INFO)
bot = CTBot()
bot.run()
