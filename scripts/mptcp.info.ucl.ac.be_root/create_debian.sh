#!/bin/bash

# Create and update the debian-repos
file=`basename $0`                                                                                                                                                                                                               
trap "mutt -s \"$file crontab-failure\" -- christoph.paasch@uclouvain.be < /tmp/${file}.log; exit 1" ERR                                                                                                                         

# Update sources 

cd /usr/src/mtcp/
git pull

# Compile everything

DATE=`date +%Y%m%d`
export CONCURRENCY_LEVEL=3
make-kpkg --initrd -j 2 --revision $DATE kernel_image kernel_headers kernel_debug

# Install new kernel on host-machine

kernel_version=`ls debian/linux-image-*/lib/modules/`
make install modules_install
if [ -f /boot/initrd.img-${kernel_version} ];
then
	update-initramfs -u -k $kernel_version
else
	update-initramfs -c -k $kernel_version
fi

# Update Debian-repositories

cd ..

dpkg-sig --sign builder linux-headers-${kernel_version}_${DATE}_i386.deb
dpkg-sig --sign builder linux-image-${kernel_version}-dbg_${DATE}_i386.deb
dpkg-sig --sign builder linux-image-${kernel_version}_${DATE}_i386.deb

mv *.deb /var/www/repos/apt/debian/

cd /var/www/repos/apt/debian/

reprepro includedeb squeeze linux-headers-${kernel_version}_${DATE}_i386.deb
reprepro includedeb squeeze linux-image-${kernel_version}-dbg_${DATE}_i386.deb
reprepro includedeb squeeze linux-image-${kernel_version}_${DATE}_i386.deb

rm *.deb

# Reboot

/usr/bin/touch /root/rebooted
/sbin/reboot
