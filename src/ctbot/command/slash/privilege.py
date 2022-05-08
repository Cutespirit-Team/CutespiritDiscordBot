import discord
from discord.ext import commands
from ..utils import cog_slash_managed
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType

# TODO: not test yet
class SlashPrivilege(commands.Cog):
	def __init__(self, bot: discord.Client):
		self.bot = bot

	@cog_slash_managed(description='清除訊息',
		options=[create_option('n', '數量',
		option_type=SlashCommandOptionType.INTEGER,
		required=True)])
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, n: int):
		await ctx.channel.purge(limit=n+1)
		await ctx.send(f'清除 {n+1} 則訊息')

	@cog_slash_managed(description='踢除成員',
		options=[create_option('member', '成員',
		option_type=SlashCommandOptionType.USER,
		required=True)])
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member: discord.Member, reason: str=None):
			await member.kick(reason=reason)
			await ctx.send(f'已踢除 {member.name} !')

	@cog_slash_managed(description='封鎖成員',
		options=[create_option('member', '成員',
		option_type=SlashCommandOptionType.USER,
		required=True)])
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member: discord.Member, reason: str=None):
		await member.ban(reason=reason)
		await ctx.send(f'已封鎖 {member.name} ！')

	@cog_slash_managed(description='解除封鎖成員',
		options=[create_option('member', '成員',
		option_type=SlashCommandOptionType.USER,
		required=True)])
	@commands.has_permissions(ban_members=True)
	async def unban(self, ctx, member: discord.Member):
		banned_users = await ctx.guild.bans()
		member_name, member_discriminator = member.split('#')
		for ban_entry in banned_users:
			user = ban_entry.user
			if (user.name, user.discriminator) == (member_name, member_discriminator):
				await ctx.guild.unban(user)
				await ctx.send(f'解除封鎖 {user.mention}')

	@cog_slash_managed(description='邀請成員')
	async def invite(self, ctx):
		link = await ctx.channel.create_invite(xkcd=True, max_age = 0, max_uses = 0)
		em = discord.Embed(title=f"現在就加入 {ctx.guild.name} Discord 伺服器吧", url=link, description=f"**{ctx.guild.member_count} 個成員** [**加入**]({link})\n\n**{ctx.channel.mention} 的邀請已被建立。**\n可使用次數: **無限**\n連結失效時間: **永遠都不**\n永久連結: **https://discord.cutespirit.org**", color=0x303037)
		em.set_footer(text=f"We are Cutespirit. We are Cute")
		em.set_thumbnail(url=ctx.guild.icon_url)
		em.set_author(name="CUTESPIRIT TEAM SERVER INVITE")
		#-----------------------------------------#
		await ctx.send(f"> {link}", embed=em)