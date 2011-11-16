#!/bin/bash

set -e

cd $HOME/uml/mptcp
git checkout mptcp_trunk
git pull

make -j 2 O=../build_uml/ ARCH=um

cd ..

scp fs_client_64.bz2 fs_server_64.bz2 cpaasch@mptcp.info.ucl.ac.be:uml/
scp build_uml/vmlinux cpaasch@mptcp.info.ucl.ac.be:uml/vmlinux_64

