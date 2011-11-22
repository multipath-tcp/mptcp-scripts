#!/bin/bash

trap "echo 'ERROR occured - contact mptcp-dev@listes.uclouvain.be' ; exit 1" ERR

# FIRST, extract the ape-algo from the OneClickFlasher

echo "Extracting ape-algo"

EXTRACT="./extract_flash/"

rm -Rf $EXTRACT
mkdir $EXTRACT

ARCHIVE=`head -c 10000 "Linux_OCF_39-5_RM680-RM680-OEM1.bin" | awk '/^__ARCHIVE_BELOW__/ {print NR + 1; exit 0; }'`

tail -n +$ARCHIVE "Linux_OCF_39-5_RM680-RM680-OEM1.bin" | tar -C $EXTRACT -xf -

N950='192.168.2.15'
echo "First, we test if the phone is at least connected via usb"
ping -c 1 $N950
scp modules.tar developer@$N950:
scp n950_insmod.sh developer@$N950:
ssh developer@$N950 "chmod a+x ./n950_insmod.sh"

echo "=========================================================="
echo "Now installing the modules."
echo "First type your developer-password."
echo "Then type in the default root-password 'rootme'"

ssh developer@$N950 "devel-su root /home/developer/n950_insmod.sh" 

ssh developer@$N950 rm ./n950_insmod.sh
ssh developer@$N950 rm ./modules.tar

echo "=========================================================="
echo "Now, you may get prompted for your host's password to access sudo"
sudo flasher -f -a ./extract_flash/img.bin -k zImage 

rm -Rf $EXTRACT
