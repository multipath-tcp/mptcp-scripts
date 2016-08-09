#!/bin/bash

# Update the git-stats on the webserver at mptcp.info.ucl.ac.be/mptcp_stats/
file=`basename $0`
logfile=/tmp/${file}.log
exec > $logfile 2>&1
trap "cat $logfile | uuencode $logfile | mailx -s \"$file failed\" christoph.paasch@gmail.com ; exit 1" ERR

cd $HOME/mtcp/
git checkout mptcp_trunk
git pull

#tag=`git describe --abbrev=0`
tag="b953c0d234bc72e8489d3bf51a276c5c4ec85345"

export PYTHONUNBUFFERED=x
$HOME/bin/gitstats -c commit_begin=$tag -c project_name=MPTCP -c max_authors=30 -c start_date="3/4/2009" . ../mptcp_stats/

