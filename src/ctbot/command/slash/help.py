import discord
from discord.ext import commands
from ..utils import cog_slash_managed
from ...version import author, bot ,team

# TODO： make it more easily to change ( auto regist ?
# NOTE: updated
class SlashHelp(commands.Cog):
	def __init__(self, bot: discord.Client):
		self.bot = bot

	@cog_slash_managed(description='幫助')
	async def help(self, ctx):
		embed=discord.Embed(title=author['name'], url=author['url'], description='此為Cutespirit Discord Bot指令全集。\n用法： /指令 [選項...] [參數...]', color=0x00ffd5)
		embed.add_field(name='一般：', value='''
					/help 幫助
					/sendmsg [訊息] [選項] | 傳送訊息
					/clear [訊息數] | 清除訊息
					/time current [選項] | 顯示時間
					/time special_days_left | 特別日倒數計時
					/time remain_time_left | 今年已經過了多久百分比
					/calc [選項] [值] | 計算機
					/tw | Taiwan
					/weather [地區] | 顯示該地區天氣資訊
					/hardware | 查看本Bot運行硬體資訊
					/speedtest | 測試上傳與下載速度
					/about dcbot | 關於本機器人
					/about author | 關於作者
					/about team | 關於靈萌團隊
					/about version | 顯示版本
				''', inline=False)
		embed.add_field(name='ArchLinux功能：', value='''
					/pacman pkg_files [套件] | 查詢 Arch 指令所屬套件
					/pacman pkg_info [套件] | 查詢 Arch 套件資訊
				''', inline=False)
		embed.add_field(name='Dicord功能：', value='''
					/status [狀態] | 更改機器人狀態
					/kick [MEMBER] | 踢掉使用者
					/ban [MEMBER] | 封鎖使用者
					/unban [MEMBER] | 解封使用者
					/membercount | 查看伺服器人數
					/invite | 建立邀請連結
				''', inline=False)
		embed.add_field(name='服務客服單功能：', value='''
					/service open | 開啟服務客服單
					/service close [YN: boolean] | 關閉服務客服單
					/service delete [YN: boolean] | 刪除服務客服單
					/service manual | 查看服務客服單手冊
				''', inline=False)
		embed.add_field(name='YouTube音樂功能：', value='''
					/yt play [URL] | 播放音樂
					/yt pause [選項] | 暫停/恢復 播放音樂
					/yt stop [選項] | 停止音樂
					/yt next | 下一首
					/yt prev | 上一首
					/yt clear | 清除播放清單
				''', inline=False)
		embed.add_field(name='Cutespirit-SHOP功能', value='''
					/product_order [產品名稱] [價格] [Email] | 商品下單
					/check_order [訂單編號] | 查看訂單
				''', inline=False)
		embed.add_field(name='權限功能：', value='''
					/has_cmd_permission manage_message | 查看是否有管理訊息的權限
					/has_cmd_permission ban_user | 查看是否有ban使用者的權限
					/has_cmd_permission create_instant_invite | 查看是否有建立邀請連結的權限
				''', inline=False)
		embed.add_field(name='Github功能：', value='''
					/github_info | 查看Github資訊
					/github_visitor | 增加Github訪客人數
				''', inline=False)
		embed.add_field(name='測試指令', value='''
					/ping | Ping-Pong
				''', inline=False)
		embed.set_footer(text='更新日期')
		await ctx.send(embed=embed)