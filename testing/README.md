Virtme
======

Setup
-----

It is simple:

```
cd <kernel src>
ln -s <path/to/scripts>/testing/virtme.sh .virtme.sh
./.virtme.sh <see manual, e.g. "normal">
```

Tips:
- Type `poweroff` to turn the VM off
- Use `docker ps` and `docker exec -it <id> bash` to modify other files than the
  current work dir
- Use the dev mode (see below) with `VIRTME_PACKETDRILL_PATH="${PWD}/../packetdrill"`
  env var to mount an external packetdrill dir.

Development
-----------

If you need to modify `mptcp-upstream-virtme-docker`, you can do a few extra
steps.

First, you need to clone mptcp-upstream-virtme-docker somewhere:

```
git clone https://github.com/multipath-tcp/mptcp-upstream-virtme-docker.git
```

Then:

```
cd <kernel src>
ln -s <path/to/mptcp-upstream-virtme-docker>/run-tests-dev.sh .virtme_run.sh
```
