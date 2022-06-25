import discord
from discord.ext import commands
from ..utils import cog_slash_managed
from ...version import author, bot ,team

# TODO： make it more easily to change ( auto regist ?
# NOTE: updated
class SlashHelp(commands.Cog):
	def __init__(self, bot: discord.Client):
		self.bot = bot

	@cog_slash_managed(base="help", description='幫助')
	async def cmd(self, ctx):
		embed=discord.Embed(title=author['name'], url=author['url'], description='此為Cutespirit Discord Bot指令全集。\n用法： /指令 [選項...] [參數...]', color=0x00ffd5)
		embed.add_field(name='一般：', value='''
					/help cmd 查看指令幫助
					/help QandA 查看疑難排解
					/sendmsg [訊息] [選項] | 傳送訊息
					/clear [訊息數] | 清除訊息
					/time current [選項] | 顯示時間
					/time special_days_left | 特別日倒數計時
					/time remain_time_left | 今年已經過了多久百分比
					/calc [選項] [值] | 計算機
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
					/status [狀態] [訊息] | 更改機器人狀態
					/kick [MEMBER] | 踢掉使用者
					/ban [MEMBER] | 封鎖使用者
					/unban [MEMBER] | 解封使用者
					/server_state | 查看伺服器資訊
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
					/yt channel_info [channel_id] | 得到頻道資訊
					/yt video_info [video_id] | 得到影片資訊
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
		embed.add_field(name='股票功能', value='''
					/stock show [data: str (YYYYMMDD)] [CODE: str]| Ping-Pong
				''', inline=False)
		embed.add_field(name='測試指令', value='''
					/ping | Ping-Pong
					/reload | 重新載入已註冊的斜線指令
				''', inline=False)
		await ctx.send(embed=embed)

	@cog_slash_managed(base="help", description='問題排解')
	async def QandA(self, ctx):
		embed=discord.Embed(title=author['name'], url=author['url'], description='此為Cutespirit Discord Bot疑難排解', color=0x00ffd5)
		embed.add_field(name='電腦出現沒指令而手機有該怎麼辦？', value='''
	別擔心，這是Discord出的錯，請靜待至一兩個小時。如還是沒有，請進入重新邀請機器人，可以使用/invite指令。
		''', inline=False)
		embed.add_field(name='當我遇到bug該如何處理？', value='''
	別擔心，請將bug資訊寄信至 service@cutespirit.org
		''', inline=False)
		embed.add_field(name='當我遇到YouTube影片無法播放的時候該怎麼辦？', value='''
	一、自行架設：
		請更新機器人至最新版本，或在github提出issue。
	二、使用官方：
		請回報至 service@cutespirit.org或在github提出issue。
		''', inline=False)
		embed.add_field(name='當我有指令出不來時該怎麼辦？', value='''
	一、自行架設：
		請檢查您是否有改寫程式碼，如果有請再三確認您的程式碼。或是將程式碼更新到最新版本。
	二、使用官方：
		請靜置10分鐘，或是重新邀請機器人，可以使用/invite指令，如果還是沒有請回報。
		''', inline=False)
		embed.add_field(name='有功能不完善怎麼辦？', value='''
	一、您可以改寫程式碼並發布Pull Requests。
	二、您可以在Github中提出Issue。
	三、您可以將您的建議提供至 service@cutespirit.org。
	四、您可善用團隊資源回報。
		''', inline=False)
		embed.add_field(name='靈萌discord機器人會收集您的指令和資料嗎？', value='''
	靈萌Discord機器人不會蒐集您的資料和您打得文字，靈萌Discord機器人是開源的，可受人檢視，任何人都可以提出問題和Pull Requests。
		''', inline=False)
		embed.add_field(name='如何進行發問？', value='''
	一、請留下您的Email信箱或Discord ID等聯繫方式以便我們連繫您。
	二、請簡明扼要說明您的敘述。
	三、請保持禮貌。
	四、請善用圖片(URL)
		''', inline=False)
		await ctx.send(embed=embed)

	@cog_slash_managed(base="help", description='Bug和問題客服和上報')
	async def report(self, ctx, msg: str):
		# TODO: Send msg to Admin
		await ctx.send('Function not finished')