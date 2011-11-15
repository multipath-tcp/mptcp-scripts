#!/bin/sh

set -e

cp /home/developer/modules.tar /lib/modules/

cd /lib/modules/
FILE=`basename modules.tar`

mkdir tmp
cd tmp
tar -xf /lib/modules/modules.tar
VER=`ls -l -t /lib/modules/tmp/ | sed -n 2p | awk '{ print $NF }'`
cd /lib/modules/
rm -Rf $VER
mv tmp/$VER .
rm -Rf tmp
/sbin/depmod $VER
rm /lib/modules/modules.tar

