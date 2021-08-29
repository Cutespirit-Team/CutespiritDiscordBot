import discord
from discord.ext import commands
from ..utils import cog_slash_managed
import requests
import json
import time

def split(text):
    temp = text.split()
    return temp[0] + 'T' + temp[1]
def dateChange(date):
    struct_time = time.strptime(date , "%Y-%m-%d %H:%M:%S")
    new_Date = time.strftime('%Y年%m月%d日的%H點%M分')
    return new_Date

class SlashWeather(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='查詢天氣資訊')
    async def weather(self, ctx , city: str):
        data = requests.get('https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-7610B04F-B7B7-4A9B-9884-52339E4314E1&locationName=' + city)
        txt = json.loads(data.text)
        
        weather = txt['records']['location'][0]['locationName'] + '的天氣:\n'+ \
                    dateChange(txt['records']['location'][0]['weatherElement'][0]['time'][0]['startTime']) + '~' + \
                    dateChange(txt['records']['location'][0]['weatherElement'][0]['time'][0]['endTime']) + ' 是 ' +  \
                    txt['records']['location'][0]['weatherElement'][0]['time'][0]['parameter']['parameterName']
        
        startTime = split(txt['records']['location'][0]['weatherElement'][0]['time'][0]['startTime'])
        endTime = split(txt['records']['location'][0]['weatherElement'][0]['time'][0]['endTime'])

        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-7610B04F-B7B7-4A9B-9884-52339E4314E1&locationName=' + city + '&timeFrom=' + startTime + '&timeTo=' + endTime

        data = requests.get(url)
        txt = json.loads(data.text)
        weather += '\n' + txt['records']['location'][0]['locationName'] + ' ' + txt['records']['location'][0]['weatherElement'][0]['time'][0]['parameter']['parameterName']
        await ctx.send(weather)

