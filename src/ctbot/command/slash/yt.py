import discord
from discord.ext import commands
from ..utils import cog_slash_managed
from ...player import SimplePlayer

# TODO: make permission check for next, prev, stop, pause, lcear function
class SlashYT(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.player = SimplePlayer()

    @cog_slash_managed(base='yt', description='播放')
    async def play(self, ctx, url: str=None):
        # TODO: check url format
        if not ctx.author.voice:
            await ctx.send('無法取得語音頻道', hidden=False)
            return

        if not self.player.is_playing() and not self.player.is_paused():
            self.player.voice_channel = ctx.author.voice.channel

        if url:
            if self.player.voice_channel == ctx.author.voice.channel:
                # TODO: add requester
                self.player.playlist.add_entry(url, '')
                txt = '已加入清單，URL = ' + str(url)
                await ctx.send(txt, hidden=False)
            else:
                await ctx.send('語音頻道與機器人不符, 無權添加', hidden=False)
        else:
            await ctx.send('播放音樂', hidden=False)

        await self.player.play()
        
    @cog_slash_managed(base='yt', description='暫停/繼續')
    async def pause(self, ctx, toggle: bool=True):
        self.player.pause(toggle=toggle)
        await ctx.send('暫停/繼續音樂', hidden=False)

    @cog_slash_managed(base='yt', description='停止')
    async def stop(self, ctx, leave: bool=True):
        self.player.stop(leave=leave)
        await ctx.send('停止音樂', hidden=False)

    @cog_slash_managed(base='yt', description='上一首')
    async def prev(self, ctx):
        self.player.playlist.go_prev()
        self.player.stop(leave=False)
        await ctx.send('上一首', hidden=False)

    @cog_slash_managed(base='yt', description='下一首')
    async def next(self, ctx):
        # self.player.playlist.go_next(force=True)
        self.player.stop(leave=False)
        await ctx.send('下一首', hidden=False)

    @cog_slash_managed(base='yt', description='清除播放清單')
    async def clear(self, ctx):
        self.player.playlist.clear_entries()
        await ctx.send('已清除播放清單', hidden=False)
        