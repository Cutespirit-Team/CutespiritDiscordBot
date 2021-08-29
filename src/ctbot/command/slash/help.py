import discord
from discord.ext import commands
from ..utils import cog_slash_managed

# TODO： make it more easily to change ( auto regist ?
# NOTE: updated
class SlashHelp(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='幫助')
    async def help(self, ctx):
        usage = '''
            用法： /指令 [選項...] [參數...]
                一般：
                    /help 幫助
                    /sendmsg [訊息] [選項] | 傳送訊息
                    /clear [訊息數] | 清除訊息
                    /time current [選項] | 顯示時間
                    /time special_days_left | 特別日倒數計時
                    /calc [選項] [值] | 計算機
                    /tw | Taiwan
                    /weather [地區] | 顯示該地區天氣資訊
                    /version | 版本
                    /about | 關於
                ArchLinux功能：
                    /pacman pkg_files [套件] | 查詢 Arch 指令所屬套件
                    /pacman pkg_info [套件] | 查詢 Arch 套件資訊
                Dicord功能：
                    /status [狀態] | 更改機器人狀態
                    /kick [MEMBER] | 踢掉使用者
                    /ban [MEMBER] | 封鎖使用者
                    /unban [MEMBER] | 解封使用者
                YouTube音樂功能：
                    /yt play [URL] | 播放音樂
                    /yt pause [選項] | 暫停/恢復 播放音樂
                    /yt stop [選項] | 停止音樂
                    /yt next | 上一首
                    /yt prev | 下一首
                    /yt clear | 清除播放清單
                測試指令:
                    /ping | Ping-Pong
                '''
        await ctx.send(usage)

