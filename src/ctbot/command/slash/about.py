import discord
from discord.ext import commands
from ..utils import cog_slash_managed
from ...version import author, bot

class SlashAbout(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='版本')
    async def version(self, ctx):
        await ctx.send(f'目前版本： {bot["version"]}')

    @cog_slash_managed(description='關於')
    async def about(self, ctx):
        embed=discord.Embed(title='靈萌bot', url='https://github.com/Cutespirit-Team/CutespiritDiscordBot', description=author['description'], color=0x00ffd5)
        embed.set_author(name='Cutesprit', url='https://cutespirit.tershi.cf/', icon_url=author['icon'])
        embed.set_thumbnail(url=bot['icon'])
        embed.add_field(name='開發日期', value=bot['develope_date'], inline=True)
        embed.add_field(name='目前版本', value=bot['version'], inline=True)
        embed.add_field(name='語言',    value=bot['language'], inline=True)
        embed.add_field(name='目前年齡', value=author['age'], inline=True)
        embed.add_field(name='年級',    value=author['grade'], inline=True)
        embed.add_field(name='使用作業系統', value=author['use_os'], inline=True)
        embed.add_field(name='創作心得',    value=author['experience'], inline=True)
        embed.set_footer(text='更新日期: ' + bot['last_udpate'])
        await ctx.send(embed=embed)
