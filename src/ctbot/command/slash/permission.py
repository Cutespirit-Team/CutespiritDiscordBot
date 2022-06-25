import discord
from discord.ext import commands
from ..utils import cog_slash_managed
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType

# TODO: Fix connot show error

class SlashPermission(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(base='has_cmd_permission',description='你有管理訊息的權限嗎')
    @commands.has_permissions(manage_messages=True)
    async def manage_message(self, ctx):
        member_name = ctx.author.name
        text = member_name + '有管理訊息的權限喔'
        await ctx.send(text)

    @manage_message.error
    async def message_message_error(error, ctx):
        if isinstance(error, MissingPermissions):
            member_name = ctx.author.name
            text = member_name + '沒有管理訊息的權限喔'
            await ctx.send(text)

    @cog_slash_managed(base='has_cmd_permission',description='你ban使用者的權限嗎')
    @commands.has_permissions(ban_members=True)
    async def ban_user(self, ctx):
        member_name = ctx.author.name
        text = member_name + '有ban使用者的權限喔'
        await ctx.send(text)

    @ban_user.error
    async def ban_user_error(error, ctx):
        if isinstance(error, MissingPermissions):
            member_name = ctx.author.name
            text = member_name + '沒有ban使用者的權限喔'
            await ctx.send(text)

    @cog_slash_managed(base='has_cmd_permission',description='你有建立邀請連結的權限嗎')
    @commands.has_permissions(create_instant_invite=True)
    async def create_instant_invite(self, ctx):
        member_name = ctx.author.name
        text = member_name + '有建立邀請連結的權限喔'
        await ctx.send(text)

    @create_instant_invite.error
    async def create_instant_invite_error(error, ctx):
        if isinstance(error, MissingPermissions):
            member_name = ctx.author.name
            text = member_name + '沒有建立連結的權限喔'
            await ctx.send(text)