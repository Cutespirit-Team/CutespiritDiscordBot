import discord
from discord.ext import commands
from ..utils import cog_slash_managed
from asyncio import sleep
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType
from discord.utils import get
import platform  

# TODO: Add uname
# TODO: add more information
# TODO: Add Chooser such as weather

class SlashHardware(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='查看本Bot運行硬體資訊')
    async def hardware(self, ctx):
        info = 'Machine: ' + platform.machine()
        info += '\nVersion: ' + platform.version()
        info += '\nPlatform: ' + platform.platform()
#        info += '\nuname: ' + platform.uname()
        info += '\nSystem: ' + platform.system()
        info += '\nProcessor: ' + platform.processor()
        await ctx.send(info)
