#!/bin/bash

# Create and maintain the snapshots
file=`basename $0`                                                                                                                                                                                                               
trap "mutt -s \"$file crontab-failure\" -- christoph.paasch@uclouvain.be < /tmp/${file}.log; exit 1" ERR                                                                                                                         

cd $HOME/mtcp/

git pull

DATE=`date +%Y_%m_%d`
git archive --format=tar --prefix=mptcp_$DATE/ HEAD | gzip > mptcp_$DATE.tar.gz
mv mptcp_$DATE.tar.gz /var/www/snapshots/

# Delete old snaphots
find /var/www/snapshots/ -type f -mtime +31 -delete

