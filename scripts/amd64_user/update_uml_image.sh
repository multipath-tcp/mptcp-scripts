#!/bin/bash

file=`basename $0`
logfile=/tmp/${file}.log
exec > $logfile 2>&1
trap "cat $logfile | uuencode $logfile | mail -s \"$file failed\" christoph.paasch@gmail.com ; exit 1" ERR

cd $HOME/mptcp
git pull

make -j 2 ARCH=um

scp -C vmlinux cpaasch@multipath-tcp.org:uml/vmlinux_64
scp -C ../uml/fs_client_64.bz2 cpaasch@multipath-tcp.org:uml/
scp -C ../uml/fs_server_64.bz2 cpaasch@multipath-tcp.org:uml/


