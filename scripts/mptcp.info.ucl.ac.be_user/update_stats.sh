#!/bin/bash

# Update the git-stats on the webserver at mptcp.info.ucl.ac.be/mptcp_stats/
file=`basename $0`
logfile=/tmp/${file}.log
exec > $logfile 2>&1
trap "cat $logfile | uuencode $logfile | mailx -s \"$file failed\" christoph.paasch@gmail.com ; exit 1" ERR

cd $HOME/mtcp/
git pull

#tag=`git describe --abbrev=0`
#tag="6e4664525b1db28f8c4e1130957f70a94c19213e"
tag="d397274c53c6a418af62b08a92cbd1207616f3c5"

export PYTHONUNBUFFERED=x
$HOME/bin/gitstats -c commit_begin=$tag -c project_name=MPTCP . ../mptcp_stats/

