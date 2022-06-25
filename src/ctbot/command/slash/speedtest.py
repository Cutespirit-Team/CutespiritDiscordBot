import discord
from discord.ext import commands
from ..utils import cog_slash_managed
from asyncio import sleep
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType
from discord.utils import get
import speedtest

# TODO: best['country'] to Chinese. ex: Taiwan = 台灣 (dict)

class SlashSpeedtest(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='測試上傳與下載速度')
    async def speedtest(self, ctx):
        test = speedtest.Speedtest()
        await ctx.send('載入伺服器清單...')
        test.get_servers()
#        await ctx.send('選擇最佳伺服器...')
        best = test.get_best_server()
        await ctx.send(f"找到: {best['host']} 位於 {best['country']}")
#        await ctx.send('執行上傳測試...')
        download_result = test.download()
#        await ctx.send('執行下載測試...')
        upload_result = test.upload()
        ping_result = test.results.ping
        result = f"上傳速度: {download_result /1024 /1024:.2f} Mbps \n"
        result += f"下載速度: {upload_result /1024 /1024:.2f} Mbps \n"
        result += f"Ping速度: {ping_result:.2f} ms"
        await ctx.send(result)
