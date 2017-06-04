#!/bin/bash

rm -Rf ~/rpmbuild/SOURCES/*
wget -P ~/rpmbuild/SOURCES/ https://github.com/multipath-tcp/net-tools/archive/mptcp_v0.92.zip
cp net-tools-config.h ~/rpmbuild/SOURCES/
cp net-tools-config.make ~/rpmbuild/SOURCES/

rpmbuild -ba ./net-tools.spec

### install with 'dnf install net-tools-mptcp_v0.92'

