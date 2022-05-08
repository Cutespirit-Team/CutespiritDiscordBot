import discord
from discord.ext import commands
from ..utils import cog_slash_managed

class SlashActivity(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='更改狀態')
    async def status(self, ctx, playing: str):
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(playing))
        await ctx.send('已變更狀態', hidden=True)
