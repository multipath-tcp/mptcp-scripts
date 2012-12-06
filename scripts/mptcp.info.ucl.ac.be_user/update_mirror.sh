#!/bin/bash

# Update all git-sites maintained by the user
file=`basename $0`
logfile=/tmp/${file}.log
exec > $logfile 2>&1
trap "cat $logfile | uuencode $logfile | mail -s \"$file failed\" christoph.paasch@gmail.com ; exit 1" ERR

cd $HOME/mptcp_mirror
git remote update

cd $HOME/mptcp_tools
git pull

touch $HOME/no_crontab
