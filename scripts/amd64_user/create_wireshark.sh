#!/bin/bash

## build dependencies: 
# apt-get build-dep wireshark 
# apt-get install dpatch 

CONFIGURE_ARGS="--prefix=/usr --sysconfdir=/usr/share --datadir=/usr/share \
     --disable-static --libdir=/usr/lib/wireshark \
     --enable-warnings-as-errors=no --with-plugins=/usr/lib/wireshark/plugins \
     --with-lua=/usr/"
MAKE=${MAKE:-make}


if ! test -z "$1"; then
	REV="-r$1"
fi

BUILD_DIR=`mktemp -d`
SOURCE_DIR="${BUILD_DIR}/wireshark"

svn co ${REV} http://anonsvn.wireshark.org/wireshark/trunk/ ${SOURCE_DIR}

cd ${SOURCE_DIR}

./autogen.sh
./configure ${CONFIGURE_ARGS}
${MAKE} debian-package 

cd ${BUILD_DIR}

# cpaasch dependent:
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/*.deb"
scp *.deb root@mptcp.info.ucl.ac.be:/tmp/
scp $HOME/bin/setup_amd64.sh root@mptcp.info.ucl.ac.be:/tmp/
ssh root@mptcp.info.ucl.ac.be "/tmp/setup_amd64.sh squeeze"
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/setup_amd64.sh"
ssh root@mptcp.info.ucl.ac.be "cd /var/www/repos/apt/debian/ ; \
    reprepro copy orneic squeeze tshark ; \
    reprepro copy orneic squeeze wireshark ; \
    reprepro copy orneic squeeze wireshark-common ; \
    reprepro copy orneic squeeze wireshark-dev"

rm -rf ${BUILD_DIR}

