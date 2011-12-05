#!/bin/bash

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Create and update the debian-repos
file=`basename $0`                                                                                                                                                                                                               
trap "mutt -s \"$file crontab-failure\" -- christoph.paasch@uclouvain.be < /tmp/${file}.log; exit 1" ERR                                                                                                                         

# Update sources 

cd /usr/src/mtcp/
git pull

# Compile everything

DATE=`date +%Y%m%d`
export CONCURRENCY_LEVEL=3
make-kpkg --initrd -j 2 --revision $DATE kernel_image kernel_headers

# Install new kernel on host-machine

kernel_version=`ls debian/linux-image-*/lib/modules/`
make install modules_install
if [ -f /boot/initrd.img-${kernel_version} ];
then
	update-initramfs -u -k $kernel_version
else
	update-initramfs -c -k $kernel_version
fi

cd ..

# Create meta-package
rm -Rf linux-mptcp

mkdir linux-mptcp
mkdir linux-mptcp/DEBIAN
chmod -R a-s linux-mptcp
ctrl="linux-mptcp/DEBIAN/control"
touch $ctrl

echo "Package: linux-mptcp" >> $ctrl
echo "Version: ${DATE}" >> $ctrl
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
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/*.deb"
scp *.deb root@mptcp.info.ucl.ac.be:/tmp/
scp /root/bin/setup_amd64.sh root@mptcp.info.ucl.ac.be:/tmp/

ssh root@mptcp.info.ucl.ac.be "/tmp/setup_amd64.sh"
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/setup_amd64.sh"

rm *.deb

# Copy vmlinux-file
cd /usr/src/mptcp
cp debian/build/build-mptcp/vmlinux /root/vmlinuxes/vmlinux_${kernel_version}_${version}
find /root/vmlinuxes -type f -mtime +90 -delete

