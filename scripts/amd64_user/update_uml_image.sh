#!/bin/bash

file=`basename $0`
logfile=/tmp/${file}.log
exec > $logfile 2>&1
trap "cat $logfile | uuencode $logfile | mail -s \"$file failed\" christoph.paasch@gmail.com ; exit 1" ERR

cd $HOME/uml/mptcp
git checkout mptcp_trunk
git pull

make -j 2 O=../build_uml/ ARCH=um

cd ..

scp -C build_uml/vmlinux cpaasch@mptcp.info.ucl.ac.be:uml/vmlinux_64
scp -C fs_client_64.bz2 cpaasch@mptcp.info.ucl.ac.be:uml/
scp -C fs_server_64.bz2 cpaasch@mptcp.info.ucl.ac.be:uml/


