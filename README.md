# Cutespirit Discord Bot - NUTC
## Install and Run
```sh
git clone https://github.com/Cutespirit-Team/CutespiritDiscordBot
cd ./CutespiritDiscordBot/
git checkout nutc

# install requirements
pip install -r requirments.txt

# execute
cd ./src
python -m ctbot
```

## Config Sample
[Configuration Example](config-example/)
bot.int
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
[Team Facebook](https://fb.cutespirit.org) <br>
[Team Discord](https://discord.cutespirit.org)<br>
[Team Telegram](https://telegram.cutespirit.org)<br>
[Cutespirit-SHOP](https://shop.cutespirit.org)<br>
[Cutespirit Discord Bot](https://dcbot.cutespirit.org)<br>

# 趨勢
[![Stargazers over time](https://starchart.cc/Cutespirit-Team/CutespiritDiscordBot.svg)](https://starchart.cc/Cutespirit-Team/CutespiritDiscordBot)


Licence:© Cutespirit 2022 All right reversed 此程式除了「關於」頁面不可重製及發布之外，其餘頁面及功能可進行重製發布。
