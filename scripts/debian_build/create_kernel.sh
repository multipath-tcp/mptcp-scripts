#!/bin/bash
# Note: mptcp repo needs to be in "${MY_ROOT_DIR}/mptcp" at the correct ref.
# If MY_ROOT_DIR is not set, it is "${HOME}"

# These variables can be modified
FULLNAME=${MY_FULLNAME:-"Christoph Paasch"}
EMAIL=${MY_EMAIL:-"christoph.paasch@gmail.com"}
ROOT_DIR=${MY_ROOT_DIR:-"${HOME}"}
CONFIG=${MY_CONFIG:-"n"}

# Unmodifiabled variables
INIT_DIR="${PWD}"
SCRIPT_DIR="${INIT_DIR}/$(dirname "${0}")"
DEB_INFO="${ROOT_DIR}/deb.info"

cd "${ROOT_DIR}"
rm -fv *.deb

cd "${ROOT_DIR}/mptcp"

if ! git describe --tags --exact-match; then
	echo "Not building a tag. Press Enter to continue."
	read
fi

DATE=$(date "+%Y%m%d%H%M%S")
KVERS=$(make kernelversion)
KVERS_MAJ=$(echo "${KVERS}" | cut -d. -f1-2)
CONFIG_KVERS="config-${KVERS_MAJ}"
CONFIG_PATH="${SCRIPT_DIR}/${CONFIG_KVERS}"
TAG="$(git describe --tags)"

[ "${CONFIG}" = "y" ] && cp -v "${CONFIG_PATH}" .config

echo "Building ${KVERS} - Tag: ${TAG}" | tee "${DEB_INFO}"
make -j $(nproc) deb-pkg DEBEMAIL="${EMAIL}" DEBFULLNAME="${FULLNAME}" LOCALVERSION=.mptcp KDEB_PKGVERSION="${DATE}"

[ "${CONFIG}" = "y" ] && cp -v .config "${CONFIG_PATH}"

cd "${ROOT_DIR}"

# Create meta-package
META_PKG="linux-mptcp"

# if it is not the last version, add a suffix to restrict to this kernel
if [ -s "${CONFIG_PATH}" ] && \
   [ "${CONFIG_KVERS}" != "$(basename "$(ls "${SCRIPT_DIR}/config-"* | sort -V | tail -n1)")" ]; then
	META_PKG+="-${KVERS_MAJ}"
fi

echo "Creating ${META_PKG} meta package"

rm -Rf "${META_PKG}"

mkdir -p "${META_PKG}/DEBIAN"
chmod -R a-s "${META_PKG}"
ctrl="${META_PKG}/DEBIAN/control"
touch "${ctrl}"

echo "Package: ${META_PKG}" >> "${ctrl}"
echo "Version: ${DATE}" >> "${ctrl}"
echo "Section: main" >> "${ctrl}"
echo "Priority: optional" >> "${ctrl}"
echo "Architecture: all" >> "${ctrl}"
echo "Depends: linux-headers-${KVERS}.mptcp, linux-image-${KVERS}.mptcp" >> "${ctrl}"
echo "Installed-Size:" >> "${ctrl}"
echo "Maintainer: ${FULLNAME} <${EMAIL}>" >> "${ctrl}"
echo "Description: A meta-package for Linux kernel v${KVERS} MPTCP ${TAG}" >> "${ctrl}"

dpkg --build "${META_PKG}"

mv "${META_PKG}.deb" "${META_PKG}_${TAG}_${DATE}_all.deb"

