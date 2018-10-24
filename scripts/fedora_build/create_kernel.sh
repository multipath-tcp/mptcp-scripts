#!/bin/bash

cd $HOME

cd $HOME/mptcp

make -j 8 rpm-pkg LOCALVERSION=.mptcp

# Install with 'dnf install kernel-4.1.34.mptcp' - may need to remove a kernel

