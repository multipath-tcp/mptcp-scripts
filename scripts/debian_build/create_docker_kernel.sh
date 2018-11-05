#! /bin/bash -ex

DISTRIB="${1?}"

docker build -t "${DISTRIB}-kernel" -f "Dockerfile_kernel_${DISTRIB}.txt" .
