import discord
import json
import requests
from discord.ext import commands
from ..utils import cog_slash_managed
from ...player import SimplePlayer
from ...version import bot, team, author, YouTube

# TODO: make permission check for next, prev, stop, pause, lcear function
# TODO: get playlist info

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
        
    @cog_slash_managed(base='yt', description='查看頻道資訊')
    async def channel_info(self, ctx, channel_id: str=None):
        url = f"https://www.googleapis.com/youtube/v3/channels?key={YouTube['API_KEY']}&id={channel_id}&part=statistics"
        jsonText = requests.get(url).text
        statistics = json.loads(jsonText)['items'][0]['statistics']

        url = f"https://www.googleapis.com/youtube/v3/channels?key={YouTube['API_KEY']}&id={channel_id}&part=snippet"
        jsonText = requests.get(url).text
        snippet = json.loads(jsonText)['items'][0]['snippet']

        hiddenSubscriberCount = '是' if statistics['hiddenSubscriberCount'] == True else '否'

        embed=discord.Embed(title=snippet['title'], url=bot['url'], description=snippet['description'], color=0x00ffd5)
        embed.set_author(name=team['name'], url=bot['url'], icon_url=bot['icon'])
        embed.set_thumbnail(url=snippet['thumbnails']['high']['url'])
        embed.add_field(name='訂閱人數', value=statistics['subscriberCount'], inline=True)
        embed.add_field(name='觀看人數', value=statistics['viewCount'], inline=True)
        embed.add_field(name='影片數量', value=statistics['videoCount'], inline=True)
        embed.add_field(name='顯示訂閱', value=hiddenSubscriberCount, inline=True)
        embed.add_field(name='建立日期', value=snippet['publishedAt'], inline=True)
        # embed.add_field(name='國家地區', value=snippet['country'], inline=True)
        embed.add_field(name='頻道ID', value=channel_id, inline=True)
        embed.set_footer(text='技術提供: 靈萌團隊')
        await ctx.send(embed=embed)

    @cog_slash_managed(base='yt', description='查看影片資訊')
    async def video_info(self, ctx, video_id: str=None):
        url = f"https://www.googleapis.com/youtube/v3/videos?key={YouTube['API_KEY']}&id={video_id}&part=statistics"
        jsonText = requests.get(url).text
        statistics = json.loads(jsonText)['items'][0]['statistics']

        url = f"https://www.googleapis.com/youtube/v3/videos?key={YouTube['API_KEY']}&id={video_id}&part=snippet"
        jsonText = requests.get(url).text
        snippet = json.loads(jsonText)['items'][0]['snippet']

        embed=discord.Embed(title=snippet['title'], url=bot['url'], description=snippet['description'], color=0x00ffd5)
        embed.set_author(name=team['name'], url=bot['url'], icon_url=bot['icon'])
        embed.set_thumbnail(url=snippet['thumbnails']['high']['url'])
        embed.add_field(name='觀看次數', value=statistics['viewCount'], inline=True)
        embed.add_field(name='按讚人數', value=statistics['likeCount'], inline=True)
        embed.add_field(name='留言次數', value=statistics['commentCount'], inline=True)
        embed.add_field(name='上傳日期', value=snippet['publishedAt'], inline=True)
        embed.add_field(name='頻道標題', value=snippet['channelTitle'], inline=True)
        # embed.add_field(name='影片標籤', value=snippet['tags'], inline=True)
        # embed.add_field(name='預設語言', value=snippet['defaultLanguage'], inline=True)
        embed.add_field(name='影片ID', value=video_id, inline=True)
        embed.add_field(name='頻道ID', value=snippet['channelId'], inline=True)
        embed.set_footer(text='技術提供: 靈萌團隊')
        await ctx.send(embed=embed)

    # @cog_slash_managed(base='yt', description='查看播放清單資訊')
    # async def playlist_info(self, ctx, playlist_id):
    #     url = f"https://www.googleapis.com/youtube/v3/playlists?key={YouTube['API_KEY']}&id={playlist_id}&part=snippet"
    #     jsonText = requests.get(url)
    #     snippet = json.loads(jsonText)

    #     url = f"https://www.googleapis.com/youtube/v3/playlists?key={YouTube['API_KEY']}&id={playlist_id}&part=id,snippet&fields=items(id,snippet(title,channelId,channelTitle))"
    #     jsonText = requests.get(url)
    #     snippet = json.loads(jsonText)['items'][0]['snippet']

    #     embed=discord.Embed(title=snippet['title'], url=bot['url'], description=snippet['description'], color=0x00ffd5)
    #     embed.set_author(name=team['name'], url=bot['url'], icon_url=bot['icon'])
    #     embed.set_thumbnail(url=snippet['thumbnails']['high']['url'])
    #     embed.add_field(name='建立日期', value=snippet['publishedAt'], inline=True)
    #     embed.add_field(name='頻道標題', value=snippet['channelTitle'], inline=True)
    #     embed.add_field(name='頻道ID', value=snippet['channelId'], inline=True)
    #     embed.set_footer(text='技術提供: 靈萌團隊')
    #     await ctx.send(embed=embed)