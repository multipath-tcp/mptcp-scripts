#!/bin/bash

# Update all git-sites maintained by the user
file=`basename $0`
host=`cat /etc/hostname`
trap "mutt -s \"$host $file crontab-failure\" -- christoph.paasch@uclouvain.be < /tmp/${file}.log; exit 1" ERR                                                                                                                         

cd $HOME/mptcp_tools
git pull

cd $HOME/mptcp
git pull

