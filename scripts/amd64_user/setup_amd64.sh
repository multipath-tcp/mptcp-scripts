#!/bin/bash

# Script to setup amd64-images on mptcp.info.ucl.ac.be
#
# arg_1 : distribution

set -e

cd /tmp/

dpkg-sig --sign builder *.deb

rm -f /var/www/repos/apt/debian/*.deb

mv *.deb /var/www/repos/apt/debian/

cd /var/www/repos/apt/debian/

reprepro includedeb $1 *.deb

rm -f *.deb

