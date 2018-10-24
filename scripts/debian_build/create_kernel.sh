#!/bin/bash
# Note: mptcp repo needs to be in "${MY_ROOT_DIR}/mptcp" at the correct ref.
# If MY_ROOT_DIR is not set, it is "${HOME}"

# These variables can be modified
FULLNAME=${MY_FULLNAME:-"Christoph Paasch"}
EMAIL=${MY_EMAIL:-"christoph.paasch@gmail.com"}
ROOT_DIR=${MY_ROOT_DIR:-"${HOME}"}

cd "${ROOT_DIR}"
rm -f *.deb

cd "${ROOT_DIR}/mptcp"

DATE=`date "+%Y%m%d%H%M%S"`
KVERS=`make kernelversion`
make -j 8 deb-pkg DEBEMAIL="${EMAIL}" DEBFULLNAME="${FULLNAME}" LOCALVERSION=.mptcp KDEB_PKGVERSION="${DATE}"

cd "${ROOT_DIR}"

# Create meta-package
rm -Rf linux-mptcp

mkdir linux-mptcp
mkdir linux-mptcp/DEBIAN
chmod -R a-s linux-mptcp
ctrl="linux-mptcp/DEBIAN/control"
touch $ctrl

echo "Package: linux-mptcp" >> $ctrl
echo "Version: ${DATE}" >> $ctrl
echo "Section: main" >> $ctrl
echo "Priority: optional" >> $ctrl
echo "Architecture: all" >> $ctrl
echo "Depends: linux-headers-${KVERS}.mptcp, linux-image-${KVERS}.mptcp" >> $ctrl
echo "Installed-Size:" >> $ctrl
echo "Maintainer: ${FULLNAME} <${EMAIL}>" >> "${ctrl}"
echo "Description: A meta-package for linux-mptcp" >> $ctrl

dpkg --build linux-mptcp

mv linux-mptcp.deb linux-mptcp_${DATE}_all.deb

