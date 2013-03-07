#!/bin/bash

set -e
[ $# -ne 1 ] && echo "Usage: $0 [distribution]" && exit

DIST=$1
AR=amd64
BASE="/tmp/iproute"
CTRL="${BASE}/DEBIAN/control"
DATE=`date +%Y%m%d%H%M`

cd $HOME/workspace/linux/iproute2/
git pull

rm -Rf $BASE
mkdir $BASE

export ARCH=$AR
make
DESTDIR=$BASE make install

mkdir $BASE/DEBIAN

echo "Package: iproute" >> $CTRL
echo "Version: ${DATE}-${DIST}" >> $CTRL
echo "Architecture: $AR" >> $CTRL
echo "Maintainer: Christoph Paasch <christoph.paasch@uclouvain.be>" >> $CTRL
#echo "Installed-Size: 1092" >> $CTRL
echo "Depends: libc6 (>= 2.11), libdb5.1" >> $CTRL
echo "Conflicts: arpd, iproute" >> $CTRL
echo "Provides: arpd" >> $CTRL
echo "Section: net" >> $CTRL
echo "Priority: important" >> $CTRL
echo "Homepage: http://mptcp.info.ucl.ac.be" >> $CTRL
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
dpkg -b iproute

# install everything
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/*.deb"
scp *.deb root@mptcp.info.ucl.ac.be:/tmp/
scp $HOME/bin/setup_amd64.sh root@mptcp.info.ucl.ac.be:/tmp/
ssh root@mptcp.info.ucl.ac.be "/tmp/setup_amd64.sh ${DIST}"
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/setup_amd64.sh"

ssh root@mptcp.info.ucl.ac.be "cd /var/www/repos/apt/debian/ ; reprepro -A $AR copy precise ${DIST} iproute"

rm *.deb

