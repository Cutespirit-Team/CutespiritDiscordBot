import discord
import twstock
import requests
import json
import datetime
from discord.ext import commands
from ...version import author, bot ,team
from ..utils import cog_slash_managed

# TODO: Add stock name by twstock

class SlashStock(commands.Cog):
	def __init__(self, bot: discord.Client):
		self.bot = bot

	@cog_slash_managed(base='stock', description='查看股票代號')
	async def show(self, ctx, date: str, code: str): # data: YYYYMMDD
		if '/' in date:
			await ctx.send('時間格式為YYYYMMDD喔，請不要輸入符號!')
		else:
			await ctx.send(f'正在搜索時間為{date}的股票代號{code}資訊...請稍後')

			latest_stock = twstock.realtime.get(code) #最新資訊
		
			url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={code}'
			data = json.loads(requests.get(url).text)
			info = []
			stock_data = []

			for item in data['data']:
				if (str(int(item[0].split('/')[0])+1911) + item[0].split('/')[1] + item[0].split('/')[2]) == date:
					stock_data = item

			# for title in range(len(data['fields'])):
			# 	text = []
			# 	for index in range(len(data['data'])):
			# 		text.append(data['data'][index][title])
			# 	info.append(text)

			# stock = []
			# for stocks in range(len(info)):
			# 	temp = ''
			# 	for lable in range(len(info[stocks])):
			# 		temp += info[stocks][lable] + '\n'
			# 	stock.append(temp)

			embed=discord.Embed(title=bot['name'], url=bot['url'],description=f'''
				股票代號：{code}，股票名稱：{latest_stock['info']['name']}\n
				股票全名：{latest_stock['info']['fullname']}''', color=0x00ffd5)
			# for index in range(len(data['fields'])):
			# 	embed.add_field(name=data['fields'][index], value=stock[index], inline=True)

			# embed.add_field(name=, value=stock_data[0], inline=True) #日期
			embed.add_field(name=data['fields'][1], value=stock_data[1], inline=True) #成交股數
			embed.add_field(name=data['fields'][2], value=stock_data[2], inline=True) #成交金額

			embed.add_field(name=data['fields'][3], value=stock_data[3], inline=True) #開盤
			embed.add_field(name=data['fields'][6], value=stock_data[6], inline=True) #收盤
			
			embed.add_field(name=data['fields'][5], value=stock_data[5], inline=True) #最低
			embed.add_field(name=data['fields'][4], value=stock_data[4], inline=True) #最高

			embed.add_field(name=data['fields'][7], value=stock_data[7], inline=True) #漲跌價差
			embed.add_field(name=data['fields'][8], value=stock_data[8], inline=True) #成交比數
			embed.set_footer(text=data['fields'][0] + ': ' + stock_data[0])
			await ctx.send(embed=embed)
