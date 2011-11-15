#!/bin/bash

set -e

# FIRST, extract the ape-algo from the OneClickFlasher

echo "Extracting ape-algo"

EXTRACT="./extract_flash/"

rm -Rf $EXTRACT
mkdir $EXTRACT

ARCHIVE=`head -c 10000 "Linux_OCF_39-5_RM680-RM680-OEM1.bin" | awk '/^__ARCHIVE_BELOW__/ {print NR + 1; exit 0; }'`

tail -n +$ARCHIVE "Linux_OCF_39-5_RM680-RM680-OEM1.bin" | tar -C $EXTRACT -xf -

N950='192.168.2.15'

echo "If a previous flash failed, and your phone doesn't boot anymore, type 'Y'."
echo "Then, it will only flash the image. Otherwise we will also update the modules and need a working phone"
read ans

if [ "$ans" != "Y" ] ; then
	echo "First, we test if the phone is at least connected via usb"
	ping -c 1 $N950
	scp clean_modules.tar developer@$N950:modules.tar
	scp n950_insmod.sh developer@$N950:
	ssh developer@$N950 "chmod a+x ./n950_insmod.sh"

	echo "Now installing the modules - type in the default-password 'rootme'"

	ssh developer@$N950 "devel-su root /home/developer/n950_insmod.sh"

	ssh developer@$N950 rm ./n950_insmod.sh
	ssh developer@$N950 rm ./modules.tar
fi

sudo flasher -f -a ./extract_flash/img.bin -k clean_zImage 

rm -Rf $EXTRACT
