#!/bin/bash

# Update the git-stats on the webserver at mptcp.info.ucl.ac.be/mptcp_stats/
file=`basename $0`
logfile=/tmp/${file}.log
exec > $logfile 2>&1
trap "cat $logfile | uuencode $logfile | mail -s \"$file failed\" christoph.paasch@gmail.com ; exit 1" ERR

cd $HOME/mtcp/
git pull

tag=`git describe --abbrev=0`
tag="805a6af8dba5dfdd35ec35dc52ec0122400b2610"

$HOME/bin/gitstats -c commit_begin=$tag -c project_name=MPTCP . ../mptcp_stats/

