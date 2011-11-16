#!/bin/bash

# Update the git-stats on the webserver at mptcp.info.ucl.ac.be/mptcp_stats/

trap "mutt -s \"$0 crontab-failure\" -- christoph.paasch@uclouvain.be < /tmp/$0.log; exit 1" ERR

cd $HOME/mtcp/
git pull
gitstats -c commit_begin=v3.0 -c project_name=MPTCP . ../mptcp_stats/

