import discord
from discord.ext import commands
from ..utils import cog_slash_managed , gen_list_of_choices
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils import manage_components
from discord_slash.model import SlashCommandOptionType , ButtonStyle
from discord_ui import Button
from datetime import datetime
from ...version import shop , bot, author, team
import requests
import os
import json
from bs4 import BeautifulSoup
import string , secrets

# 達成功能:
# 一、顯示商品數
# 二、顯示商品類別
# 三、顯示商品資訊
# 四、下單功能(配合姓名、暱稱、電子郵件、電話、等...)
# 五、付款功能(不顯示個資，只顯示暱稱)
# 六、傳送郵件
# 七、跟WP進行連結，修改餘額、數據...等

tld = ['com', 'org', 'idv', 'gov', 'co', 'net', 'mil', 'edu']
shop_id = f'{shop["shop_id"]}'
shop_key = f'{shop["shop_key"]}'
iv = f'{shop["IV"]}'

def search(text):
    return 'NULL'

def getOrderCode():
    time = datetime.now()
    sec = ''.join(secrets.choice(string.ascii_letters) for _ in range(6))
    time = datetime.strftime(time,'%Y_%m_%d_%H_%M_%S_')
    return time + sec

def check_email(email):
    if '@' not in email:
        return 'Email無效，請重新輸入！'
    elif '.' not in email.split('@')[1]:
        return 'Email無效，請重新輸入！'
    else:
        count = 0
        text = ''
        for index in range(len(tld)):
            text += tld[index] + ' '
            if tld[index] in email:
                count +=1
        if count == 0:
            return 'Email 網域無效，目前只支持' + text
        else:
            return True
def check_price(price):
    if price <0:
        return '價格不能為負'
    else:
        return True
def check_product_name(product_name):
    return True

def getOrderInfo(OrderCode):
    path = '/var/www/html/pay2/' + OrderCode + '.data'
    f = open(path, encoding = 'utf-8')
    data = f.read()
    f.close()
    data = data.split(',')
    csv = data[0].split(':')[1]
    OrderCode = data[1].split(':')[1]
    TradeCode = data[2].split(':')[1]
    AMT = data[3].split(':')[1]
    PaymentType = data[4].split(':')[1]
    ExpireDate = data[5].split(':')[1]
    BankCode = data[6].split(':')[1]
    OrderInfo = [str(csv), str(OrderCode), str(TradeCode), str(AMT), str(PaymentType), str(ExpireDate), str(BankCode)]
    # CSV = 0, OrderCode = 1, TradeCode = 2, AMT = 3, PaymentType = 4, ExpireDate = 5, BankCode = 6
    return OrderInfo

