#!/bin/bash
# This script enables mptcp routing (multiple routing tables) on a Nokia N950

set -e

wget -N http://mptcp.info.ucl.ac.be/data/n950/mptcp_set_routing_tables_down
wget -N http://mptcp.info.ucl.ac.be/data/n950/mptcp_set_routing_tables_up

scp mptcp_set_routing_tables_down developer@192.168.2.15:
scp mptcp_set_routing_tables_up developer@192.168.2.15:

echo "Give the device root password (default: rootme):"
ssh developer@192.168.2.15 "devel-su root -c 'cp /home/developer/mptcp_set_routing_tables_down /etc/network/if-down.d/'"
echo "Give the device root password (default: rootme):"
ssh developer@192.168.2.15 "devel-su root -c 'cp /home/developer/mptcp_set_routing_tables_up /etc/network/if-up.d/'"


ssh developer@192.168.2.15 "rm /home/developer/mptcp_set_routing_tables_up"
ssh developer@192.168.2.15 "rm /home/developer/mptcp_set_routing_tables_down"

rm mptcp_set_routing_tables_down mptcp_set_routing_tables_up

