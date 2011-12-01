#!/bin/bash

# Script to setup amd64-images on mptcp.info.ucl.ac.be
#
# arg_1 : kernel-version
# arg_2 : date

set -e

kernel_version=$1
DATE=$2

cd /tmp/

dpkg-sig --sign builder linux-*.deb

rm -f /var/www/repos/apt/debian/*.deb

mv *.deb /var/www/repos/apt/debian/

cd /var/www/repos/apt/debian/

reprepro includedeb orneic linux-*.deb

rm -f *.deb

