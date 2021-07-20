import discord
import os
import subprocess
from pprint import pprint	#這是print的加強版 可以讓文字自動排版
from datetime import datetime	#一樣處理時間
from datetime import datetime #這是時間
from datetime import timedelta 
from datetime import date #時間
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from discord_slash import SlashCommand , SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from youtube_dl import YoutubeDL
import math #數學
import time	#可以處理時間

#設定檔:
	#Bot的Token 沒有的要去 t.me/BotFather申請
TOKEN = 'Your Token Here'
idDebug = False
    #參數設定
capCountDown111text = "2022/06/04 08:30 AM" #111會考日期文字
capCountDown111 = datetime(2022,6,4,8,30)#111會考日期

tcteCountDown111text = "2022/05/07 10:15 AM" #111統測日期文字
tcteCountDown111 = datetime(2022,5,7,10,15) #111統測日期

ceecCountDown111text = "2022/05/15 09:20 AM" #111學測日期文字
ceecCountDown111 = datetime(2022,1,15,9,20) #111學測日期

TershiBirthday18text = "2022/05/26" #夏特稀111生日文字
TershiBirthday18 = datetime(2022,5,26,0,0) #夏特稀111生日


YahooStoptext = "2021/05/04" #Yahoo停止日文字
YahooStop = datetime(2021,5,4) #Yahoo停止日

client = commands.Bot(command_prefix='/')
slash = SlashCommand(client, sync_commands=True)
yt_players = {}
guild_ids=[866199579014987816]

