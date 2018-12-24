#!/bin/bash

crypt=/usr/bin/hgycrypt
decrypt=/usr/bin/hgydecrypt
file=~/.hgyuser

echo "please select: 1.install 2.update 3.uninstall 4.changeusercode"
read mode

if [ $mode -eq 1 ];then
	if [ ! -d "$crypt" ];then
		wget http://linux.heguangyu.net/hgycrypt
		chmod +x hgycrypt
		sudo mv hgycrypt /usr/bin
	fi

	if [ ! -d "$decrypt" ];then
		wget http://linux.heguangyu.net/hgydecrypt
		chmod +x hgydecrypt
		mv hgydecrypt /usr/bin
	fi

	if [ ! -f "$file" ];then
		echo "first time using the script plz input your usercode(only number):"
		read user
		echo "${user}" > ~/.hgyuser
	fi
elif [ $mode -eq 2 ];then
	wget http://linux.heguangyu.net/hgycrypt
	chmod +x hgycrypt
	sudo mv hgycrypt /usr/bin
	wget http://linux.heguangyu.net/hgydecrypt
	chmod +x hgydecrypt
	mv hgydecrypt /usr/bin
elif [ $mode -eq 3 ]; then
	sudo rm -rf /usr/bin/hgycrypt
	sudo rm -rf /usr/bin/hgydecrypt
	sudo rm -rf ~/.hgyuser
	sudo rm -rf ~/hgycrypted-*
elif [ $mode -eq 4 ]; then
	echo "input your usercode(only number):"
	read user
	echo "${user}" > ~/.hgyuser
fi
