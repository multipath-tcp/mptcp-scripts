#!/bin/bash

# Script to setup amd64-images on mptcp.info.ucl.ac.be
#
# arg_1 : kernel-version
# arg_2 : date

set -e

kernel_version=$1
DATE=$2

cd /tmp/

dpkg-sig --sign builder linux-headers-${kernel_version}_${DATE}_amd64.deb
dpkg-sig --sign builder linux-image-${kernel_version}-dbg_${DATE}_amd64.deb
dpkg-sig --sign builder linux-image-${kernel_version}_${DATE}_amd64.deb
dpkg-sig --sign builder linux-source-${kernel_version}_${DATE}_all.deb

mv *.deb /var/www/repos/apt/debian/

cd /var/www/repos/apt/debian/

reprepro includedeb orneic linux-headers-${kernel_version}_${DATE}_amd64.deb
reprepro includedeb orneic linux-image-${kernel_version}-dbg_${DATE}_amd64.deb
reprepro includedeb orneic linux-image-${kernel_version}_${DATE}_amd64.deb
reprepro includedeb orneic linux-source-${kernel_version}_${DATE}_all.deb

rm *.deb

