#!/bin/bash

# Create and update the debian-repos
file=`basename $0`
host=`cat /etc/hostname`
trap "mutt -s \"$host $file crontab-failure\" -- christoph.paasch@uclouvain.be < /tmp/${file}.log; exit 1" ERR                                                                                                                         

cd $HOME
rm -f *.deb

# Update sources 

cd $HOME/mptcp
git pull

# Compile everything

DATE=`date +%Y%m%d%H`
export CONCURRENCY_LEVEL=3
fakeroot make-kpkg --initrd -j 2 --revision $DATE kernel_image kernel_headers

kernel_version=`cat include/generated/utsrelease.h | cut -d \" -f 2`

cd ..

# Create meta-package
#rm -Rf linux-mptcp

#mkdir linux-mptcp
#mkdir linux-mptcp/DEBIAN
#chmod -R a-s linux-mptcp
#ctrl="linux-mptcp/DEBIAN/control"
#touch $ctrl

#echo "Package: linux-mptcp" >> $ctrl
#echo "Version: ${DATE}" >> $ctrl
#echo "Section: main" >> $ctrl
#echo "Priority: optional" >> $ctrl
#echo "Architecture: all" >> $ctrl
#echo "Depends: linux-headers-${kernel_version}, linux-image-${kernel_version}" >> $ctrl
#echo "Installed-Size:" >> $ctrl
#echo "Maintainer: Christoph Paasch <christoph.paasch@uclouvain.be>" >> $ctrl
#echo "Description: A meta-package for linux-mptcp" >> $ctrl

#dpkg --build linux-mptcp
#mv linux-mptcp.deb linux-mptcp_${DATE}_all.deb

# Install everything
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/*.deb"
scp *.deb root@mptcp.info.ucl.ac.be:/tmp/
scp $HOME/bin/setup_amd64.sh root@mptcp.info.ucl.ac.be:/tmp/

ssh root@mptcp.info.ucl.ac.be "/tmp/setup_amd64.sh squeeze"
ssh root@mptcp.info.ucl.ac.be "rm -f /tmp/setup_amd64.sh"

rm *.deb

# Copy vmlinux-file
cd $HOME/mptcp
cp vmlinux $HOME/vmlinuxes/vmlinux_${kernel_version}_${DATE}
find $HOME/vmlinuxes -type f -mtime +90 -delete

