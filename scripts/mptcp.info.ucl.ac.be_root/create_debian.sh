#!/bin/bash

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Create and update the debian-repos
file=`basename $0`                                                                                                                                                                                                               
trap "mutt -s \"$file crontab-failure\" -- christoph.paasch@uclouvain.be < /tmp/${file}.log; exit 1" ERR                                                                                                                         

# Update sources 

cd /usr/src/mtcp/
git pull

# Compile everything

DATE=`date +%Y%m%d%H`
export CONCURRENCY_LEVEL=3
make-kpkg --initrd -j 2 --revision $DATE kernel_image kernel_headers

# Install new kernel on host-machine

kernel_version=`cat include/generated/utsrelease.h | cut -d \" -f 2`
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
echo "Maintainer: Christoph Paasch <christoph.paasch@uclouvain.be>" >> $ctrl
echo "Description: A meta-package for linux-mptcp" >> $ctrl

dpkg --build linux-mptcp
mv linux-mptcp.deb linux-mptcp_${DATE}_all.deb

rm -Rf linux-mptcp

# Update Debian-repositories
dpkg-sig --sign builder *.deb

mv *.deb /var/www/repos/apt/debian/

cd /var/www/repos/apt/debian/

reprepro includedeb squeeze *.deb

rm *.deb

# Copy vmlinux-file
cd /usr/src/mtcp
cp vmlinux /root/vmlinuxes/vmlinux_${kernel_version}_${DATE}
find /root/vmlinuxes -type f -mtime +90 -delete


# Reboot

/usr/bin/touch /root/rebooted
/sbin/reboot
