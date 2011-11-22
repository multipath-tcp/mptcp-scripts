#!/bin/bash
# This script installs opera browser on the Nokia N950 device

trap "echo 'ERROR occured - contact mptcp-dev@listes.uclouvain.be' ; exit 1" ERR

echo "When asked for the developer-password type in the one you configured"

#wget -N http://mptcp.info.ucl.ac.be/data/n950/operamobile_11.00-1_armel.deb

scp operamobile_11.00-1_armel.deb developer@192.168.2.15:
echo "Type the root password of the device (default: rootme):"
ssh developer@192.168.2.15 "devel-su root -c '/usr/bin/dpkg -i /home/developer/operamobile_11.00-1_armel.deb' ; rm operamobile_11.00-1_armel.deb"

#rm operamobile_11.00-1_armel.deb

if [ $(ssh developer@192.168.2.15 "cat /home/user/.config/operamobile/opera.ini |grep Proxy" | wc -l) != 0 ]
then
	echo "Proxy already configured for the Opera browser"
	exit 0
fi

read -p "Set Opera browser to use a proxy server? [Y/n]" response
if [ "$response" = "n" ]
then
	exit 0
fi

proxy=""
port=""
response=""
while [ "$response" != "y" ]
do
	read -p "The URL of your proxy server (default: mptcp.info.ucl.ac.be) [CTRL+C to cancel]:" proxy
	read -p "The port of your proxy server (default: 3128) [CTRL+C to cancel]:" port

	if [ "$proxy" = "" ]
	then
		proxy="mptcp.info.ucl.ac.be"
	fi
	if [ "$port" = "" ]
	then
		port="3128"
	fi
	

	read -p "Setting $proxy:$port as proxy. Is this correct? [y/n]:" response
done

read -p "Now, please start the opera-browser on your device and 'Accept' the license-agreement. When done, hit enter" response

ssh developer@192.168.2.15 "echo -e \"\n[Proxy]\nHTTP server=$proxy:$port\nUse HTTP=1\" >> /home/user/.config/operamobile/opera.ini"

