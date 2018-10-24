#!/bin/bash
# Note: mptcp repo needs to be in "${MY_ROOT_DIR}/mptcp" at the correct ref.
# If MY_ROOT_DIR is not set, it is "${HOME}"

# These variables can be modified
ROOT_DIR=${MY_ROOT_DIR:-"${HOME}"}
CONFIG=${MY_CONFIG:-"n"}

# Unmodifiabled variables
INIT_DIR="${PWD}"
SCRIPT_DIR="${INIT_DIR}/$(dirname "${0}")"

cd "${ROOT_DIR}/mptcp"

KVERS=$(make kernelversion)
KVERS_MAJ=$(echo "${KVERS}" | cut -d. -f1-2)
CONFIG_KVERS="config-${KVERS_MAJ}"
CONFIG_PATH="${SCRIPT_DIR}/${CONFIG_KVERS}"

[ "${CONFIG}" = "y" ] && cp -v "${CONFIG_PATH}" .config

make -j 8 rpm-pkg LOCALVERSION=.mptcp

[ "${CONFIG}" = "y" ] && cp -v .config "${CONFIG_PATH}"

# Install with 'dnf install kernel-4.1.34.mptcp' - may need to remove a kernel

