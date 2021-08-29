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
    new_Date = time.strftime('%Y年%m月%d日的%H點%M分' , struct_time)
    return new_Date

class SlashWeather(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='查詢天氣資訊')
    async def weather(self, ctx , city: str):
        if city == '台北市':
        data = requests.get('https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-7610B04F-B7B7-4A9B-9884-52339E4314E1&locationName=' + city)
        txt = json.loads(data.text)
        
        weather = txt['records']['location'][0]['locationName'] + '的天氣:\n'+ \
                    '\t' + dateChange(txt['records']['location'][0]['weatherElement'][0]['time'][0]['startTime']) + ' ~ ' + \
                    dateChange(txt['records']['location'][0]['weatherElement'][0]['time'][0]['endTime']) + ' 是 ' + \
                    txt['records']['location'][0]['weatherElement'][0]['time'][0]['parameter']['parameterName'] + '\n' + \
                    '\t' + dateChange(txt['records']['location'][0]['weatherElement'][0]['time'][1]['startTime']) + ' ~ ' + \
                    dateChange(txt['records']['location'][0]['weatherElement'][0]['time'][1]['endTime']) + ' 是 ' +  \
                    txt['records']['location'][0]['weatherElement'][0]['time'][1]['parameter']['parameterName'] + '\n' + \
                    '\t' + dateChange(txt['records']['location'][0]['weatherElement'][0]['time'][2]['startTime']) + ' ~ ' + \
                    dateChange(txt['records']['location'][0]['weatherElement'][0]['time'][2]['endTime']) + ' 是 ' +  \
                    txt['records']['location'][0]['weatherElement'][0]['time'][2]['parameter']['parameterName'] + '\n' + \
                    '\n濕度是:\n' + \
                    '\t' + dateChange(txt['records']['location'][0]['weatherElement'][1]['time'][0]['startTime']) + ' ~ ' + \
                    dateChange(txt['records']['location'][0]['weatherElement'][1]['time'][0]['endTime']) + ' 是 ' + \
                    txt['records']['location'][0]['weatherElement'][1]['time'][0]['parameter']['parameterName'] + '%\n' + \
                    '\t' + dateChange(txt['records']['location'][0]['weatherElement'][1]['time'][1]['startTime']) + ' ~ ' + \
                    dateChange(txt['records']['location'][0]['weatherElement'][1]['time'][1]['endTime']) + ' 是 ' +  \
                    txt['records']['location'][0]['weatherElement'][1]['time'][1]['parameter']['parameterName'] + '%\n' + \
                    '\t' + dateChange(txt['records']['location'][0]['weatherElement'][1]['time'][2]['startTime']) + ' ~ ' + \
                    dateChange(txt['records']['location'][0]['weatherElement'][1]['time'][2]['endTime']) + ' 是 ' +  \
                    txt['records']['location'][0]['weatherElement'][1]['time'][2]['parameter']['parameterName'] + '%\n' + \
                    '\n溫度是:\n' + \
                    '\t' + dateChange(txt['records']['location'][0]['weatherElement'][2]['time'][0]['startTime']) + ' ~ ' + \
                    dateChange(txt['records']['location'][0]['weatherElement'][2]['time'][0]['endTime']) + ' 是 ' + \
                    txt['records']['location'][0]['weatherElement'][2]['time'][0]['parameter']['parameterName'] + '°C\n' + \
                    '\t' + dateChange(txt['records']['location'][0]['weatherElement'][2]['time'][1]['startTime']) + ' ~ ' + \
                    dateChange(txt['records']['location'][0]['weatherElement'][2]['time'][1]['endTime']) + ' 是 ' +  \
                    txt['records']['location'][0]['weatherElement'][2]['time'][1]['parameter']['parameterName'] + '°C\n' + \
                    '\t' + dateChange(txt['records']['location'][0]['weatherElement'][2]['time'][2]['startTime']) + ' ~ ' + \
                    dateChange(txt['records']['location'][0]['weatherElement'][2]['time'][2]['endTime']) + ' 是 ' +  \
                    txt['records']['location'][0]['weatherElement'][2]['time'][2]['parameter']['parameterName'] + '°C\n'



        startTime = split(txt['records']['location'][0]['weatherElement'][0]['time'][0]['startTime'])
        endTime = split(txt['records']['location'][0]['weatherElement'][0]['time'][0]['endTime'])

        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-7610B04F-B7B7-4A9B-9884-52339E4314E1&locationName=' + city + '&timeFrom=' + startTime + '&timeTo=' + endTime

        data = requests.get(url)
        txt = json.loads(data.text)
        weather += '\n現在' + txt['records']['location'][0]['locationName'] + \
                '的天氣是' + txt['records']['location'][0]['weatherElement'][0]['time'][0]['parameter']['parameterName'] + \
                ' ,濕度是:' + txt['records']['location'][0]['weatherElement'][1]['time'][0]['parameter']['parameterName'] + '%' + \
                ' ,濕度是:' + txt['records']['location'][0]['weatherElement'][2]['time'][0]['parameter']['parameterName'] + '%'
        await ctx.send(weather)

