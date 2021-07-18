#!/bin/bash
file="/srv/http"
if [ -f "$file" ]
then
	echo "$file存在正在進行安裝..."
	mkdir yt
	sudo mkdir /srv/http/yt
	sudo pacman -Syy python3 python3-pip httpd
	pip3 install discord.py pprint
	sudo systemctl start httpd
	sudo chown USER:USER /srv/http/yt
	echo "安裝完成... Installation Finished..."
else
	echo "找不到$file"
	file1="/var/www/html"
	if [ -f "$file1" ]
	then
		echo "$file存在正在進行安裝..."
		sudo apt update&&sudo apt upgrade -y
		sudo apt install httpd python3 python3-pip
		pip3 install discord.py pprint
		sudo mkdir /var/www/html/yt
		sudo chown USER:USER /var/www/html/yt
		sudo service httpd start
		echo "安裝完成... Installation Finished..."
	else
		echo "找不到$file"
		echo "無法判別您的系統"
	fi
fi
