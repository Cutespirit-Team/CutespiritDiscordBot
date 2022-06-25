import discord
from discord.ext import commands
from ..utils import cog_slash_managed
from ...version import author, bot, team

class SlashServerState(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='查看伺服器資訊')
    async def server_state(self, ctx):
        embed=discord.Embed(title=ctx.guild.name, url=bot['url'], description=str(ctx.guild.description), color=0x00ffd5)
        embed.set_author(name=bot['name'], icon_url=bot['icon'])
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name='伺服器人數', value=str(ctx.guild.member_count), inline=True)
        embed.add_field(name='頻道人數', value=str(len(ctx.guild.channels)), inline=True)
        embed.add_field(name='類別數', value=str(len(ctx.guild.categories)), inline=True)
        embed.add_field(name='頻道建立日期', value=str(ctx.guild.created_at), inline=True)
        embed.add_field(name='伺服器id', value=str(ctx.guild.id), inline=True)
        embed.add_field(name='服主', value=str(ctx.guild.owner.name), inline=True)
        embed.add_field(name='語音頻道數量', value=str(len(ctx.guild.voice_channels)), inline=True)
        embed.add_field(name='文字頻道數量', value=str(len(ctx.guild.text_channels)), inline=True)
        embed.add_field(name='舞台頻道數量', value=str(len(ctx.guild.stage_channels)), inline=True)
        embed.set_footer(text='技術提供: ' + team['name'])
        await ctx.send(embed=embed)