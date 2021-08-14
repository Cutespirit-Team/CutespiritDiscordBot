import discord
from discord.ext import commands
from ..utils import cog_slash_managed

# TODO： make it more easily to change ( auto regist ?
# NOTE: outdated
class SlashHelp(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='幫助')
    async def help(self, ctx):
        usage = '''
            用法： /指令 [選項...] [參數...]
                一般：
                    /help 幫助
                    /sendmsg 次數 訊息 [選項] | 傳送訊息
                    /calc 函數 數字x 數字y | 計算機
                    /time current | 顯示時間
                    /time special_days_left | 倒數計時
                    /tw | Taiwan
                    /version | 版本
                    /about | 關於
                ArchLinux功能：
                    /pacman <操作> 套件 | Arch-pacman工具
                Dicord功能：
                    /status 文字 | 更改機器人狀態
                    /kick USER | 踢掉使用者
                    /ban USER | 封鎖使用者
                    /unban USER | 解封使用者
                YouTube音樂功能：
                    /yt play [URL] | 播放音樂
                    /yt pause | 暫停/恢復 播放音樂
                    /yt stop | 停止音樂
                    /yt next | 上一首
                    /yt prev | 下一首
                    /yt clear | 清除播放清單
                '''
        await ctx.send(usage)

