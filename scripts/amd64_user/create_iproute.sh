#!/bin/bash

set -e
[ $# -ne 2 ] && echo "Usage: $0 [distribution] [arch]" && exit

DIST=$1
AR=$2
BASE="/tmp/iproute2"
PKG="iproute2"
CTRL="${BASE}/DEBIAN/control"
DATE=`date +%Y%m%d%H%M`

cd /root/iproute-mptcp
git pull

rm -Rf $BASE
mkdir $BASE

export ARCH=$AR
make clean
make
DESTDIR=$BASE make install

mkdir $BASE/DEBIAN

echo "Package: $PKG" >> $CTRL
echo "Version: 3.16.${DATE}-${DIST}" >> $CTRL
echo "Architecture: $AR" >> $CTRL
echo "Maintainer: Christoph Paasch <christoph.paasch@gmail.com>" >> $CTRL
#echo "Installed-Size: 1092" >> $CTRL
echo "Depends: libc6 (>= 2.14), libdb5.3, libselinux1 (>= 2.0.15)" >> $CTRL
echo "Conflicts: arpd, iproute" >> $CTRL
echo "Replaces: iproute" >> $CTRL
echo "Provides: arpd" >> $CTRL
echo "Section: net" >> $CTRL
echo "Priority: important" >> $CTRL
echo "Homepage: http://mulitpath-tcp.org" >> $CTRL
echo "Description: networking and traffic control tools" >> $CTRL
echo " The iproute suite, also known as iproute2, is a collection of" >> $CTRL
echo " utilities for networking and traffic control." >> $CTRL
echo " ." >> $CTRL
echo " These tools communicate with the Linux kernel via the (rt)netlink" >> $CTRL
echo " interface, providing advanced features not available through the" >> $CTRL
echo " legacy net-tools commands 'ifconfig' and 'route'." >> $CTRL
echo " ." >> $CTRL
echo " This tool is extended for MultiPath TCP!!!" >> $CTRL

cd /tmp/
dpkg -b $PKG


echo "DONE FIRST PART"

BASE="/tmp/iproute"
rm -Rf $BASE
mkdir $BASE
mkdir $BASE/DEBIAN
CTRL="${BASE}/DEBIAN/control"
echo "Package: iproute" >> $CTRL
echo "Version: 1:3.16.${DATE}-${DIST}" >> $CTRL
echo "Architecture: $AR" >> $CTRL
echo "Maintainer: Christoph Paasch <christoph.paasch@gmail.com>" >> $CTRL
echo "Depends: iproute2" >> $CTRL
echo "Section: net" >> $CTRL
echo "Priority: important" >> $CTRL
echo "Description: transitional dummy package for iproute2" >> $CTRL
echo " This is a transitional dummy package to get upgrading systems to install the iproute2 package. It can safely be removed." >> $CTRL
echo "Homepage: http://multipath-tcp.org" >> $CTRL

cd /tmp/
dpkg -b iproute

