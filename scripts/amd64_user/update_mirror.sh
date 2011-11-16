#!/bin/bash

# Update all git-sites maintained by the user

trap "mutt -s \"$0 crontab-failure\" -- christoph.paasch@uclouvain.be < /tmp/$0.log; exit 1" ERR

cd $HOME/mptcp_tools
git pull
