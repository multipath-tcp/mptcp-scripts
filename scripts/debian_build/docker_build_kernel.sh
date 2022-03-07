#!/bin/bash -ex

DISTRIB="$(basename "$(dirname "${PWD}/docker_build_kernel.sh")" | cut -d_ -f1)"

# Create docker
./create_docker_kernel.sh "${DISTRIB}"

# Run docker
MY_ROOT_DIR=${MY_ROOT_DIR:-"$(grep ${SUDO_USER:-"${USERNAME}"} /etc/passwd | cut -d: -f6)"}

EXTRA_ARGS=("-v" "${MY_ROOT_DIR}:${MY_ROOT_DIR}:rw")

# to make sure they are both available in the docker
if [[ "${PWD}" != "${MY_ROOT_DIR}"* ]]; then
	EXTRA_ARGS+=("-v" "${PWD}:${PWD}:ro")
fi

# by default, RPM are produced in ${HOME}/rpmbuild but user is root in docker
if [ "${DISTRIB}" == "fedora" ]; then
	EXTRA_ARGS+=("-e" "RPMOPTS=--define '_topdir ${MY_ROOT_DIR}/rpm'")
	rm -rf "${MY_ROOT_DIR}/rpm"
fi

add_args() {
	if [ -n "${!1}" ]; then
		EXTRA_ARGS+=("-e" "${1}=${!1}")
	fi
}

add_args MY_FULLNAME
add_args MY_EMAIL
add_args MY_ROOT_DIR
add_args MY_CONFIG

docker run -it --rm "${EXTRA_ARGS[@]}" "${DISTRIB}-kernel" bash -ex "${PWD}/create_kernel.sh"
