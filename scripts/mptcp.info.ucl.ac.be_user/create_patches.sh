#!/bin/bash

# Create and maintain the snapshots
file=`basename $0`
logfile=/tmp/${file}.log
exec > $logfile 2>&1
trap "cat $logfile | uuencode $logfile | mailx -s \"$file failed\" christoph.paasch@gmail.com ; exit 1" ERR

function gen_patch {
	VERSION=`git log --oneline --merges origin/$1 | grep -m 1 "Merge tag" | cut -d "'" -f2 | cut -d "'" -f1`

	rm /home/ftp/mptcp-patches/mptcp-${VERSION}-*.patch
	git diff ${VERSION}..origin/$1 > /home/ftp/mptcp-patches/mptcp-${VERSION}-`git rev-parse --short origin/${1}`.patch
}

cd $HOME/mtcp/

git fetch --tags --all

gen_patch 'mptcp_trunk'
for i in $(seq 91 96); do
	gen_patch "mptcp_v0.${i}"
done

git checkout mptcp_trunk
git pull
