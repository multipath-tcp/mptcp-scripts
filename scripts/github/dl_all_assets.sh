#! /bin/bash

RELEASES="https://api.github.com/repos/multipath-tcp/mptcp/releases"

for URL in $(curl -s "${RELEASES}" | grep browser_download_url | cut -d\" -f4); do
	D=$(echo "${URL}" | cut -d/ -f8)
	F=$(echo "${URL}" | cut -d/ -f9)
	mkdir -p "${D}"
	wget -L "${URL}" -O "${D}/${F}"
done
