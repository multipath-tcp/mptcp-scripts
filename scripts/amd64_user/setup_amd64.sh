#!/bin/bash

# Script to setup amd64-images on mptcp.info.ucl.ac.be
#
# arg_1 : kernel-version
# arg_2 : date

kernel_version=$1
DATE=$2

cd /tmp/

dpkg-sig --sign builder linux-headers-${kernel_version}_${DATE}_amd64.deb
dpkg-sig --sign builder linux-image-${kernel_version}_${DATE}_amd64.deb

mv *.deb /var/www/repos/apt/debian/

cd /var/www/repos/apt/debian/

reprepro includedeb squeeze linux-headers-${kernel_version}_${DATE}_amd64.deb
reprepro includedeb squeeze linux-image-${kernel_version}_${DATE}_amd64.deb

rm *.deb

