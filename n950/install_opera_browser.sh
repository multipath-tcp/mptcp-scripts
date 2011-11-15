#!/bin/bash
# This script installs opera browser on the Nokia N950 device

set -e

wget -N http://mptcp.info.ucl.ac.be/data/n950/operamobile_11.00-1_armel.deb

scp operamobile_11.00-1_armel.deb developer@192.168.2.15:
echo "Type the root password of the device (default: rootme):"
ssh developer@192.168.2.15 "devel-su root -c '/usr/bin/dpkg -i /home/developer/operamobile_11.00-1_armel.deb'"

read -p "Set Opera browser to use mptcp.info.ucl.ac.be as a proxy server? (Make sure you have a proxy account there, or request one from the mptcp developers mailing list) [Y/n]" response
if [ "$response" == "n" ]
then
	exit 0
fi

scp set-proxy-for-opera.sh developer@192.168.2.15:
echo "Type the root password of the device (default: rootme):"
ssh developer@192.168.2.15 "devel-su root '/home/developer/set-proxy-for-opera.sh'"
ssh developer@192.168.2.15 "rm set-proxy-for-opera.sh"
