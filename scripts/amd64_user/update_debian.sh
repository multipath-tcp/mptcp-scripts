#!/bin/bash

# Script on the amd64-host to compile amd64-images and update them on mptcp.info.ucl.ac.be
file=`basename $0`
host=`cat /etc/hostname`
trap "mutt -s \"$host $file crontab-failure\" -- christoph.paasch@uclouvain.be < /tmp/${file}.log; exit 1" ERR

if [ $# -eq 1 ]
then
	FLAV=$1
else
	FLAV="mptcp"
fi

cd /usr/src

rm -f *.deb

cd /usr/src/mptcp
rm -Rf debian/linux-*
git pull

# Create mptcp image and header package
export CONCURRENCY_LEVEL=3
fakeroot debian/rules clean
fakeroot debian/rules debian/control
skipabi=true skipmodule=true fakeroot debian/rules binary-$FLAV
kernel_version=`ls -1 -t debian/linux-image-*/lib/modules/ | head -n 1 | tail -n 1`
version=`cat debian/linux-image-${kernel_version}/DEBIAN/control | grep Version | cut -d . -f 4`


echo "======================================================================================"
echo $kernel_version
echo $version

cd /usr/src

# Create meta-package
rm -Rf linux-$FLAV

mkdir linux-$FLAV
mkdir linux-$FLAV/DEBIAN
chmod -R a-s linux-$FLAV
ctrl="linux-${FLAV}/DEBIAN/control"
touch $ctrl

echo "Package: linux-${FLAV}" >> $ctrl
echo "Version: ${version}" >> $ctrl
echo "Section: main" >> $ctrl
echo "Priority: optional" >> $ctrl
echo "Architecture: all" >> $ctrl
echo "Depends: linux-headers-${kernel_version}, linux-image-${kernel_version}" >> $ctrl
echo "Installed-Size:" >> $ctrl
echo "Maintainer: Christoph Paasch <christoph.paasch@uclouvain.be>" >> $ctrl
echo "Description: A meta-package for linux-${FLAV}" >> $ctrl

dpkg --build linux-$FLAV
mv linux-${FLAV}.deb linux-${FLAV}_${version}_all.deb

# Install everything
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/*.deb"
scp -C *.deb root@mptcp.info.ucl.ac.be:/tmp/
scp /root/bin/setup_amd64.sh root@mptcp.info.ucl.ac.be:/tmp/

ssh root@mptcp.info.ucl.ac.be "/tmp/setup_amd64.sh precise"
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/setup_amd64.sh"

rm *.deb

# Copy vmlinux-file
cd /usr/src/mptcp
cp debian/build/build-${FLAV}/vmlinux /root/vmlinuxes/vmlinux_${kernel_version}_${version}
rm /root/vmlinuxes/vmlinux
ln -s /root/vmlinuxes/vmlinux_${kernel_version}_${version} /root/vmlinuxes/vmlinux
find /root/vmlinuxes -type f -mtime +90 -delete

