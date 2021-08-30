# Cutespirit Discord Bot
## Install and Run
```sh
git clone https://github.com/Cutespirit-Team/CutespiritDiscordBot

# install requirements
cd ./CutespiritDiscordBot/
pip install -r requirments.txt

# execute
cd ./src
python -m ctbot
```

## Config Sample
```ini
[bot]
# First run you need to change token to your bot token.
# you can create a bot from 
# https://discord.com/developers/applications
token = MTa4MjS3ASI ....
owner = 196207520585351180

[command]
enable_slash = true
general_prefix = !

[slash]
# regist all slash command for specific guilds.
# accept list of guilds seprate by comma.
all = 875896592052420618,196207701661843456

# regist specific slash command for specific guilds.
# <class name without 'Slash' prefix>.<method> = <guild_ids> 
example.ping = 866199579014987816,96230004047740928

# specific setting for guild
[guild_866199579014987816]
# only response message in specific channels (not work in slash commands)
responsible_channels = 866213047016882206,866977922929917972
```
## 關於我們
[Team Website](https://www.cutespirit.org) <br>
[Team Facebook](https://www.facebook.com/cutespirit05428/) <br>
[XiaTerShi YouTube](https://www.youtube.com/channel/UCPdpFDFOp3sPbZhRkaQVaQA) <br>
[XiaTerShi FaceBook](https://www.facebook.com/Tershi25648) <br>
[Tershi MailServer](https://mail.tershi.org) <br>
[Tershi Official WebSite](https://tershi.cutespirit.ml) <br>
[Tershi Gitbook](https://gitbook.tershi.cf) <br>
[Tershi Telegram](https://t.me/TershiXia) <br>
以上關於因為域名為免費域 因此隨時會網域更換！ <br>
Licence:© Cutespirit 2021 All right reversed 此程式除了「關於」頁面不可重製及發布之外，其餘頁面及功能可進行重製發布。
