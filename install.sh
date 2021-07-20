#!/bin/bash
file="/srv/http"
if [ -f "$file" ]
then
	echo "$file存在正在進行安裝..."
	mkdir yt
	sudo mkdir /srv/http/yt
	sudo pacman -Syy python3 python3-pip
	pip3 install discord.py pprint
	echo "安裝完成... Installation Finished..."
else
	echo "找不到$file"
	file1="/var/www/html"
	if [ -f "$file1" ]
	then
		echo "$file存在正在進行安裝..."
		sudo apt update&&sudo apt upgrade -y
		sudo apt install python3 python3-pip
		pip3 install discord.py pprint
		echo "安裝完成... Installation Finished..."
	else
		echo "找不到$file"
		echo "無法判別您的系統"
	fi
fi
