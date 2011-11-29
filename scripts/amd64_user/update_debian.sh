#!/bin/bash

# Script on the amd64-host to compile amd64-images and update them on mptcp.info.ucl.ac.be
file=`basename $0`
trap "mutt -s \"$file crontab-failure\" -- christoph.paasch@uclouvain.be < /tmp/${file}.log; exit 1" ERR

cd /usr/src

files=$(ls *.deb 2> /dev/null | wc -l)
if [ "$files" != "0" ] 
then
	rm *.deb
fi

cd /usr/src/mptcp
git pull

# Create mptcp image and header package
export CONCURRENCY_LEVEL=3
skipabi=true skipmodule=true fakeroot debian/rules binary-mptcp
kernel_version=`ls -l -t debian/linux-image-*/lib/modules/ | head -n 2 | tail -n 1 | cut -d \  -f 8`
version=`cat debian/linux-image-${kernel_version}/DEBIAN/control | grep Version | cut -d . -f 4`

cd /usr/src

# Create meta-package
rm -Rf linux-mptcp

mkdir linux-mptcp
mkdir linux-mptcp/DEBIAN
chmod -R a-s linux-mptcp
ctrl="linux-mptcp/DEBIAN/control"
touch $ctrl

echo "Package: linux-mptcp" >> $ctrl
echo "Version: ${version}" >> $ctrl
echo "Section: main" >> $ctrl
echo "Priority: optional" >> $ctrl
echo "Architecture: all" >> $ctrl
echo "Depends: linux-headers-${kernel_version}, linux-image-${kernel_version}" >> $ctrl
echo "Installed-Size:" >> $ctrl
echo "Maintainer: Christoph Paasch" >> $ctrl
echo "Description: A meta-package for linux-mptcp" >> $ctrl

dpkg --build linux-mptcp
mv linux-mptcp.deb linux-mptcp_${version}_all.deb

# Install everything
ssh root@mptcp.info.ucl.ac.be "rm /tmp/*.deb"
scp *.deb root@mptcp.info.ucl.ac.be:/tmp/
scp /root/bin/setup_amd64.sh root@mptcp.info.ucl.ac.be:/tmp/

ssh root@mptcp.info.ucl.ac.be "/tmp/setup_amd64.sh"
ssh root@mptcp.info.ucl.ac.be "rm /tmp/setup_amd64.sh"

rm *.deb

# Copy vmlinux-file
cd /usr/src/mptcp
cp debian/build/build-mptcp/vmlinux /root/vmlinuxes/vmlinux_${kernel_version}_${version}
find /root/vmlinuxes -type f -mtime +90 -delete

