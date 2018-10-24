#!/bin/bash
# Note: mptcp repo needs to be in "${MY_ROOT_DIR}/mptcp" at the correct ref.
# If MY_ROOT_DIR is not set, it is "${HOME}"

# These variables can be modified
ROOT_DIR=${MY_ROOT_DIR:-"${HOME}"}

cd "${ROOT_DIR}/mptcp"

make -j 8 rpm-pkg LOCALVERSION=.mptcp

# Install with 'dnf install kernel-4.1.34.mptcp' - may need to remove a kernel

