#!/bin/bash

USER=`whoami`

sudo tunctl -u $USER -t tap2

sudo ifconfig tap2 10.2.1.1 netmask 255.255.255.0 up

sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -s 10.0.0.0/8 ! -d 10.0.0.0/8 -j MASQUERADE

sudo chmod 666 /dev/net/tun

./vmlinux ubda=fs_server mem=256M umid=umlA eth0=tuntap,tap2

sudo tunctl -d tap2

sudo iptables -t nat -D POSTROUTING -s 10.0.0.0/8 ! -d 10.0.0.0/8 -j MASQUERADE

