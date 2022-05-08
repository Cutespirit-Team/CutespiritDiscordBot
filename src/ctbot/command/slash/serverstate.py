import discord
from discord.ext import commands
from ..utils import cog_slash_managed

class SlashServerState(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='查看伺服器人數')
    async def membercount(self, ctx):
        member_count = ctx.guild.member_count
        txt = '目前伺服器人數: ' + str(member_count)
        await ctx.send(txt)
