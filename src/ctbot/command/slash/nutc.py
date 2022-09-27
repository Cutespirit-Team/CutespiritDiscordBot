import discord
from discord.ext import commands
from ..utils import cog_slash_managed
import requests
import json


def strB2Q(ustring):
    """半形轉全形"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:                 # 半形空格直接轉化
            inside_code = 12288
        elif 32 <= inside_code <= 126:        # 半形字元（除空格）根據關係轉化
            inside_code += 65248
        rstring += chr(inside_code)
    return rstring

def getID(class_name):
    url = 'https://api.tershi.com/getClassRoom'
    data = requests.get(url).text
    data = json.loads(data)
    matching = [s['id'] for s in data if strB2Q(class_name) in s['name']]
    lst = []
    for i in matching:
        lst.append(i)
    return lst

class SlashNutc(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(base="timetable",
        description='查看班級代號',
        options=[
        create_option('class_name', '班級名稱(例:資工一1)',
        option_type=SlashCommandOptionType.STRING,
        required=True)])
    async def id_check(self, ctx, class_name: str="null"):
        if class_name == null:
            await ctx.send('請輸入班級名稱或是正確的值')
        else:
            lst = getID(class_name)
            text = ''
            for i in lst:
                text += i + ', '
            return text

    @cog_slash_managed(base="timetable",
        description='查看班級課表',
        options=[
        create_option('class_name', '班級名稱(例:資工一1)',
        option_type=SlashCommandOptionType.STRING,
        required=True)])
    async def id_check(self, ctx, class_name: str="null"):
        if class_name == null:
            await ctx.send('請輸入班級名稱或是正確的值')
        else:
            if len(getID(class_name)) == 1:
                url = 'https://api.tershi.com/getTable?id=' + getID(class_name)[0]
                data = requests.get(url).text
                # data = json.loads(data)
                await ctx.send(data)
                await ctx.send('課表尚還沒完成')
            else:
                await ctx.send('請輸入完整的班級號碼')

        # for i in range(len(data)):
        #     lst = data[i][]


        # await ctx.send('Pong!')
