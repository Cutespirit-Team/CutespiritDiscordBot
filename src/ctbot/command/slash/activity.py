import discord
from discord.ext import commands
from ..utils import cog_slash_managed, gen_list_of_choices
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType
import json

dict_status = {
	'線上' : 'online', '閒置' :  'idle',
	'勿擾' : 'do_not_disturb', '下線' : 'offline'
}

class SlashActivity(commands.Cog):
	def __init__(self, bot: discord.Client):
		self.bot = bot

	@cog_slash_managed(description='更改狀態',
			options=[
			create_option('ty', '類型',
			option_type=SlashCommandOptionType.STRING,
			required=True,
			choices=gen_list_of_choices(['online','idle','do_not_disturb','offline'])),
			create_option('msg', '訊息',
        	option_type=SlashCommandOptionType.STRING,
        	required=True)
        	])
	async def status(self, ctx, ty: str, msg: str):
		if ty == 'online':
			await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(msg))
		elif ty == 'idle':
			await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(msg))
		elif ty == 'do_not_disturb':
			await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(msg))
		elif ty == 'offline':
			await self.bot.change_presence(status=discord.Status.offline, activity=discord.Game(msg))
		await ctx.send('已變更狀態', hidden=True)