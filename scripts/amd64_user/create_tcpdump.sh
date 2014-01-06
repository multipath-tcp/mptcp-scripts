#!/bin/bash

set -e
[ $# -ne 2 ] && echo "Usage: $0 [distribution] [arch]" && exit

DIST=$1
AR=$2
BASE="/tmp/tcpdump"
CTRL="${BASE}/DEBIAN/control"
DATE=`date +%Y%m%d%H%M`

cd $HOME/workspace/linux/tcpdump/
#git pull

rm -Rf $BASE
mkdir $BASE

export ARCH=$AR
make
DESTDIR=${BASE} make install

mkdir $BASE/DEBIAN

echo "Package: tcpdump" >> $CTRL
echo "Version: 5-${DATE}-${DIST}" >> $CTRL
echo "Architecture: $AR" >> $CTRL
echo "Maintainer: Christoph Paasch <christoph.paasch@uclouvain.be>" >> $CTRL
#echo "Installed-Size: 1092" >> $CTRL
echo "Depends: libc6 (>= 2.14), libpcap0.8 (>= 1.2.1), libssl1.0.0 (>= 1.0.0), libdnet (>= 2.61)" >> $CTRL
echo "Section: net" >> $CTRL
echo "Priority: important" >> $CTRL
echo "Homepage: http://multipath-tcp.org" >> $CTRL
echo "Description: A powerful tool for network monitoring and data acquisition" >> $CTRL
echo " ." >> $CTRL
echo " This tool is extended for MultiPath TCP!!!" >> $CTRL

cd /tmp/
dpkg -b tcpdump

# install everything
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/*.deb"
scp *.deb root@mptcp.info.ucl.ac.be:/tmp/
scp $HOME/bin/setup_amd64.sh root@mptcp.info.ucl.ac.be:/tmp/
ssh root@mptcp.info.ucl.ac.be "/tmp/setup_amd64.sh ${DIST}"
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/setup_amd64.sh"

rm *.deb

