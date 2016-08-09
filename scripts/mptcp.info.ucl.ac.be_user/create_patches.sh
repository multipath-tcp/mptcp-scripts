#!/bin/bash

# Create and maintain the snapshots
file=`basename $0`
logfile=/tmp/${file}.log
exec > $logfile 2>&1
trap "cat $logfile | uuencode $logfile | mailx -s \"$file failed\" christoph.paasch@gmail.com ; exit 1" ERR

function gen_patch {
	VERSION=`git log --oneline --first-parent | grep -m 1 "Merge tag" | cut -d "'" -f2 | cut -d "'" -f1`

	rm /home/ftp/mptcp-patches/mptcp-${VERSION}-*.patch
	git diff $VERSION > /home/ftp/mptcp-patches/mptcp-${VERSION}-`git rev-parse --short HEAD`.patch
}

function repo {
	git checkout $1
	git pull
	gen_patch
}

cd $HOME/mtcp/

git fetch stable

repo 'mptcp_trunk'
repo 'mptcp_v0.90'
repo 'mptcp_v0.91'

git checkout mptcp_trunk