def getCount(deadline): #把deadline(過期 就是到期) 放進來
	#today = date.today() #現在日期
	#CurrentToday = today.strftime("%Y") + "," + today.strftime("%m") + "," + today.strftime("%d") #現在日期格式
	if (deadline-datetime.now()).days/365 >=1: #如果到期日-今天 還有365天 就True
		return str((deadline-datetime.now()).days//365)+ '年' + str((deadline-datetime.now()).days%365) + '天' + str((deadline-datetime.now()).seconds//3600) + '小時' + str(((deadline-datetime.now()).seconds//60)%60) + '分鐘' #加入年
	return str((deadline-datetime.now()).days) + '天' + str((deadline-datetime.now()).seconds//3600) + '小時' + str(((deadline-datetime.now()).seconds//60)%60) + '分鐘'

def getExamCountText():
	text  = '中華帝國年行事曆\n\n'
	text += '=====111年=====\n'
	text += str(TershiBirthday18text) + '夏特稀皇帝18歲誕辰倒數' + str(getCount(TershiBirthday18)) + '\n'
	text += str(capCountDown111text) + '會考倒數：' + str(getCount(capCountDown111)) + '\n'
	text += str(tcteCountDown111text) + '學測倒數：' + str(getCount(tcteCountDown111)) + '\n'
	text += str(ceecCountDown111text) + '統測倒數：' + str(getCount(ceecCountDown111)) + '\n'
	text += '\n各位中華帝國的子民的，有什麼需要倒數的，或是日程，可以與 @TershiXia聯絡喔！\n'
	text += '111會考生: @拉拉拉拉 \n'
	text += '111學測升: @拉拉拉拉 \n'
	text += "111統測生: @拉拉拉拉 \n"
	return text

#class MyClient(discord.Client):
@client.event
async def on_ready():
	print('登入成功')
	print('------')

@client.event
async def on_member_join(self, member):
	guild = member.guild
	if guild.system_channel is not None:
		to_send = f'Welcome {member.mention} to {guild.name}!'
		await guild.system_channel.send(to_send)
		print('{member.mention} has joined the group')

@slash.slash(
	name="clear",
	description="用於清除(收回)頻道內之訊息數",
	guild_ids=guild_ids
)
#@client.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx:SlashContext ,num:int, cmd=None):
	if cmd =='--help':
		await ctx.send('''
		用法： /clear 訊息數
		變數：
			訊息數: int
		說明：
			用於清除(收回)頻道內之訊息數
			''')
	else:
		print('cleared')
		await ctx.channel.purge(limit=num+1)
		await ctx.send('刪除成功')
		print('The Channel Text have been cleared successfully!')

@slash.slash(
	name="kick",
	description="用於踢出在伺服器中的使用者",
	guild_ids=guild_ids
)
#@client.command(name='kick')
@commands.has_permissions(manage_messages=True)
async def kick(ctx, member : discord.Member, *,reason=None, cmd=None):
	if cmd =='--help':
		await ctx.send('''
		用法： /kick USER
		變數：
			USER: String
		說明：
			用於踢出在伺服器中的使用者
			''')
	else:
		await member.kick(reason=reason)
		await message.channel.send('已成功踢掉{discord.Member}！')
		print('{discord.Member} has been kicked successfully!')

@slash.slash(
	name="ban",
	description="用於封鎖尚未封鎖的使用者",
	guild_ids=guild_ids
)
#@client.command(name='ban')
@commands.has_permissions(manage_messages=True)
async def ban(ctx, member:discord.Member , *, reason=None, cmd=None):
	if cmd =='--help':
		await ctx.send('''
		用法： /ban USER
		變數：
			USER: String
		說明：
			用於封鎖尚未封鎖的使用者
			''')
	else:
		await member.ban(reason=reason)
		await message.channel.send('已成功ban {discord.Member}！')
		print('{discord.Member} has been banned successfully!')

@slash.slash(
	name="unban",
	description="用於解封已經被封鎖的使用者",
	guild_ids=guild_ids
)
#@client.command(name='unban')
@commands.has_permissions(manage_messages=True)
async def unban(ctx , * , member, cmd=None):
	if cmd =='--help':
		await ctx.send('''
		用法： /unban USER
		變數：
			USER: String
		說明：
			用於解封已經被封鎖的使用者
			''')
	else:
		banned_users = await ctx.guild.bans()
		member_name, member_discriminator = member.split('#')
		for ban_entry in banned_users:
			user = ban_entry.user
			if (user.name, user.discriminator) == (member_name, member_discriminator):
				await ctx.guild.unban(user)
				await ctx.send(f'Unbanned {user.mention}')
				return
				await message.channel.send('已成功解封{discord.Member}！')
				print('{discord.Member} has been unbanned successfully!')

@slash.slash(
	name="join",
	description="用於加入訊息發送者所屬的語音頻道",
	guild_ids=guild_ids
)
#@client.command(pass_context=True)
async def join(ctx, cmd=None):
	if cmd =='--help':
		await ctx.send('''
		用法： /join
		說明：
			用於加入訊息發送者所屬的語音頻道
			''')
	else:
		channel = ctx.author.voice.channel
		await channel.connect()
		await ctx.send('Connected!')
		print('Send Text: Connected!')
		print('Bot: Connected to the Voice Channel')

@slash.slash(
	name="leave",
	description="用於離開Bot所屬的語音頻道",
	guild_ids=guild_ids
)
#@client.command(pass_context=True)
async def leave(ctx, cmd=None):
	if cmd =='--help':
		await ctx.send('''
		用法： /leave
		說明：
			用於離開Bot所屬的語音頻道
			''')
	else:
		if (ctx.voice_client): # If the bot is in a voice channel 
			await ctx.guild.voice_client.disconnect() # Leave the channel
			await ctx.send('Bot left')
			print('Bot: The Bot left the Voice Channel')
		else: # But if it isn't
			await ctx.send("I'm not in a voice channel, use the join command to make me join")
			print('Bot: Not in Voice Channel')
			print("Send Text: I'm not in a voice channel, use the join command to make me join")

@slash.slash(
	name="play",
	description="用於播放YouTube影片or音樂音量",
	guild_ids=guild_ids
)
#@client.command(pass_context=True)
async def play(ctx, url, cmd=None):
	if cmd =='--help':
		await ctx.send('''
		用法： /play URL
		變數：
			URL: String
		說明：
			用於播放YouTube影片or音樂音量。
			''')
	else:
		YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
		FFMPEG_OPTIONS = {
			'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
		voice = get(client.voice_clients, guild=ctx.guild)

		if not voice.is_playing():
			with YoutubeDL(YDL_OPTIONS) as ydl:
				info = ydl.extract_info(url, download=False)
			URL = info['url']
			voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
			voice.is_playing()
			await ctx.send('playing')
			print('Bot: Playing the Audio')
			print("Send Text: playing")
		else:
			await ctx.send('There is no Audio playing now')
			print('Bot: There is no Audio playing now')
			print("Send Text: There is no Audio playing now")

@slash.slash(
	name="resume",
	description="用於暫停播放正在播放的YouTube影片or音樂音量",
	guild_ids=guild_ids
)
#@client.command()
async def resume(ctx, cmd=None):
	if cmd =='--help':
		await ctx.send('''
		用法： /resume
		說明：
			用於暫停播放正在播放的YouTube影片or音樂音量。
			''')
	else:
		voice = get(client.voice_clients, guild=ctx.guild)
		if not voice.is_playing():
			voice.resume()
			await ctx.send('resuming')
			print('Bot: Resuming The Audio')
			print("Send Text: resuming")
		else:
			await ctx.send('There is no Audio playing now')
			print('Bot: There is no Audio playing now')
			print("Send Text: There is no Audio playing now")

@slash.slash(
	name="volume",
	description="用於修改YouTube影片or音樂音量",
	guild_ids=guild_ids
)
#@client.command(name="volume")                          
async def volume(ctx, volume: float, cmd=None):
	if cmd =='--help':
		await ctx.send('''
		用法： /volume 音量
		變數：
			音量: int
		說明：
			用於修改YouTube影片or音樂音量。
			''')
	else:
		voice = get(client.voice_clients, guild=ctx.guild)  
		if 0 <= volume <= 100:
			if voice.is_playing():
				new_volume = volume / 100
				voice.source .volume = new_volume
				print('Bot: set volume =',new_volume)
			else:
				await ctx.reply("#")
		else:
			await ctx.reply("#")
		await ctx.reply(f"Volume: {volume}")

@slash.slash(
	name="pause",
	description="用於暫停播放正在播放的YouTube影片or音樂。",
	guild_ids=guild_ids
)
#@client.command()
async def pause(ctx, cmd=None):
	if cmd =='--help':
		await ctx.send('''
		用法： /pause
		說明：
			用於暫停播放正在播放的YouTube影片or音樂。
			''')
	else:
		voice = get(client.voice_clients, guild=ctx.guild)
		if voice.is_playing():
			voice.pause()
			await ctx.send('paused')
			print('Bot: Audio is paused')
			print('Send Text: paused')
		else:
			await ctx.send('There is no Audio playing now')
			print('Bot: There is no Audio playing now')
			print("Send Text: There is no Audio playing now")

@slash.slash(
	name="stop",
	description="用於停止播放YouTube影片or音樂。",
	guild_ids=guild_ids
)
#@client.command()
async def stop(ctx ,cmd=None):
	if cmd =='--help':
		await ctx.send('''
		用法： /stop
		說明：
			用於停止播放YouTube影片or音樂。
			''')
	else:
		voice = get(client.voice_clients, guild=ctx.guild)
		if voice.is_playing():
			voice.stop()
			await ctx.send('Stopping...')
			print('Bot: Stopping The Audio')
			print("Send Text: Stopping...")
		else:
			await ctx.send('There is no Audio playing now')
			print('Bot: There is no Audio playing now')
			print("Send Text: There is no Audio playing now")

@slash.slash(
	name="updateinfo",
	description="此命令可查看更新內容",
	guild_ids=guild_ids
)
async def updateinfo(ctx):
	#if message.content == '/更新內容' or message.content == '/updateinfo' or '/updateinfo' in message.content:
	await ctx.send('''
		更新日期   - 版本 - 更新內容
		2021/07/19 - v0.1 - 初始版本(由TershiCloud Telegram Bot修改)
		2021/07/19 - v0.2 - 增加/status指令，可以隨時更改Discord狀態，刪除lang語言功能。
		2021/07/20 - v0.3 - 增加/kick /ban /unban指令，可以隨時踢人，封鎖，解封人。
		2021/07/20 - v0.4 - 將/time --help顯示/week問題修復。
		2021/07/20 - v0.5 - 完善各--help幫助內容。
		2021/07/20 - v0.6 - 修復Bug。
		2021/07/20 - v0.7 - 並加入YouTube之/join /play /pause /resume /stop /leave功能。
		''')

@slash.slash(
	name="version",
	description="此命令可查看版本",
	guild_ids=guild_ids
)
async def version(ctx):
	#if message.content == '/更新內容' or message.content == '/version' or '/version' in message.content:
	await ctx.send('目前版本：1.4.1')

@client.command(name='status')
async def status(ctx, STATUS: str):
	# tmp = message.content.split(' ')
	# text = ''
	# for i in range(1,len(tmp)):
	# 	text = text + str(tmp[i])
	# game = discord.Game(text)
	game = discord.Game(STATUS)
	await client.change_presence(status=discord.Status.idle, activity=game)
	await client.process_commands(message)
	await ctx.send('將狀態更改為:' + message)
	print('將狀態更改為:' + message)

@slash.slash(
	name="help",
	description="幫助",
	guild_ids=guild_ids
)
#if message.content == '幫助' or message.content == 'help' or '/help' in  message.content:	
#or兩方有一個為True就成立(邏輯運算子) 最後一個in的語法是 只要"/help"有在傳來的訊息裡面就True
async def help(ctx):
	text = '''
用法： /指令 [選項...] [參數...]
	一般：
		/help 顯示幫助
		/sendmsg 次數 訊息 [選項] | 傳送訊息 --help可以查看幫助
		/calc 數字x 數字y [選項] | 計算機 --help可以查看幫助
		/time [選項] | 顯示時間 --help可以查看幫助
		/count | 倒數計時
		/weareroc | 我們是中國(中華民國)
		/showweb | 顯示官網
		/updateinfo | 查看更新內容
		/version | 顯示版本
	ArchLinux功能：
		/pacman <操作> 套件 | Arch-pacman工具 --help可以查看幫助
		/pkg 套件 | Arch套件查詢資訊工具 --help可以查看幫助
		/cmd 指令 | Arch指令尋找所屬套件 --help可以查看幫助
	Dicord功能：	
		/status 文字 | 更改Discord 機器人狀態
		/kick USER | 踢掉使用者
		/ban USER | 封鎖使用者
		/unban USER | 解封使用者
	YouTube音樂功能：
		/join | 加入到語音頻道
		/play URL | 播放YouTube音樂
		/pause | 暫停播放YouTube音樂
		/resume | 恢復播放YouTube音樂
		/stop | 停止播放YouTube音樂
			'''
			#三個單引號或雙引號可以多行當字串
	await ctx.send(text) #調用傳送訊息的方法 將聊天室的(id傳出去,文字傳出去)



@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		return
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Missing a required argument.  Do /help")
		print('Bot:Missing a required argument.  Do /help')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send("You dont have the permissions to run this command.")
		print('You dont have the permissions to run this command.')
	if isinstance(error, commands.BotMissingPermissions):
		await ctx.send("I don't have permissions to do it!")
		print("I don't have permissions to do it!")
	else:
		print("error not caught")
		print(error) 

@client.event
async def on_message(message):
	# don't respond to ourselves
	if message.author == client.user:
		return
	if message.content == '顯示網站' or '/showweb' in message.content:
		text = '''
1. 靈萌官網 - https://cutespirit.tershi.cf
2. 夏特稀雲端硬碟 - https://mail.tershi.cf/tershicloud
3. 夏特稀郵件 - https://mail.tershi.cf
4. 愛神閃靈團隊官網 - https://www.tershi.cf
5. 夏特稀YT - https://www.youtube.com/夏特稀
6. Bot Source Code: https://github.com/mmm25002500/TershiBot-Telegram
夏特稀TG - t.me/TershiXia
本Bot - t.me/@TershiCloudBot
隱私權政策 - https://mail.tershi.cf/policy
本Bot 是夏特稀製作
			'''
		await message.channel.send(text)
	if message.content == '/倒數' or message.content == '/count' or '/count' in message.content:
		await message.channel.send(getExamCountText())
		print('Bot:' + getExamCountText())
	if message.content == '/我們是中國' or message.content == '/weareroc' or '/weareroc' in message.content:
		await message.channel.send('''中華民國萬歲，三民主義統一中國，我們是自由民主中國。''')
		print('Bot:' + '''中華民國萬歲，三民主義統一中國，我們是自由民主中國。''')
	if message.content == '/傳送' or message.content == '/sendmsg' or '/sendmsg' in message.content:
		text = str(message.content) #取得訊息 並放入text裡面
		numbers = [int(temp)for temp in text.split() if temp.isdigit()] #將有出現數字的 放入numbers裡面
		text = text.split() #將text 依照空格切割
		if numbers == []: #如果numbers為空
			if '--help' in text or ' —help' in text: #如果--help在text串列裡面
				await message.channel.send('''
				用法： /sendmsg 次數 訊息 [選項]
				變數：
					次數: int
					訊息: String
					秒: int
				選項：
				--count | 計數器 用來顯示字串+x索引值
				--sleep 秒 | 間隔秒數 每次執行間隔x秒 間隔 0<=x<=10
				--help | 顯示幫助
				''')
			else:
				await message.channel.send('請輸入該有參數 /sendmsg 次數 訊息 [選項] 使用--help可以查看幫助')
		else:
			text.remove(str(numbers[0])) #text串列刪除數字
			temp = text[:] #將text放入temp
			tempS = 0
			if '--sleep' in text or '—sleep' in text:
					tempS = 1
					if numbers[-1] >10:
						await message.channel.send('輸入的時間太長了喔 介於0~10之間')
						tempS = 0
					elif  numbers[-1] <0:
						await message.channel.send('輸入的時間太短了喔 介於0~10之間')
						tempS = 0
			if '--count' in text or '—count' in text: #如果--count在text裡面
				if '--count' in text:
					temp.remove('--count') #temp刪掉--help
				elif '—count' in text:
					temp.remove('—count') #temp刪掉—help
				try:
					for i in range(0,numbers[0]):
						if tempS == 1:
							time.sleep(numbers[-1])
						await message.channel.send(temp[1] + 'x' + str(i+1))
				except IndexError:
						await message.channel.send('可能有哪裡錯誤了 IndexError')
			#elif 參數 in text: 自己新增
			else: #如果--count不在裡面
				print(text)
				for i in range(0,numbers[0]):
					if tempS == 1:
						time.sleep(numbers[-1])
					await message.channel.send(text[1])
	if message.content == '/計算' or message.content == '/calc' or '/calc' in message.content:
		text = str(message.content) #將訊息提取至text
		numbers = [int(temp)for temp in text.split() if temp.isdigit()] #取得數字
		text = text.split() #進行空格切割
		if '--root' in text or '—root' in text:
			result = math.sqrt(numbers[0])
			await message.channel.send(result)
		elif '--fact' in text or '—fact' in text:
			result = math.factorial(numbers[0])
			await message.channel.send(result)
		elif '--fabs' in text or '—fabs' in text:
			result = math.fabs(numbers[0])
			await message.channel.send(result)
		elif '--pow' in text or '—pow' in text:
			result = math.pow(numbers[0], numbers[1])
			await message.channel.send(result)
		elif '--cos' in text or '—cos' in text:
			result = math.cos(numbers[0])
			await message.channel.send(result)
		elif '--sin' in text or '—sin' in text:
			result = math.sin(numbers[0])
			await message.channel.send(result)
		elif '--tan' in text or '—tan' in text:
			result = math.tan(numbers[0])
			await message.channel.send(result)
		elif '--degrees' in text or '—degrees' in text:
			result = math.degrees(numbers[0])
			await message.channel.send(result)
		elif '--radians' in text or '—radians' in text:
			result = math.radians(numbers[0])
			await message.channel.send(result)
		elif '--linearEqSo' in text or '—linearEqSo' in text:
			a = numbers[0]
			b = numbers[1]
			c = numbers[2]
			x1 = 0
			x2 = 0
			result = ''
			if b**2-4*a*c > 0:
				x1=((-b+math.sqrt(b**2-4*a*c))/(2*a))
				x2=((-b-math.sqrt(b**2-4*a*c))/(2*a))
				result = '有兩根實數解/兩根 x1=' +str(x1), 'x2=' + str(x2)
			elif b**2 -4*a*c ==0:
				result = '重根'
			elif b**2 - 4*a*c <0:
				result = '無實數根之解/無根'
			await message.channel.send(result)
		elif '--bmi' in text or '—bmi' in text:
			try:
				w = numbers[0] #可能出錯 如果沒有數字的話
				h = numbers[1]
				bmi = w / (h/100)**2
			except IndexError: #沒有數字會出現Index Out Of Range
				await message.channel.send('可能有哪裡出錯了喔:Index Out Of Range')
			if '--check' in text or '—check' in text:
				if bmi >= 35:
					Ctext = '過重'
				elif bmi >= 30:
					Ctext = '中度肥胖'
				elif bmi >=27:
					Ctext = '輕度肥胖'
				elif bmi >=24:
					Ctext = '過重'
				elif bmi >=18.5:
					Ctext = '正常範圍'
				elif bmi <18.5:
					Ctext = '體重過輕'
				await message.channel.send(Ctext + ' BMI=' + str(bmi))
			elif '--help' in text or '—help' in text:
				await message.channel.send('''
				用法： /calc --bmi [選項]
				選項：
				--check 顯示是否過重或是過輕
				--help 顯示幫助
				''')
			else:
				await message.channel.send(bmi)
		elif '+' in text:
			result = numbers[0] + numbers[1]
			print(result)
			await message.channel.send(str(result))
		elif '-' in text:
			result = numbers[0] - numbers[1]
			await message.channel.send(str(result))
		elif '*' in text:
			result = numbers[0] * numbers[1]
			await message.channel.send(str(result))
		elif '/' in text:
			if numbers[1] == 0:
				await message.channel.send('第二個參數請勿放0')
			else:
				result = numbers[0] / numbers[1]
				await message.channel.send(str(result))
		elif '--help' in text or '—help' in text:
			text = '''
			用法： /calc [選項] [參數]
			選項：
			+ 數字x 數字y | 加
			- 數字x 數字y | 減
			* 數字x 數字y | 乘 
			/ 數字x 數字y | 除
			--root 數字x | 返回 x 的平方根。
			--fact 數字x | 以一個整數返回 x 的階乘。
			--fabs 數字x | 返回 x 的絕對值
			--pow  數字x 數字y | 返回 x 的 y 次方
			--cos 數字x | 返回 x 弧度的m餘弦值。
			--sin 數字x | 返回 x 弧度的正弦值。
			--tan 數字x | 返回 x 弧度的正切值。
			--degrees 數字x | 將角度 x 從弧度轉換為度數。
			--radians 數字x | 將角度 x 從度數轉換為弧度。
			--linearEqSo 數字a 數字b 數字c | 取得兩根/重根/無根
			--bmi 體重w(公斤) 身高h(公分) | 取得bmi之值 --help 取得幫助
			--help 顯示幫助
			'''
			await message.channel.send(text)
	
	if message.content == '/時間' or message.content == '/time' or '/time' in message.content:
		today = datetime.now() #取得現在時間
		text = str(message.content) #將輸入的指令放入text
		nowtime = '現在時間：'
		counter= 0 #計數器為0
		if '--year' in text or '—year' in text: #依照指令需要進行累加，並且計數器設定為1
			nowtime += today.strftime("%Y") + '年'
			counter=1
		if '--month'in text or '—month'in text: #依照指令需要進行累加，並且計數器設定為1
			nowtime += today.strftime("%m") + '月'
			counter=1
		if '--date'in text or '—date'in text: #依照指令需要進行累加，並且計數器設定為1
			nowtime += today.strftime("%d") + '日'
			counter=1
		if '--hour'in text or '—hour'in text: #依照指令需要進行累加，並且計數器設定為1
			nowtime += today.strftime("%H") + '時'
			counter=1
		if '--minute'in text or '—minute'in text: #依照指令需要進行累加，並且計數器設定為1
			nowtime += today.strftime("%M") + '分'
			counter=1
		if '--second'in text or '—second'in text: #依照指令需要進行累加，並且計數器設定為1
			nowtime += today.strftime("%S") + '秒'
			counter=1
		if '--week'in text or '—week'in text: #依照指令需要進行累加，並且計數器設定為1
			if today.strftime("%A") == 'Monday':
				nowtime += '星期一'
			elif today.strftime("%A") == 'Tuesday':
				nowtime += '星期二'
			elif today.strftime("%A") == 'Wednesday':
				nowtime += '星期三'
			elif today.strftime("%A") == 'Thursday':
				nowtime += '星期四'
			elif today.strftime("%A") == 'Friday':
				nowtime += '星期五'
			elif today.strftime("%A") == 'Saturday':
				nowtime += '星期六'
			elif today.strftime("%A") == 'Sunday':
				nowtime += '星期日'
			counter=1
		if '--help' in text or '—help' in text: #如果有輸入--help
			text = '''
			用法： /week [選項]
			選項：
			--year | 取得年份
			--month | 取得月份
			--date | 取得日期
			--hour | 取得小時
			--minute | 取得分鐘
			--secound | 取得秒數
			--week | 取得星期幾
			--help | 顯示幫助
			'''
			await message.channel.send(text)
		elif counter == 1: #如果沒有輸入--help 並且count是1
			await message.channel.send(nowtime)
		else: #如果只有/time
			nowtime = '現在時間：' + today.strftime("%Y") + '年'+ today.strftime("%m") +'月' +today.strftime("%d") + '日' + today.strftime("%H") + '時' +today.strftime("%M") + '分' + today.strftime("%S") + '秒' 
			await message.channel.send(nowtime)
	
	if message.content == '/pacman'  or '/pacman' in message.content:
		text = str(message.content) #將文字放進來 轉成字串
		text = text.split() #將文字以空格切割
		if '--help' in text or '—help' in text or '-h' in text:
			await message.channel.send('''
		用法:  pacman <操作> 套件
		變數：
			套件: String
		操作：
			-h 幫助
			-V 版本
			-F 檔案 [選項] [檔案]
			-Ss搜尋 [選項] [檔案]
			-Q 佇列 [選項] [軟體包]
			-Qi資訊	[選項] <檔案>
		說明：
			此命令可執行某個pacman操作，使用 'pacman {-h --help}' 及某個操作以查看可用選項
			''')
		elif '-S' not in text or '--sync' not in text or '-Syy' not in text or '-Sy' not in text or '-U' not in text or '--upgrade' not in text or '--upgrade' not in text:
			temp = 'pacman ' #設定temp變數
			for i in range(1,len(text[:])): #/command後面的字
				temp += text[i] + ' ' #放進來
			result = os.popen(temp) #將/command後面的指令執行
			txt = temp
			output = subprocess.getstatusoutput(temp) #執行結果
			txt += output[1] #[0,輸出指令] 將0排除
			await message.channel.send(txt)

@slash.slash(
	name="pkg",
	description="此命令可查找Arch Repo的套件資訊",
	guild_ids=guild_ids
)
async def pkg(ctx, pkg: str):
#if message.content == '/套件' or message.content == '/pkg' or '/pkg' in message.content:
#	text = str(message.content) #將文字放進來 轉成字串
#	if '--help' in text or '—help' in text or '-h' in text:
	if pkg == '--help':
		await ctx.send('''
	用法： /pkg 套件
	變數：
		套件: String
	說明：
		此命令可查找Arch Repo的套件資訊，Repo有「core、community、extra、archlinuxcn、blackarch」
		''')
	else:
#		text = text.split() #將文字以空格切割
		await ctx.send('正在尋找該套件之資訊...請稍後...')

#		temp = 'pacman -Si ' #設定temp變數
#		for i in range(1,len(text[:])): #/command後面的字
#			temp += text[i] + ' ' #放進來
		temp = 'pacman -Si ' + pkg
		result = os.popen(temp) #將/command後面的指令執行
		txt = temp
		output = subprocess.getstatusoutput(temp) #執行結果
		txt += output[1] #[0,輸出指令] 將0排除
		await ctx.send(txt)
	

@slash.slash(
	name="cmd",
	description="此命令可查找Arch 指令所屬套件",
	guild_ids=guild_ids
)
async def cmd(ctx, pkg: str):
	#text = str(message.content) #將文字放進來 轉成字串
	#if '--help' in text or '—help' in text or '-h' in text:
	if str == '--help':
		await ctx.send('''
	用法： /cmd 套件
	變數：
		套件: String
	說明：
		此命令可查找Arch 指令所屬套件，Repo有「core、community、extra、archlinuxcn、blackarch」
		''')
	else:
		await ctx.send('正在尋找該指令所屬的套件...請稍後...')
		# text = text.split() #將文字以空格切割
		# temp = 'pacman -F ' #設定temp變數
		# for i in range(1,len(text[:])): #/command後面的字
			# temp += text[i] + ' ' #放進來
		temp = 'pacman -F ' + pkg
		result = os.popen(temp) #將/command後面的指令執行
		txt = temp
		output = subprocess.getstatusoutput(temp) #執行結果
		txt += output[1] #[0,輸出指令] 將0排除
		txt = txt.split('\n')
		for i in range(0,len(txt)):
			if '錯誤' in txt[i]:
				txt[i] = ''
		finaltxt = ''
		for i in range(0,len(txt)):
			#print(txt[i])
			finaltxt = finaltxt + str(txt[i]) + '\n'
		await ctx.send(finaltxt)

	#discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
#intents = discord.Intents.default()
#intents.members = True
#client = MyClient()
client.run(TOKEN) #TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面
