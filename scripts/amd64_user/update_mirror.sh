#!/bin/bash

# Update all git-sites maintained by the user
file=`basename $0`                                                                                                                                                                                                               
trap "mutt -s \"$file crontab-failure\" -- christoph.paasch@uclouvain.be < /tmp/${file}.log; exit 1" ERR                                                                                                                         

cd $HOME/mptcp_tools
git pull

cd $HOME/mptcp
git pull

