import discord
import logging
import json
from .config import BotConfig
from discord.ext import commands
from discord_slash.client import SlashCommand

config = BotConfig('../bot.ini')
class CTBot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix=config.get_general_prefix())
		self.logger = logging.getLogger('ctbot')
		SlashCommand(self, delete_from_unused_guilds=True, sync_commands=True)
		if config.get_enable_slash():
			self.logger.info('Enable slash command.')
			from .command.utils import regist_slash_command
			regist_slash_command(self)

	def run(self):
		try:
			super().run(config.get_token())
		except discord.LoginFailure as e:
			self.logger.error(f'{e}\nPlease edit config in: {config.path}')

# discord event
	async def on_ready(self):
		self.logger.info('Ready.')

	async def on_message(self, message: discord.Message):
		if message.author == self.user:
			return

		# NOTE: use decorate instead except we are going to use manual way to handle commands
		# responsible_channels = config.get_responsible_channels(message.guild.id)
		# if len(responsible_channels) != 0 and message.channel.id not in responsible_channels:
		# 	await message.add_reaction('😷')
		try:
			words = open('config/words.json', mode='r', encoding='utf-8')
			words = json.loadw(ords)
			for i in words.keys():
				if i.startswith('.') and i[1:-1] == message.content:
					channel = message.channel
					user = message.author.id
					ID = '<@' + str(user)+'>'
					await channel.send(ID + '，' + words[i])
					await message.delete()
					break
				if i.startswith('.') == False and i in message.content:
					channel = message.channel
					user = message.author.id
					ID = '<@' + str(user)+'>'
					await channel.send(ID + '，' + words[i])
					await message.delete()
					break

		except FileNotFoundError:
			filename = 'config/words.json'
			content = {
				'Example1' : 'a word',
				'.Example2.' : 'a word in a sentense'
				}
			f = open(filename, 'w')
			json.dump(content, f, indent=4)
			f.close()

	async def on_member_join(self, member):
		guild = member.guild
		if guild.system_channel is not None:
			to_send = f'Welcome {member.mention} to {guild.name}!'
			await guild.system_channel.send(to_send)
			# self.logger.info(f'{member.mention} 加入了伺服器')

	# async def on_error(self, ev, *args, **kwargs):
	# 	pass

# slash evnet
	async def on_slash_command(self, ctx):
		pass

	async def on_slash_command_err(self, ctx, err):
		if isinstance(err, commands.CommandError):
			await ctx.send("錯誤： 指令或參數不正確")

		perm = [commands.MissingPermissions, commands.BotMissingPermissions]
		if any(map(lambda e: isinstance(err, e), perm)):
			await ctx.send("錯誤： 權限不足")

		# NOTE: i dont know what {err} format is
		self.logger.error(f'slash_command  {err}')

	async def on_component(self, ctx):
		pass

	async def on_component_callback(self, ctx, callback):
		pass
		
	# async def on_component_callback_error(self, ctx, ex):
	# 	pass
		
		