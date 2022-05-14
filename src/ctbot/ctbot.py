import discord
import logging
import json
import datetime
from .config import BotConfig
from discord.ext import commands
from discord_slash.client import SlashCommand
from .version import author, bot ,team
from discord_components import DiscordComponents, ComponentsBot, Button, ButtonStyle

config = BotConfig('../bot.ini')
time_window_milliseconds = 10000
max_msg_per_window = 5
author_msg_times = {}

class CTBot(commands.Bot):
	def __init__(self):
		# super().__init__(command_prefix="/")
		intents = discord.Intents.default()
		intents.members = True
		super().__init__(command_prefix=config.get_general_prefix(), intents=intents)
		self.logger = logging.getLogger('ctbot')
		DiscordComponents(self)
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
		global author_msg_counts

		author_id = message.author.id
		# Get current epoch time in milliseconds
		curr_time = datetime.datetime.now().timestamp() * 1000

		# Make empty list for author id, if it does not exist
		if not author_msg_times.get(author_id, False):
			author_msg_times[author_id] = []

		# Append the time of this message to the users list of message times
		author_msg_times[author_id].append(curr_time)

		# Find the beginning of our time window.
		expr_time = curr_time - time_window_milliseconds

		# Find message times which occurred before the start of our window
		expired_msgs = [
			msg_time for msg_time in author_msg_times[author_id]
			if msg_time < expr_time
		]

		# Remove all the expired messages times from our list
		for msg_time in expired_msgs:
			author_msg_times[author_id].remove(msg_time)
		# ^ note: we probably need to use a mutex here. Multiple threads
		# might be trying to update this at the same time. Not sure though.

		if len(author_msg_times[author_id]) > max_msg_per_window:
			await message.channel.send(f"{message.author.mention}，請不要刷屏喔！！")

		# Test button
		# if message.content == 'hello_btn':
		# 	await message.channel.send(
		# 		"Hello, World!",
		# 		components = [
		# 			Button(label = "WOW button!", custom_id = "button1")
		# 		]
		# 	)
		# 	interaction = await self.wait_for("button_click", check = lambda i: i.custom_id == "button1")
		# 	await interaction.send(content = "Button clicked!")

		# NOTE: use decorate instead except we are going to use manual way to handle commands
		# responsible_channels = config.get_responsible_channels(message.guild.id)
		# if len(responsible_channels) != 0 and message.channel.id not in responsible_channels:
		# 	await message.add_reaction('😷')
		try:
			words = open('config/words.json', mode='r', encoding='utf-8')
			words = json.load(words)
			for i in words.keys():
				if i.startswith('.') and i[1:-1] == message.content:
					channel = message.channel
					user = message.author.id
					ID = '<@' + str(user)+'>'
					await channel.send(ID + '，' + words[i])
					# await message.delete()
					break
				if i.startswith('.') == False and i in message.content:
					channel = message.channel
					user = message.author.id
					ID = '<@' + str(user)+'>'
					await channel.send(ID + '，' + words[i])
					# await message.delete()
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
			
			# self.logger.info(f'{member.mention} 加入了伺服器')
			try:
				config = open('config/member_join.json', mode='r', encoding='utf-8')
				config = json.load(config)
				to_send = config['member_join_text']
				join_role_id = config['join_role_id']
				role = guild.get_role(int(join_role_id))
				await member.add_roles(role)

				if config['enable_embed'] == 'no':
					await guild.system_channel.send(to_send.format(member_mention=member.mention, guild_name=guild.name))
				elif config['enable_embed'] == 'yes':
					embed=discord.Embed(title=bot['name'], url=bot['url'], description=config['embed_join_text'].format(member_mention=member.mention), color=0x00ffd5)
					embed.set_author(name=team['name'], url=bot['url'], icon_url=bot['icon'])
					if config['enable_embed_thumbnail'] == 'yes':
						embed.set_thumbnail(url=bot['icon'])
					await guild.system_channel.send(embed=embed)
				else:
					print('Error Json File Config')
			except FileNotFoundError:
				filename = 'config/member_join.json'
				content = {
					'member_join_text' : 'Welcome {member_mention} to {guild_name}!',
					'enable_embed' : 'yes',
					'embed_join_text' : 'Yo~ {member_mention} 歡迎您加入 Cutespirit Team 伺服器群組喔！ 啾咪~別忘記去領取身分組',
					'enable_embed_thumbnail' : 'no'
					}
				f = open(filename, 'w')
				json.dump(content, f, indent=4)
				f.close()

	async def on_member_remove(self, member):
		guild = member.guild
		if guild.system_channel is not None:
			
			# self.logger.info(f'{member.mention} 離開了伺服器')
			try:
				config = open('config/member_leave.json', mode='r', encoding='utf-8')
				config = json.load(config)
				to_send = config['member_leave_text']
				if config['enable_embed'] == 'no':
					await guild.system_channel.send(to_send.format(member_name=member.name))
				elif config['enable_embed'] == 'yes':
					embed=discord.Embed(title=bot['name'], url=bot['url'], description=config['embed_leave_text'].format(member_name=member.name), color=0x00ffd5)
					embed.set_author(name=team['name'], url=bot['url'], icon_url=bot['icon'])
					if config['enable_embed_thumbnail'] == 'yes':
						embed.set_thumbnail(url=bot['icon'])
					await guild.system_channel.send(embed=embed)
				else:
					print('Error Json File Config')
			except FileNotFoundError:
				filename = 'config/member_leave.json'
				content = {
					'member_leave_text' : '{member_name} 離開了我們QQ!',
					'enable_embed' : 'yes',
					'embed_leave_text' : '{member_name} 無情又殘忍地離開了 Cutespirit Team 伺服器群組喔！QQ',
					'enable_embed_thumbnail' : 'no'
					}
				f = open(filename, 'w')
				json.dump(content, f, indent=4)
				f.close()

	# TODO: Add specific channel id for spectific reaction role
	# TODO: Change time zone for Asia time
	async def on_raw_reaction_add(self, payload):
		try:
			config = open('config/reaction_role.json', mode='r', encoding='utf-8')
			config = json.load(config)
			emoji = payload.emoji
			guild = self.get_guild(payload.guild_id)
			channel_ID = config['channel_id']
			if payload.channel_id == int(channel_ID):
				for emoji_ID in config.keys():
					if emoji_ID == emoji.name:
						# 給身分組
						role = guild.get_role(int(config[emoji_ID]))
						await payload.member.add_roles(role)
						
		except FileNotFoundError:
			filename = 'config/reaction_role.json'
			content = {
				'channel_id' : 'channel_id',
				'EMOJI_ID' : 'ROLE_ID'
				}
			f = open(filename, 'w')
			json.dump(content, f, indent=4)
			f.close()

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