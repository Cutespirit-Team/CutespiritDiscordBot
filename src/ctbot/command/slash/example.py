import discord
from discord.ext import commands
from ..utils import cog_slash_managed

class SlashExample(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='ping')
    async def ping(self, ctx):
        await ctx.send('Pong!')
