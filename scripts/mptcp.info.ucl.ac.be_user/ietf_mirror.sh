#!/bin/bash

file=`basename $0`
logfile=/tmp/${file}.log
exec > $logfile 2>&1
trap "cat $logfile | uuencode $logfile | mail -s \"$file failed\" christoph.paasch@gmail.com ; exit 1" ERR

cd /home/ftp/
rsync -avz --delete www.ietf.org::everything-ftp ietf-full/

