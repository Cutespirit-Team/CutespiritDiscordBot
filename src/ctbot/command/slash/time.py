import discord
import argparse
import json
from discord.ext import commands
from datetime import datetime
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType
from ..utils import cog_slash_managed, gen_list_of_option_choices

date_format = '%Y/%m/%d'
datetime_format = '%Y/%m/%d %H:%M'

def get_days_left(deadline, format=None):
	if type(deadline) == str:
		deadline = datetime.strptime(deadline, format)

	if (deadline - datetime.now()).days/365 >=1: #如果到期日-今天 還有365天
		return str((deadline-datetime.now()).days//365) + '年' \
			 + str((deadline-datetime.now()).days%365) + '天' \
			 + str((deadline-datetime.now()).seconds//3600) + '小時' \
			 + str(((deadline-datetime.now()).seconds//60)%60) + '分鐘' #加入年
	return str((deadline-datetime.now()).days) + '天' + str((deadline-datetime.now()).seconds//3600) + '小時' + str(((deadline-datetime.now()).seconds//60)%60) + '分鐘'

def get_special_days_left():
	try:
		timeLabel = open('config/timeLabel.json', mode='r', encoding='utf-8')
		timeLabel = json.load(timeLabel)
		text = ''
		for i in timeLabel.keys():
			text += f'{timeLabel[i]} {i} {get_days_left(timeLabel[i], date_format)}\n'
		return text
	except FileNotFoundError:
		filename = 'config/timeLeftLabel.json'
		content = {
			'My Birthday' : '2022/12/01',
			'Example Day' : 'YYYY/MM/DD'
		}
		f = open(filename, 'w')
		json.dump(content, f, indent=4)
		f.close()

def get_remain_time(year, month, day, hour, minute, second):
	d1 = datetime(year,1,1)
	d2 = datetime(year,month,day)
	remain_day = d2 - d1
	remain_time = ((remain_day.days *24 + hour)*60+minute)*60+second
	remain_time = remain_time / 31536000
	remain_time = "%.2f%%" % (remain_time * 100)
	return remain_time

class SlashTime(commands.Cog):
	def __init__(self, client: discord.Client):
		parser = argparse.ArgumentParser(exit_on_error=False, add_help=False)
		parser.add_argument('--year', action='store_true', default=False)
		parser.add_argument('--month', '--mon', action='store_true', default=False)
		parser.add_argument('--day', action='store_true', default=False)
		parser.add_argument('--hour', action='store_true', default=False)
		parser.add_argument('--minute', '--min', action='store_true', default=False)
		parser.add_argument('--second', '--sec', action='store_true', default=False)
		parser.add_argument('--week', action='store_true', default=False)
		parser.add_argument('--date', action='store_true', default=False)
		parser.add_argument('--time', action='store_true', default=False)
		parser.add_argument('--datetime', action='store_true', default=False)
		parser.add_argument('unused', nargs='*')
		self.parser = parser

	@cog_slash_managed(base='time', description='特別日倒數計時')
	async def special_days_left(self, ctx):
		await ctx.send(get_special_days_left())
	
	@cog_slash_managed(base='time', description='今年已經過了多少百分比',
				options=[create_option('format', '格式',
				option_type=SlashCommandOptionType.STRING,
				required=False,
				choices=gen_list_of_option_choices(['西元','民國']))])
	async def remain_time_left(self, ctx, format=None):
		today = datetime.now()
		year, month, day, hour, minute, second, week = today.timetuple()[:7]
		remain_time = get_remain_time(year, month, day, hour, minute, second)
		if '民國' in str(format):
			year = year - 1911
		text = str(year) + '年已經過了' + str(remain_time)
		await ctx.send(text)

	@cog_slash_managed(base='time', description='自訂倒數計時 格式:YYYY/MM/DD')
	async def left(self, ctx, time: str):
		time = get_days_left(time, date_format)
		await ctx.send('還剩下: ' + time)

	@cog_slash_managed(base='time', description='現在時間',
		options=[create_option('format', '格式', 
			option_type=SlashCommandOptionType.STRING, 
			required=False, 
			choices=gen_list_of_option_choices(['year', 'month', 'day',
										 'hour', 'minute', 'second', 'week',
										 'date', 'time', 'datetime'])
			)])
	async def current(self, ctx, format: str = ''):
		args = self.parser.parse_args(format.split(' '))
		today = datetime.now()
		year, month, day, hour, minute, second, week = today.timetuple()[:7]

		if args.date:
			args.year = args.month = args.day = args.week = True
		
		if args.time:
			args.hour = args.minute = args.second = True

		# if specified any one of these we do not force concat whole string
		nooptions = not (args.year or args.month or args.day 
				or  args.hour or args.minute or args.second
				or  args.week)

		if args.datetime or nooptions :
			args.year = args.month = args.day \
				= args.hour = args.minute = args.second = True

		week_text = ['一', '二', '三', '四', '五', '六', '日']
		nowtime = '現在時間：'
		nowtime += f'{year}年'   if args.year   else ''
		nowtime += f'{month}月'  if args.month  else ''
		nowtime += f'{day}日'    if args.day    else ''
		nowtime += f'{hour}時'   if args.hour   else ''
		nowtime += f'{minute}分' if args.minute else ''
		nowtime += f'{second}秒' if args.second else ''
		nowtime += f' 星期{week_text[week]}' if args.week else ''
		await ctx.send(nowtime)