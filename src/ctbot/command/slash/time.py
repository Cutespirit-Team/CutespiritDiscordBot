import discord
import argparse
from discord.ext import commands
from datetime import datetime
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType
from ..utils import cog_slash_managed, gen_list_of_option_choices

# NOTE: something need to change cause it's wrong
when_cap_111  = '2022/05/14 08:30' # 111 會考日期
when_tcte_111 = '2022/05/07 10:15' # 111 統測日期
when_ceec_111 = '2022/01/15 09:20' # 111 學測日期
# ceecCountDown111 = datetime(2022,1,15,9,20) # 111學測日期
when_tershi_18 = '2022/05/26' # 夏特稀 111 生日
yahoo_knowledge_discontinued = '2021/05/04' # 奇摩知識家停止服務

date_format = '%Y/%m/%d'
datetime_format = '%Y/%m/%d %H:%M'

def get_days_left(deadline, format=None):
    if type(deadline) == str:
        deadline = datetime.strptime(deadline, format)

    if (deadline - datetime.now()).days/365 >=1: #如果到期日-今天 還有365天
        return str((deadline-datetime.now()).days//365) + '年' \
             + str((deadline-datetime.now()).days%365) + '天' \
             + str((deadline-datetime.now()).seconds//3600) + '小時' \
             + str(((deadline-datetime.now()).seconds//60)%60) + '分鐘' #加入年
    return str((deadline-datetime.now()).days) + '天' + str((deadline-datetime.now()).seconds//3600) + '小時' + str(((deadline-datetime.now()).seconds//60)%60) + '分鐘'

def get_exam_days_left():
    text  = '中華帝國年行事曆\n\n'
    text += '=====111年=====\n'
    text += f'{when_tershi_18} 夏特稀皇帝18歲誕辰倒數 {get_days_left(when_tershi_18, date_format)} \n'
    text += f'{when_cap_111 } 會考倒數：\t{get_days_left(when_cap_111, datetime_format)} \n'
    text += f'{when_ceec_111} 學測倒數：\t{get_days_left(when_tcte_111, datetime_format)} \n'
    text += f'{when_tcte_111} 統測倒數：\t{get_days_left(when_ceec_111, datetime_format)} \n'
    text += '\n各位中華帝國的子民的，有什麼需要倒數的，或是日程，可以與 @TershiXia聯絡喔！\n'
    text += '111會考生: Cute USB#5387 , 嘎逼#1596 , 祥翔#4073\n'
    text += '111學測生: @拉拉拉拉 \n'
    text += '111統測生: 夏特稀#3716 \n'
    return text

def get_remain_time(year, month, day, hour, minute, second):
    d1 = datetime(year,1,1)
    d2 = datetime(year,month,day)
    remain_day = d2 - d1
    remain_time = ((remain_day.days *24 + hour)*60+minute)*60+second
    remain_time = remain_time / 31536000
    remain_time = "%.2f%%" % (remain_time * 100)
    return remain_time

class SlashTime(commands.Cog):
    def __init__(self, client: discord.Client):
        parser = argparse.ArgumentParser(exit_on_error=False, add_help=False)
        parser.add_argument('--year', action='store_true', default=False)
        parser.add_argument('--month', '--mon', action='store_true', default=False)
        parser.add_argument('--day', action='store_true', default=False)
        parser.add_argument('--hour', action='store_true', default=False)
        parser.add_argument('--minute', '--min', action='store_true', default=False)
        parser.add_argument('--second', '--sec', action='store_true', default=False)
        parser.add_argument('--week', action='store_true', default=False)
        parser.add_argument('--date', action='store_true', default=False)
        parser.add_argument('--time', action='store_true', default=False)
        parser.add_argument('--datetime', action='store_true', default=False)
        parser.add_argument('unused', nargs='*')
        self.parser = parser

    @cog_slash_managed(base='time', description='特別日倒數計時')
    async def special_days_left(self, ctx):
        await ctx.send(get_exam_days_left())
    
    @cog_slash_managed(base='time', description='今年已經過了多少百分比')
    async def remain_time_left(self, ctx):
        today = datetime.now()
        year, month, day, hour, minute, second, week = today.timetuple()[:7]
        remain_time = get_remain_time(year, month, day, hour, minute, second)
        text = str(year) + '年已經過了' + str(remain_time)
        await ctx.send(text)

    @cog_slash_managed(base='time', description='現在時間',
        options=[create_option('format', '格式', 
            option_type=SlashCommandOptionType.STRING, 
            required=False, 
            choices=gen_list_of_option_choices(['year', 'month', 'day',
                                         'hour', 'minute', 'second', 'week',
                                         'date', 'time', 'datetime'])
            )])
    async def current(self, ctx, format: str = ''):
        args = self.parser.parse_args(format.split(' '))
        today = datetime.now()
        year, month, day, hour, minute, second, week = today.timetuple()[:7]

        if args.date:
            args.year = args.month = args.day = args.week = True
        
        if args.time:
            args.hour = args.minute = args.second = True

        # if specified any one of these we do not force concat whole string
        nooptions = not (args.year or args.month or args.day 
                or  args.hour or args.minute or args.second
                or  args.week)

        if args.datetime or nooptions :
            args.year = args.month = args.day \
                = args.hour = args.minute = args.second = True

        week_text = ['一', '二', '三', '四', '五', '六', '日']
        nowtime = '現在時間：'
        nowtime += f'{year}年'   if args.year   else ''
        nowtime += f'{month}月'  if args.month  else ''
        nowtime += f'{day}日'    if args.day    else ''
        nowtime += f'{hour}時'   if args.hour   else ''
        nowtime += f'{minute}分' if args.minute else ''
        nowtime += f'{second}秒' if args.second else ''
        nowtime += f' 星期{week_text[week]}' if args.week else ''
        await ctx.send(nowtime)
