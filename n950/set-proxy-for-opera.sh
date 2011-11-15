#!/bin/sh
# This script sets the Opera browser to use a proxy server.

set -e

devel-su user -c 'echo "" >> /home/user/.config/operamobile/opera.ini'
devel-su user -c 'echo "[Proxy]" >> /home/user/.config/operamobile/opera.ini'
devel-su user -c 'echo "HTTP server=mptcp.info.ucl.ac.be:3128" >> /home/user/.config/operamobile/opera.ini'
devel-su user -c 'echo "Use HTTP=1" >> /home/user/.config/operamobile/opera.ini'
