import discord
from discord.ext import commands
from ..utils import cog_slash_managed
from ...version import author, bot ,team
import platform

class SlashAbout(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(base="about", description='版本')
    async def version(self, ctx):
        await ctx.send(f'目前版本： {bot["version"]}')

    @cog_slash_managed(base="about", description='關於機器人')
    async def dcbot(self, ctx):
        embed=discord.Embed(title=bot['name'], url=bot['url'], description=bot['description'], color=0x00ffd5)
        embed.set_author(name=team['name'], url=bot['url'], icon_url=bot['icon'])
        embed.set_thumbnail(url=bot['icon'])
        embed.add_field(name='開發日期', value=bot['develope_date'], inline=True)
        embed.add_field(name='目前版本', value=bot['version'], inline=True)
        embed.add_field(name='語言', value=bot['language'], inline=True)
        embed.add_field(name='使用作業系統', value=platform.system(), inline=True)
        embed.add_field(name='創作心得', value=bot['experience'], inline=True)
        embed.set_footer(text='更新日期: ' + bot['last_udpate'])
        await ctx.send(embed=embed)
    
    @cog_slash_managed(base="about", description="關於作者")
    async def author(self, ctx):
        embed=discord.Embed(title=author['name'], url=author['url'], description=author['description'], color=0x00ffd5)
        embed.set_author(name=bot['name'], url=bot['url'], icon_url=bot['icon'])
        embed.set_thumbnail(url=author['icon'])
        embed.add_field(name='目前年齡', value=author['age'], inline=True)
        embed.add_field(name='性別', value=author['gender'], inline=True)
        embed.add_field(name='年級', value=author['grade'], inline=True)
        embed.add_field(name='使用作業系統', value=author['use_os'], inline=True)
        embed.set_footer(text='生日: ' + author['birthday'])
        await ctx.send(embed=embed)

    @cog_slash_managed(base="about", description="關於團隊")
    async def cutespirit(self, ctx):
        embed=discord.Embed(title=bot['name'], url=bot['url'], description=team['description'], color=0x00ffd5)
        embed.set_author(name=team['name'], url=team['url'], icon_url=team['icon'])
        embed.set_thumbnail(url=team['icon'])
        embed.add_field(name='團員人數', value=team['teammate_count'], inline=True)
        embed.add_field(name='團長', value=team['team_leader'], inline=True)
        embed.add_field(name='副團長', value=team['team_coleader'], inline=True)
        embed.add_field(name='團隊創立人員', value=team['team_cofounder'], inline=True)
        embed.set_footer(text='團隊建立日期: ' + team['founded_day'])
        await ctx.send(embed=embed)
