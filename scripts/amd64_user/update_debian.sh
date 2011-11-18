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

DATE=`date +%Y%m%d`
export CONCURRENCY_LEVEL=3
fakeroot make-kpkg --initrd -j 2 --revision $DATE kernel_image kernel_headers
kernel_version=`ls debian/linux-image-*/lib/modules/`

cd /usr/src
scp *.deb root@mptcp.info.ucl.ac.be:/tmp/

scp /root/bin/setup_amd64.sh root@mptcp.info.ucl.ac.be:/tmp/

ssh root@mptcp.info.ucl.ac.be "/tmp/setup_amd64.sh $kernel_version $DATE"

ssh root@mptcp.info.ucl.ac.be "rm /tmp/setup_amd64.sh"

rm *.deb
