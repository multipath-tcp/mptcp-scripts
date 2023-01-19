#! /bin/bash

STD="tools/testing/selftests/net/mptcp"
STC="${STD}/config"

mkdir -p "${STD}"
cat <<EOF > "${STC}"
CONFIG_MPTCP=y
CONFIG_MPTCP_PM_ADVANCED=y
CONFIG_MPTCP_FULLMESH=y
CONFIG_MPTCP_NDIFFPORTS=y
CONFIG_MPTCP_BINDER=y
CONFIG_MPTCP_NETLINK=y
# CONFIG_DEFAULT_FULLMESH is not set
# CONFIG_DEFAULT_NDIFFPORTS is not set
# CONFIG_DEFAULT_BINDER is not set
# CONFIG_DEFAULT_NETLINK is not set
CONFIG_DEFAULT_DUMMY=y
CONFIG_DEFAULT_MPTCP_PM="default"
CONFIG_MPTCP_SCHED_ADVANCED=y
CONFIG_MPTCP_BLEST=y
CONFIG_MPTCP_ROUNDROBIN=y
CONFIG_MPTCP_REDUNDANT=y
CONFIG_MPTCP_ECF=y
CONFIG_DEFAULT_SCHEDULER=y
# CONFIG_DEFAULT_ROUNDROBIN is not set
# CONFIG_DEFAULT_REDUNDANT is not set
# CONFIG_DEFAULT_BLEST is not set
# CONFIG_DEFAULT_ECF is not set
CONFIG_DEFAULT_MPTCP_SCHED="default"
CONFIG_IPV6=y
CONFIG_INET_DIAG=y
CONFIG_VETH=y
EOF

exit_trap() {
	rm -r "${STD}"
}

trap exit_trap EXIT

cat <<'EOF' > ".virtme-prepare-post"
#! /bin/bash

# For sudo, not to say: sudo: unable to resolve host (none): Name or service not known
echo "127.0.1.1 (none)" >> /etc/hosts

cd /opt/iproute2
git fetch https://github.com/multipath-tcp/iproute-mptcp mptcp_v0.96
git switch -c mptcp_v0.96 FETCH_HEAD
./configure
make -j"$(nproc)" -l"$(nproc)" clean all install

cd /opt/packetdrill/gtests/net/packetdrill
#git fetch https://github.com/multipath-tcp/packetdrill_mptcp master
git fetch https://github.com/matttbe/packetdrill_mptcp mptcp_v0.96
git switch -c mptcp FETCH_HEAD
./configure
make -j"$(nproc)" -l"$(nproc)"

cd "${KERNEL_SRC}"
EOF

if [ -x ./.virtme_run.sh ]; then
	INPUT_BUILD_SKIP_PERF=1 \
		INPUT_BUILD_SKIP_SELFTESTS=1 \
		INPUT_BUILD_SKIP_PACKETDRILL=1 \
			./.virtme_run.sh "${@}"
else
	docker run \
		-v "${PWD}:${PWD}:rw" \
		-w "${PWD}" \
		-e INPUT_BUILD_SKIP_PERF=1 \
		-e INPUT_BUILD_SKIP_SELFTESTS=1 \
		-e INPUT_BUILD_SKIP_PACKETDRILL=1 \
		--privileged \
		--rm \
		-it \
		--pull always \
		mptcp/mptcp-upstream-virtme-docker:latest \
		"${@}"
fi