class SlashPay(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @cog_slash_managed(description='查看訂單')
    async def check_order(self, ctx, order_number: str):
        OrderInfo = getOrderInfo(order_number)
        data = '訂單編號:' + OrderInfo[0] + ',交易編號:' + OrderInfo[1] + ',交易金額:' + OrderInfo[3] + ',付款方式:' + OrderInfo[4] + ',到期日:' + OrderInfo[5] + ',銀行代碼:' + OrderInfo[6]

        embed=discord.Embed(title=shop['name'], url=shop['url'], description=shop['description'], color=0x00ffd5)
        embed.set_author(name=team['name-eng'], url=team['url'], icon_url=bot['icon'])
        embed.set_thumbnail(url=shop['icon'])
#        embed.add_field(name='商品名稱', value=OrderInfo[], inline=True)
        embed.add_field(name='商品金額', value=OrderInfo[3], inline=True)
        embed.add_field(name='訂單編號', value=OrderInfo[1], inline=True)
        embed.add_field(name='交易編號', value=OrderInfo[2], inline=True)
        embed.add_field(name='銀行代號', value=OrderInfo[6], inline=True)
#        embed.add_field(name='電子郵件', value=OrderInfo[], inline=True)
        embed.add_field(name='到期時間', value=OrderInfo[5], inline=True)
        embed.add_field(name='付款方式', value=OrderInfo[4], inline=True)
        embed.set_footer(text='商店代碼: ' + shop_id)
        await ctx.send(embed=embed)

    @cog_slash_managed(description='商品下單')
    async def product_order(self, ctx , product_name: str, price: int, email: str):
        if check_email(email) != True or check_price(price) != True or check_product_name(product_name) != True:
            error = ''
            if check_email(email) != True:
                error += check_email(email) + ' '
            if check_price(price) != True:
                error += check_price(price) + ' '
            if check_product_name(product_name) != True:
                error += check_product_name(product_name)
            await ctx.send(error)
        else:
            OrderCode = getOrderCode()
            ITEMNAME = str(product_name)
            AMT = str(price)
            EMAIL = str(email)
            data  = '商店代號是:' + shop_id + ',您下單的是:' + product_name + ',價格是:' + str(price) + ',email:' + email + ',訂單編號:' + OrderCode
#            cmd = 'php -f /mnt/e/Bot/CutespiritDiscordBot/src/ctbot/command/slash/pay/getinfo.php py "' + str(product_name) + '" "' + str(price) + '" "' + str(email) + '" "' + str(shop_id) + '" "' + str(shop_key) + '" "' + str(iv) + '" "' + OrderCode + '"'
#output = os.popen(cmd)
#            print(output.read())
#            output = output.read().split('\n')
#            output = list(filter(None,output))
#            print(output[:])
#            ITEMNAME = output[0].split(':')[1]
#            AMT = output[1].split(':')[1]
#            EMAIL = output[2].split(':')[1]
#            TradeInfo = output[3].split(':')[1]
#            OrderCode = output[4].split(':')[1]
#            SHA256 = output[5].split(':')[1]
#            Version = output[6].split(':')[1]
#            TimeStamp = output[7].split(':')[1]
#            RespondType = output[8].split(':')[1]
#            LoginType = output[9].split(':')[1]
#            ReturnURL = output[10].split(':')[1:]
#            CustomerURL = output[11].split(':')[1:]
            URL = 'https://tershi.cutespirit.org/pay2/getinfo2.php?ITEMNAME=' + str(ITEMNAME) + '&AMT=' + str(AMT) + '&EMAIL=' + str(EMAIL) + '&OrderCode=' + str(OrderCode)
            data = data + ',網址是:' + URL
#            print(ITEMNAME, AMT, email, TradeInfo, SHA256 , Version, timestamp ,RespondType , LoginType, ReturnURL , CustomerURL )
#            shop_data = {
#                    'MerchantID' : shop_id, #商店代號
#                    'MerchantOrderNo' : OrderCode, #訂單編號
#                    'ItemDesc' : ITEMNAME, #商品名稱
#                    'Email' : EMAIL, #電子郵件
#                    'Amt' : price, #價格
#                    'TradeInfo' : TradeInfo,
#                    'TradeSha' : SHA256,
#                    'Version' : Version,
#                    'TimeStame' : TimeStamp,
#                    'RespondType' : RespondType,
#                    'LoginType' : LoginType,
#                    'ReturnURL' : ReturnURL,
#                    'CustomerURL' : CustomerURL
#            }
#           tershislove = requests.post('https://ccore.newebpay.com/MPG/mpg_gateway', data = shop_data)
#           print(SHA256) 
#           print(tershislove.text)
            
            embed=discord.Embed(title=shop['name'], url=shop['url'], description=shop['description'], color=0x00ffd5)
            embed.set_author(name=team['name-eng'], url=bot['url'], icon_url=shop['icon'])
            embed.set_thumbnail(url=shop['icon'])
            embed.add_field(name='商品名稱', value=ITEMNAME, inline=True)
            embed.add_field(name='商品金額', value=AMT, inline=True)
            embed.add_field(name='訂單編號', value=OrderCode, inline=True)
#            embed.add_field(name='交易編號', value=TradeCode, inline=True)
#            embed.add_field(name='銀行代號', value=BankCode, inline=True)
            embed.add_field(name='電子郵件', value=EMAIL, inline=True)
            embed.add_field(name='訂單網址(進去付款)', value=URL, inline=True)
#            embed.add_field(name='到期時間', value=ExpireDate, inline=True)
#           TODO:Do a button that can check if paid or not
#            embed.add_field(name='付款方式', value=PaymentType, inline=True)
#            embed.set_footer(text='商店代碼: ' + shop_id)
            await ctx.send(embed=embed)
#           await ctx.send(data)
