#!/bin/bash -ex

# Create docker
./create_docker_kernel.sh "debian"

# Run docker
MY_ROOT_DIR=${1:-"$(grep ${SUDO_USER:-"${USERNAME}"} /etc/passwd | cut -d: -f6)"}

EXTRA_ARGS=("-v" "${MY_ROOT_DIR}:${MY_ROOT_DIR}:rw")

# to make sure they are both available in the docker
if [[ "${PWD}" != "${MY_ROOT_DIR}"* ]]; then
	EXTRA_ARGS+=("-v" "${PWD}:${PWD}:ro")
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

docker run -it --rm "${EXTRA_ARGS[@]}" "debian-kernel" bash -ex "${PWD}/create_kernel.sh"
