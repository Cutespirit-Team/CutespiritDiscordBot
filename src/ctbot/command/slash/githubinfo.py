import discord
from discord.ext import commands
from ..utils import cog_slash_managed , gen_list_of_choices
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils import manage_components
from discord_slash.model import SlashCommandOptionType , ButtonStyle
import requests
import json

dict_info = {
    '登入' : 'login', 'id' : 'id',
    'html_url' : 'html_url', '粉絲連結' : 'followers_url',
    '追蹤連結' : 'following_url', 'gists_url' : 'gists_url',
    'starred_url' : 'starred_url', 'subscriptions_url' : 'subscriptions_url',
    '組織連結' : 'organizations_url', 'Repos連結' : 'repos_url',
    '事件連結' : 'events_url', '名字' : 'name',
    '公司' : 'company', '部落格' : 'blog',
    '位置' : 'location', '電子郵件' : 'email',
    '自我介紹' : 'bio', '推特使用者名稱' : 'twitter_username',
    '公開的Repos' : 'public_repos', 'public_gists' : 'public_gists',
    '粉絲' : 'followers', '追蹤者' : 'following',
    '建立時間' : 'created_at', '更新時間' : 'updated_at'
    }

class SlashGithubInfo(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='查看Github資訊',
            options=[create_option('user_id', '使用者ID',
                option_type=SlashCommandOptionType.STRING,
                required=True),
            create_option('parameters', '參數',
                option_type=SlashCommandOptionType.STRING,
                required=True,
                choices=gen_list_of_choices(dict_info.keys()))])
    async def github_info(self, ctx, user_id:str, parameters: str):
        label_name = parameters
        parameters = dict_info.get(parameters)
        data = requests.get('https://api.github.com/users/'+ user_id)
        txt = json.loads(data.text)
        if 'message' in txt.keys():
            if txt['message'] == 'Not Found':
                text = '找不到使用者:' + user_id
            await ctx.send(text)
        else:
            info = txt[parameters]
            info = user_id + '的' + label_name + ':' +str(info)
            await ctx.send(info)
