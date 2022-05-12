import discord
from datetime import datetime
from discord.ext import commands
# import discord_interactions
from discord_slash import SlashCommand, cog_ext
from ..utils import cog_slash_managed, gen_list_of_choices
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType, ButtonStyle
# from discord_components import DiscordComponents, ComponentsBot, Button, ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow

# TODO: add open, close, delete, rename, transcript, add, remove, claim, add

dict_yn = { 'yes' : '是', 'no' : '否' }

class SlashService(commands.Cog):
	def __init__(self, bot: discord.Client):
		self.bot = bot

	@cog_slash_managed(base='service', description='打開服務客服單')
	async def open(self, ctx):
		channel_name = ctx.channel.name
		if channel_name.startswith('closed'):   # in closed TextChannel: reopen
			name =  'ticket-' + channel_name.split('-')[1] + '-' +channel_name.split('-')[2]
			await ctx.channel.edit(name=name)
			embed=discord.Embed(description=f'<@{str(ctx.author.id)}> 已重新打開客服服務單\n如欲關閉服務客服單，請使用指令「/service close」', color=0x2cff00)
			# buttons = [create_button(style=ButtonStyle.blue, label="關閉服務客服單", custom_id="reopen_close_service")]
			# buttons1 = [create_button(style=ButtonStyle.blue, label="關閉服務客服單", custom_id="close_service")]
			# action_row1 = create_actionrow(*buttons1)
			# await ctx.send(embed=embed, components=[action_row1])
			await ctx.send(embed=embed)
		elif channel_name.startswith('ticket'): # in ticket TextChannel: already inside
			await ctx.send('警告：您已經在服務客服單中了，無法重新開啟。')
		else:                                   # in other TextChannel: open
			channel_name = ctx.channel.name
			today = datetime.now()
			now_today = today.strftime("%m%d-%H%M")
			ticket_ID = 'Ticket-' + now_today
			overwrites = {
			ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
			ctx.author: discord.PermissionOverwrite(view_channel=True),
			# your_role: discord.PermissionOverwrite(view_channel=True)
			}
			service_channel = await ctx.guild.create_text_channel(ticket_ID, overwrites=overwrites)
			text = '服務客服單已被' + ctx.author.name + '打開'
			await ctx.send(text)
			text = '歡迎 <@' + str(ctx.author.id) + '> 來到服務客服單\n如果要關閉服務客服單請輸入點擊 🔒\n單號：' + ticket_ID
			embed=discord.Embed(description=text, color=0x2cff00)
			text = '服務客服單 - 靈萌團隊 Discord 機器人'
			embed.set_footer(text=text)
			# buttons = [create_button(style=ButtonStyle.blue, label="關閉服務客服單", custom_id="open_close_service")]
			# buttons2 = [create_button(style=ButtonStyle.blue, label="關閉服務客服單", custom_id="close_service")]
			# action_row2 = create_actionrow(*buttons2)
			# await service_channel.send(embed=embed, components=[action_row2])
			await ctx.send(embed=embed)

	@cog_slash_managed(base='service',
			description='關閉服務客服單',
			options=[create_option('confirm', '是否',
			option_type=SlashCommandOptionType.STRING,
			required=True,
			choices=gen_list_of_choices(dict_yn.keys()))]
			)
	async def close(self, ctx, confirm: str):
		channel_name = ctx.channel.name
		if channel_name.startswith('ticket'):   # in ticket TextChannel: close
			if confirm == 'yes':
				name =  'closed-' + channel_name.split('-')[1] + '-' +channel_name.split('-')[2]
				await ctx.channel.edit(name=name)
				embed=discord.Embed(description=f'<@{str(ctx.author.id)}> 已關閉客服服務單\n如欲重新打開服務客服單，請使用指令「/service open」', color=0x2cff00)
				# buttons = [create_button(style=ButtonStyle.blue, label="開啟服務客服單", custom_id="close_open_service")]
				# buttons3 = [create_button(style=ButtonStyle.blue, label="開啟服務客服單", custom_id="open_service")]
				# action_row3 = create_actionrow(*buttons3)
				# await ctx.send(embed=embed, components=[action_row3])
				await ctx.send(embed=embed)
			else:
				await ctx.send('取消成功')
		elif channel_name.startswith('closed'): # in closed TextChannel: already inside
			# buttons = [create_button(style=ButtonStyle.blue, label="開啟服務客服單", custom_id="inside_open_service")]
			# buttons4 = [create_button(style=ButtonStyle.blue, label="開啟服務客服單", custom_id="open_service")]
			# action_row4 = create_actionrow(*buttons4)
			# await ctx.send('警告：客服單已經關閉了，無法重新關閉。', components=[action_row4])
			await ctx.send('警告：客服單已經關閉了，無法重新關閉。')
		else:
			await ctx.send('您不在服務客服單中！')
		
	@cog_slash_managed(base='service',
			description='刪除服務客服單',
			options=[create_option('confirm', '是否',
			option_type=SlashCommandOptionType.STRING,
			required=True,
			choices=gen_list_of_choices(dict_yn.keys()))]
	)
	async def delete(self, ctx, confirm: str):
		channel_name = ctx.channel.name
		if channel_name.startswith('ticket') or channel_name.startswith('closed'):  # in ticket or closed TextChannel: delete
			if confirm == 'yes':
				await ctx.send('正在刪除中，可能會用到幾秒時間...')
				await ctx.channel.delete()
			else:
				await ctx.send('取消成功')
		else:
			await ctx.send('您不在服務客服單中！')

	@cog_slash_managed(base='service', description='服務客服單說明')
	async def manual(self, ctx):
		user_id = '<@' + str(ctx.author.id) + '>'
		text = f'歡迎 {user_id} 來到服務客服單說明\n以下為服務客服單規則和使用說明書。 \n'
		rule = '''
				一、請勿一直重複開服務客服單。
				二、請勿開服務客服單罵人。
				三、如已得到解決方法請關閉或刪除服務客服單。
				四、如關閉服務客服單，管理員會保存起來，以便後續糾紛清查。
			'''
		manual = '''
				一、如欲打開服務客服單，請使用指令「/service open」。
				二、如欲關閉服務客服單，請使用指令「/service close」。
				三、如欲刪除服務客服單，請使用指令「/service delete」。
				四、如欲查看服務客服單說明，請使用指令「/service manual」。
			'''
		embed=discord.Embed(description=text, color=0x2cff00)
		embed.add_field(name='使用規則', value=rule, inline=False)
		embed.add_field(name='使用說明書', value=manual, inline=False)
		embed.set_footer(text='服務客服單 - 靈萌團隊 Discord 機器人')
		buttons5 = [create_button(style=ButtonStyle.blue, label="開啟服務客服單", custom_id="open_service")]
		action_row5 = create_actionrow(*buttons5)
		await ctx.send(embed=embed, components=[action_row5])

	# def check_button(i: discord.Interaction, button):
	#       return i.author == ctx.author and i.message == msg

	@cog_slash_managed(base='service', description='建立服務客服單')
	async def create(self, ctx):
		bot = self.bot
		# # await ctx.message.delete()
		# embed = discord.Embed(title="開啟服務客服單", description="使用📩來開啟服務客服單")
		# msg = await ctx.channel.send(embed=embed, components=[Button(style=ButtonStyle.blue, label="開啟服務客服單", custom_id="open", disabled = False)])
		# interaction, button = await bot.wait_for('button_click', check=lambda i: i.component.label.startswith("Click"))
		# if button.custom_id == "open":
		#   ctx.send('Open a ticket')

		buttons6 = [create_button(style=ButtonStyle.blue, label="開啟服務客服單", custom_id="open_service")]
		action_row6 = create_actionrow(*buttons6)
		await ctx.send(components=[action_row6])

	# @cog_ext.cog_component()
	# async def reopen_close_service(self, ctx):
	# 	# await ctx.edit_origin(content="要開啟了喔幹!")
	# 	await ctx.send("要關閉了喔幹!")

	# @cog_ext.cog_component()
	# async def open_close_service(self, ctx):
	# 	# await ctx.edit_origin(content="要開啟了喔幹!")
	# 	await ctx.send("要關閉了喔幹!")

	# @cog_ext.cog_component()
	# async def close_open_service(self, ctx):
	# 	# await ctx.edit_origin(content="要開啟了喔幹!")
	# 	await ctx.send("要開啟了喔幹!")

	# @cog_ext.cog_component()
	# async def inside_open_service(self, ctx):
	# 	# await ctx.edit_origin(content="要開啟了喔幹!")
	# 	await ctx.send("要開啟了喔幹!")

	# @cog_ext.cog_component()
	# async def manual_open_service(self, ctx):
	# 	# await ctx.edit_origin(content="要開啟了喔幹!")
	# 	await ctx.send("要開啟了喔幹!")

	@cog_ext.cog_component()
	async def open_service(self, ctx):
		# await ctx.delete()
		channel_name = ctx.channel.name
		if channel_name.startswith('closed'):   # in closed TextChannel: reopen
			name =  'ticket-' + channel_name.split('-')[1] + '-' +channel_name.split('-')[2]
			embed=discord.Embed(description=f'<@{str(ctx.author.id)}> 已重新打開客服服務單', color=0x2cff00)
			await ctx.channel.edit(name=name)
			# buttons = [create_button(style=ButtonStyle.blue, label="關閉服務客服單", custom_id="reopen_close_service")]
			buttons7 = [create_button(style=ButtonStyle.blue, label="關閉服務客服單", custom_id="close_service")]
			action_row7 = create_actionrow(*buttons7)
			await ctx.send(embed=embed, components=[action_row7])
		elif channel_name.startswith('ticket'): # in ticket TextChannel: already inside
			await ctx.send('警告：您已經在服務客服單中了，無法重新開啟。')
		else:                                   # in other TextChannel: open
			channel_name = ctx.channel.name
			today = datetime.now()
			now_today = today.strftime("%m%d-%H%M")
			ticket_ID = 'Ticket-' + now_today
			overwrites = {
			ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
			ctx.author: discord.PermissionOverwrite(view_channel=True),
			# your_role: discord.PermissionOverwrite(view_channel=True)
			}
			service_channel = await ctx.guild.create_text_channel(ticket_ID, overwrites=overwrites)
			text = '服務客服單已被' + ctx.author.name + '打開'
			await ctx.send(text)
			text = f'''歡迎 <@{str(ctx.author.id)}> 來到服務客服單\n
						如果要關閉服務客服單請輸入點擊 🔒\n單號：{ticket_ID}\n
						如欲查看服務客服單說明，請使用指令「/service manual」。'''
			embed=discord.Embed(description=text, color=0x2cff00)
			text = '服務客服單 - 靈萌團隊 Discord 機器人'
			embed.set_footer(text=text)
			# buttons = [create_button(style=ButtonStyle.blue, label="關閉服務客服單", custom_id="open_close_service")]
			# buttons = [create_button(style=ButtonStyle.blue, label="關閉服務客服單", custom_id="close_service")]
			# action_row = create_actionrow(*buttons) #, components=[action_row]
			await service_channel.send(embed=embed)

	@cog_ext.cog_component()
	async def close_service(self, ctx):
		# await ctx.delete()
		channel_name = ctx.channel.name
		if channel_name.startswith('ticket'):   # in ticket TextChannel: close
			if confirm == 'yes':
				name =  'closed-' + channel_name.split('-')[1] + '-' +channel_name.split('-')[2]
				embed=discord.Embed(description=f'<@{str(ctx.author.id)}> 已關閉客服服務單', color=0x2cff00)
				await ctx.channel.edit(name=name)
				# buttons = [create_button(style=ButtonStyle.blue, label="開啟服務客服單", custom_id="close_open_service")]
				buttons8 = [create_button(style=ButtonStyle.blue, label="開啟服務客服單", custom_id="open_service")]
				action_row8 = create_actionrow(*buttons8)
				await ctx.send(embed=embed, components=[action_row8])
			else:
				await ctx.send('取消成功')
		elif channel_name.startswith('closed'): # in closed TextChannel: already inside
			# buttons = [create_button(style=ButtonStyle.blue, label="開啟服務客服單", custom_id="inside_open_service")]
			buttons9 = [create_button(style=ButtonStyle.blue, label="開啟服務客服單", custom_id="open_service")]
			action_row9 = create_actionrow(*buttons9)
			await ctx.send('警告：客服單已經關閉了，無法重新關閉。', components=[action_row9])
		else:
			await ctx.send('您不在服務客服單中！')

	# @cog_slash_managed(base='service', description='客服單測試')
	# async def _ButtonTest(self, ctx):
	#   await ctx.channel.send("test", components=[Button(style=ButtonStyle.blue, label='sus')])
	#   instruction = await bot.wait_for("button_click", check=lambda i: i.component.label.startswith("Click"))
	#   await instruction.send(content='Test button function succeeded!!')