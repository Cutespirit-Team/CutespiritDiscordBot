import discord
from discord.ext import commands
from ..utils import cog_slash_managed
from asyncio import sleep
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType
from discord.utils import get

class SlashSend(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed()
    async def tw(self, ctx):
        await ctx.send('Taiwan No.1')

    @cog_slash_managed(description='重複 n 次訊息',
        options=[
        create_option('msg', '訊息',
        option_type=SlashCommandOptionType.STRING,
        required=True),
        create_option('repeat', '次數: 1 ~ 5 次',
        option_type=SlashCommandOptionType.INTEGER,
        required=False),
        create_option('counter', '計數器',
        option_type=SlashCommandOptionType.BOOLEAN,
        required=False),
        create_option('delay', '延遲: 0 ~ 10 秒',
        option_type=SlashCommandOptionType.INTEGER,
        required=False)])
    async def sendmsg(self, ctx, msg:str, repeat: int=1, counter: bool=False, delay: int=1):
        delay = min(10, max(0, delay))
        repeat = min(5, max(1, repeat))

        await ctx.send('start', hidden=True)
        channel = self.bot.get_channel(ctx.channel_id)
        for n in range(repeat):
            txt = msg

            if counter:
                txt += f'x{n+1}'

            await channel.send(txt)
            await sleep(delay)
