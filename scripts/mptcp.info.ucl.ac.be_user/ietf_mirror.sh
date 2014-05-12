#!/bin/bash

file=`basename $0`
logfile=/tmp/${file}.log
exec > $logfile 2>&1
#trap "cat $logfile | uuencode $logfile | mailx -s \"$file failed\" christoph.paasch@gmail.com ; exit 1" ERR

cd /home/ftp/
rsync -avz --delete /var/www/repos/apt/debian/dists mptcp-repo/dists/ 
rsync -avz --delete /var/www/repos/apt/debian/pool mptcp-repo/pool/
rsync --chmod=Fo-t -avz --delete www.ietf.org::everything-ftp ietf-full

