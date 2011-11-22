#!/bin/bash
# This script enables mptcp routing (multiple routing tables) on a Nokia N950
# And it allows connecting to multiple interfaces

trap "echo 'ERROR occured - contact mptcp-dev@listes.uclouvain.be' ; exit 1" ERR

wget -N http://mptcp.info.ucl.ac.be/data/n950/mptcp_set_routing_tables_down
wget -N http://mptcp.info.ucl.ac.be/data/n950/mptcp_set_routing_tables_up

echo "When prompted for 'developer' password, type your password."

scp mptcp_set_routing_tables_down mptcp_set_routing_tables_up developer@192.168.2.15:

echo "Give the device root password (default: rootme):"
ssh developer@192.168.2.15 "devel-su root -c 'cp /home/developer/mptcp_set_routing_tables_down /etc/network/if-down.d/'"
echo "Give the device root password (default: rootme):"
ssh developer@192.168.2.15 "devel-su root -c 'cp /home/developer/mptcp_set_routing_tables_up /etc/network/if-up.d/'"


ssh developer@192.168.2.15 "rm /home/developer/mptcp_set_routing_tables_up /home/developer/mptcp_set_routing_tables_down"

rm mptcp_set_routing_tables_down mptcp_set_routing_tables_up

ssh developer@192.168.2.15 "gconftool -s /system/osso/connectivity/policy/modules -t list --list-type string [libicd_policy_merge.so,libicd_policy_ask.so,libicd_policy_any.so,libicd_policy_change.so,libicd_policy_add.so,libicd_policy_always_online.so,libicd_policy_restart.so,libicd_policy_nw_disconnect.so]"

