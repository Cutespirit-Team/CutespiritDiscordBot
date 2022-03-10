import discord
from discord.ext import commands
from ..utils import cog_slash_managed , gen_list_of_choices
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils import manage_components
from discord_slash.model import SlashCommandOptionType , ButtonStyle
from ...version import weather
import requests
import json
import time , datetime

# TODO: Clean Code
# TODO: Fix Error that somewhere can not be outputed to the Discord

token = f'{weather["weather_token"]}'

def split(text):
    temp = text.split()
    return temp[0] + 'T' + temp[1]
def dateChange(date):   #將日期轉換格式
    struct_time = time.strptime(date , "%Y-%m-%d %H:%M:%S")
    new_Date = time.strftime('%Y年%m月%d日的%H點%M分' , struct_time)
    return new_Date
def dateToday(date):    #將日期轉換格式
    struct_time = time.strptime(date , "%Y-%m-%d %H:%M:%S")
    new_Date = time.strftime('%H點%M分' , struct_time)
    return new_Date
def isToday(date):  #傳進來的時間對於今天來講是明天還是今天
    #處理今天
    today = datetime.datetime.today()
    today_text = str(today.year) + '-' + str(today.month) + '-' + str(today.day)
    stuct_today = time.strptime(today_text , "%Y-%m-%d")
    new_today_month = int(time.strftime('%m' , stuct_today))
    new_today_date = int(time.strftime('%d' , stuct_today))
    new_today = new_today_month *31 + new_today_date    #月份*31天+日
    #處理傳進來的日子
    struct_time = time.strptime(date , "%Y年%m月%d日的%H點%M分")
    new_time_month = int(time.strftime('%m' , struct_time))
    new_time_date = int(time.strftime('%d' , struct_time))
    new_time = new_time_month*31 + new_time_date        #月份*31天*日
    if new_today == new_time:
        return '今天'
    elif new_today < new_time:
        return '明天'
    else:
        return '時間錯誤'

dict_city = {
    '台北' : '臺北市', #'臺北' : '臺北市',
    '宜蘭' : '宜蘭縣', '花蓮' : '花蓮縣',
    '台東' : '臺東縣', #'臺東' : '臺東縣', 
    '澎湖' : '澎湖縣', '金門' : '金門縣',
    '連江' : '連江縣', '新北' : '新北市',
    '桃園' : '桃園市', #'臺中' : '臺中市',
    '台中' : '臺中市', #'臺南' : '臺南市',
    '台南' : '臺南市', '高雄' : '高雄市',
    '基隆' : '基隆市', '新竹' : '新竹市',
    '苗栗' : '苗栗縣', '彰化' : '彰化縣',
    '南投' : '南投縣', '雲林' : '雲林縣', 
    '嘉義' : '嘉義市', '屏東' : '屏東縣'
        }

class SlashWeather(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='查詢天氣資訊',
            options=[create_option('city', '城市',
            option_type=SlashCommandOptionType.STRING,
            required=True,
            choices=gen_list_of_choices(dict_city.keys()))]
            )
    async def weather(self, ctx , city: str):
        if '市' not in city and '縣' not in city:
            city = dict_city.get(city)
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&locationName=' + city
        data = requests.get(url)
        txt = json.loads(data.text)
        weatherElement = txt['records']['location'][0]['weatherElement']       
        weather = txt['records']['location'][0]['locationName'] + '的天氣:\n'+ \
                    isToday(dateChange(weatherElement[0]['time'][0]['startTime'])) + '\t' + \
                    '\t' + dateToday(weatherElement[0]['time'][0]['startTime']) + ' ~ ' + \
                    dateToday(weatherElement[0]['time'][0]['endTime']) + ' 是 ' + \
                    weatherElement[0]['time'][0]['parameter']['parameterName'] + '\n' + \
                    isToday(dateChange(weatherElement[0]['time'][2]['startTime'])) + '\t' + \
                    '\t' + dateToday(weatherElement[0]['time'][2]['startTime']) + ' ~ ' + \
                    dateToday(weatherElement[0]['time'][2]['endTime']) + ' 是 ' +  \
                    weatherElement[0]['time'][2]['parameter']['parameterName'] + '\n' + \
                    '\n濕度是:\n' + \
                    isToday(dateChange(weatherElement[1]['time'][0]['startTime'])) + '\t' + \
                    '\t' + dateToday(weatherElement[1]['time'][0]['startTime']) + ' ~ ' + \
                    dateToday(weatherElement[1]['time'][0]['endTime']) + ' 是 ' + \
                    weatherElement[1]['time'][0]['parameter']['parameterName'] + '%\n' + \
                    isToday(dateChange(weatherElement[1]['time'][2]['startTime'])) + '\t' + \
                    '\t' + dateToday(weatherElement[1]['time'][2]['startTime']) + ' ~ ' + \
                    dateToday(weatherElement[1]['time'][2]['endTime']) + ' 是 ' +  \
                    weatherElement[1]['time'][2]['parameter']['parameterName'] + '%\n' + \
                    '\n溫度是:\n' + \
                    isToday(dateChange(weatherElement[2]['time'][0]['startTime'])) + '\t' + \
                    '\t' + dateToday(weatherElement[2]['time'][0]['startTime']) + ' ~ ' + \
                    dateToday(weatherElement[2]['time'][0]['endTime']) + ' 是 ' + \
                    weatherElement[2]['time'][0]['parameter']['parameterName'] + '°C\n' + \
                    isToday(dateChange(weatherElement[2]['time'][2]['startTime'])) + '\t' + \
                    '\t' + dateToday(weatherElement[2]['time'][2]['startTime']) + ' ~ ' + \
                    dateToday(weatherElement[2]['time'][2]['endTime']) + ' 是 ' +  \
                    weatherElement[2]['time'][2]['parameter']['parameterName'] + '°C\n'

        startTime = split(weatherElement[0]['time'][0]['startTime'])
        endTime = split(weatherElement[0]['time'][0]['endTime'])

        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&locationName=' + city + '&timeFrom=' + startTime + '&timeTo=' + endTime

        data = requests.get(url)
        txt = json.loads(data.text)
        weather += '\n現在' + txt['records']['location'][0]['locationName'] + \
                '的天氣是' + weatherElement[0]['time'][0]['parameter']['parameterName'] + \
                ' ,濕度是:' + weatherElement[1]['time'][0]['parameter']['parameterName'] + '%' + \
                ' ,溫度是:' + weatherElement[2]['time'][0]['parameter']['parameterName'] + '%'
        await ctx.send(weather)
