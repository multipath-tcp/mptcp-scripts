#!/bin/bash

rm ~/rpmbuild/SOURCES/*
wget -P ~/rpmbuild/SOURCES/ https://github.com/multipath-tcp/iproute-mptcp/archive/mptcp_v0.94.zip

rpmbuild -ba ./iproute.spec

### install with 'dnf install iproute-mptcp_v0.93'

