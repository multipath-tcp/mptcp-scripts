#!/bin/bash

set -e

[ $# -ne 2 ] && echo "Usage: $0 [distribution] [arch]" && exit

AR=$2
DIST=$1
BASE="/tmp/net-tools"
CTRL="${BASE}/DEBIAN/control"
DATE=`date +%Y%m%d%H%M`

cd $HOME/workspace/linux/net-tools/
git pull

rm -Rf $BASE
mkdir $BASE

export ARCH=$AR
make clean
make
DESTDIR=${BASE} make install

mkdir $BASE/DEBIAN

echo "Package: net-tools" >> $CTRL
echo "Version: ${DATE}-${DIST}" >> $CTRL
echo "Architecture: ${AR}" >> $CTRL
echo "Maintainer: Christoph Paasch <christoph.paasch@uclouvain.be>" >> $CTRL
#echo "Installed-Size: 1092" >> $CTRL
echo "Depends: libc6 (>= 2.11)" >> $CTRL
echo "Conflicts: ja-trans (<= 0.8-2)" >> $CTRL
echo "Replaces: ja-trans (<= 0.8-2), netbase (<< 4.00)" >> $CTRL
echo "Section: net" >> $CTRL
echo "Priority: important" >> $CTRL
echo "Homepage: http://multipath-tcp.org" >> $CTRL
echo "Description: The NET-3 networking toolkit" >> $CTRL
echo " This package includes the important tools for controlling the network" >> $CTRL
echo " subsystem of the Linux kernel.  This includes arp, ifconfig, netstat," >> $CTRL
echo " rarp, nameif and route.  Additionally, this package contains utilities" >> $CTRL
echo " relating to particular network hardware types (plipconfig, slattach," >> $CTRL
echo " mii-tool) and advanced aspects of IP configuration (iptunnel, ipmaddr)." >> $CTRL
echo " ." >> $CTRL
echo " This tool is extended for MultiPath TCP!!!" >> $CTRL

cd /tmp/
dpkg -b net-tools

# install everything
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/*.deb"
scp *.deb root@mptcp.info.ucl.ac.be:/tmp/
scp $HOME/bin/setup_amd64.sh root@mptcp.info.ucl.ac.be:/tmp/
ssh root@mptcp.info.ucl.ac.be "/tmp/setup_amd64.sh ${DIST}"
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/setup_amd64.sh"

rm *.deb

