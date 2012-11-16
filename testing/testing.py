#!/usr/bin/python

import math
import os
import time
import sys
import getopt
import inspect
import re
import subprocess
import shutil

global client
global server
global server_ip
global sub_cli
global sub_pro
global sub_srv
global cli
global pro
global srv
global HZ

HZ = 1000

current = "default"

def usage():
        print "./testing.py [--gig] [bug_xx [bug_xx [bug_xx...]]]"
        print "--gig means one-gig testbed on hen"
        print "--inl means one-gig testbed on inl"
        print "--twoinl means the second one-gig testbed on inl"

try:
        optlist, bugs = getopt.getopt(sys.argv[1:], '', ['gig', 'inl', 'twoinl', 'slow'])
except  getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

if len(bugs) < 1:
        usage()
        sys.exit(2)

onehen = False
oneinl = False
twoinl = False
slow = False

for o, a in optlist:
        if o == "--gig":
                onehen = True
        if o == "--inl":
                oneinl = True
        if o == "--twoinl":
                twoinl = True
        if o == "--slow":
                slow = True

if onehen:
        clientidx = "48"
        client_itf0 = "eth0"
        client_itf1 = "eth2"
        client_itf2 = "eth3"
        client_itf3 = "eth4"
        client_itf4 = "eth5"

        routeridx = "49"
        router_itf0 = "eth0"
        router_itf11 = "eth2"
        router_itf12 = "eth3"
        router_itf21 = "eth4"
        router_itf22 = "eth5"

        serveridx = "50"
        server_itf0 = "eth0"
        server_itf1 = "eth4"
        server_itf2 = "eth5"
        server_itf3 = "eth2"
        server_itf4 = "eth3"
        client = "computer"+clientidx
        router = "computer"+routeridx
        server = "computer"+serveridx
elif oneinl:
        clientidx = "4"
        client_itf0 = "eth0"
        client_itf1 = "eth6"
        client_itf2 = "eth7"
        client_itf3 = "eth4"
        client_itf4 = "eth5"

        routeridx = "5"
        router_itf0 = "eth0"
        router_10gitf1 = "eth2"
        router_10gitf2 = "eth3"
        router_itf11 = "eth4"
        router_itf12 = "eth5"
        router_itf21 = "eth6"
        router_itf22 = "eth7"

        serveridx = "6"
        server_itf0 = "eth0"
        server_10gitf1 = "eth2"
        server_10gitf2 = "eth3"
        server_itf1 = "eth6"
        server_itf2 = "eth7"
        server_itf3 = "eth4"
        server_itf4 = "eth5"

        client = "comp"+clientidx
        router = "comp"+routeridx
        server = "comp"+serveridx
elif twoinl:
        clientidx = "1"
        client_itf0 = "eth0"
        client_itf1 = "eth6"
        client_itf2 = "eth7"
        client_itf3 = "eth4"
        client_itf4 = "eth5"

        routeridx = "2"
        router_itf0 = "eth0"
        router_10gitf1 = "eth2"
        router_10gitf2 = "eth3"
        router_itf11 = "eth4"
        router_itf12 = "eth5"
        router_itf21 = "eth6"
        router_itf22 = "eth7"

        serveridx = "3"
        server_itf0 = "eth0"
        server_10gitf1 = "eth2"
        server_10gitf2 = "eth3"
        server_itf1 = "eth6"
        server_itf2 = "eth7"
        server_itf3 = "eth4"
        server_itf4 = "eth5"

        client = "comp"+clientidx
        router = "comp"+routeridx
        server = "comp"+serveridx

else:
        clientidx = "98"
        client_itf0 = "eth1"
        client_itf1 = "eth6"
        client_itf2 = "eth7"

        routeridx = "97"
        router_itf0 = "eth1"
        router_itf1 = "eth6"
        router_itf2 = "eth7"

        serveridx = "100"
        server_itf0 = "eth1"
        server_itf1 = "eth6"
        server_itf2 = "eth7"
        client = "computer"+clientidx
        router = "computer"+routeridx
        server = "computer"+serveridx

client_ip = "10.1.1.1"
client_ip2 = "10.1.2.1"
client_ip3 = "10.1.3.1"
client_ip4 = "10.1.4.1"
router_ip = "10.1.1.2"
router_ip2 = "10.1.2.2"
server_ip = "10.2.1.1"
server_ip_10g = "10.2.10.1"

def do_ssh(host, cmd):
        return os.system("ssh -o ServerAliveInterval=10 root@"+host+" \""+cmd+"\"")

def do_ssh_back(host, cmd):
        return os.system("ssh -o ServerAliveInterval=10 root@"+host+" "+cmd)

def get_netstat(host, f):
        do_ssh_back(host, "netstat -s > "+f+"/ns_"+host+"_before")

def get_netstat_final(host, f):
        do_ssh_back(host, "netstat -s > "+f+"/ns_"+host+"_after")
        os.system("beforeafter "+f+"/ns_"+host+"_before "+f+"/ns_"+host+"_after > "+f+"/"+host+"ns")

        do_ssh_back(host, "netstat -n > "+f+"/ns-n_"+host)

def crash_in_serial(look_for, must_be, host, bug):
        f = open(bug+"/"+host+"_serial")
        found_must = False

        stop = False
        for l in f:
                for s in look_for:
                        if l.find(s) == -1:
                                continue

                        stop = True
                        break
                if stop:
                        print l
                        break

                for s in must_be:
                        if l.find(s) != -1:
                                found_must = True
                                break

        if found_must == False and len(must_be) != 0:
                print "+++ did not find a necessary item"
                print must_be
                stop = True

        f.close()

        return stop

def ping_test(host):
        ret = os.system("ping -c 1 -W 3 "+host)
        return ret != 0

def start_bug(bug, cliport = 0, srvport = 0):
        global sub_cli
        global sub_pro
        global sub_srv
        global cli
        global pro
        global srv

        if os.path.exists(bug):
                shutil.rmtree(bug)
        time.sleep(1)
        os.system("mkdir "+bug)

	if cliport != 0:
		do_ssh_back(client, "tshark -s 150 -i any -n -w /tmp/client.dump tcp port "+str(cliport)+" &")
	if srvport != 0:
		do_ssh_back(server, "tshark -s 150 -i any -n -w /tmp/server.dump tcp port "+str(srvport)+" &")

        do_ssh(client, "echo '1' > /proc/sys/net/mptcp/mptcp_reset_snmp")
        do_ssh(router, "echo '1' > /proc/sys/net/mptcp/mptcp_reset_snmp")
        do_ssh(server, "echo '1' > /proc/sys/net/mptcp/mptcp_reset_snmp")

        get_netstat(client, bug)
        get_netstat(router, bug)
        get_netstat(server, bug)

        cli = open(bug+"/client_serial", 'w')
        sub_cli = subprocess.Popen(["s",clientidx],stdin=subprocess.PIPE, stdout=cli, stderr=cli)
        srv = open(bug+"/server_serial", 'w')
        sub_srv = subprocess.Popen(["s",serveridx],stdin=subprocess.PIPE, stdout=srv, stderr=srv)
        pro = open(bug+"/router_serial", 'w')
        sub_pro = subprocess.Popen(["s",routeridx],stdin=subprocess.PIPE, stdout=pro, stderr=pro)

        time.sleep(5)

        for i in range(0,5):
                sub_cli.stdin.write("\n")
                sub_srv.stdin.write("\n")
                sub_srv.stdin.write("\n")
                time.sleep(1)


def kill_serial(proc):
        pid = proc.pid

        os.system("ps u --ppid "+str(pid)+" | grep cpaasch | grep -v grep > /tmp/ps_cpaasch")

        f = open("/tmp/ps_cpaasch")
        for l in f:
                s = re.sub(' +', ' ', l)
                os.system("kill "+s.split(" ")[1])

        f.close()

        proc.kill()

def stop_bug(bug, look_for=["Call Trace:", "kmemleak", "too many of orphaned", "mptcp_fallback_infinite"], must_be_client=[], must_be_router=[], must_be_server=[], tcpdump = False):
        failed = False

        do_ssh(client, "ip route flush cache")
        do_ssh(router, "ip route flush cache")
        do_ssh(server, "ip route flush cache")

        get_netstat_final(client, bug)
        get_netstat_final(router, bug)
        get_netstat_final(server, bug)

        do_ssh_back(client, "cat /proc/net/snmp > "+bug+"/client_snmp")
        do_ssh_back(router, "cat /proc/net/snmp > "+bug+"/router_snmp")
        do_ssh_back(server, "cat /proc/net/snmp > "+bug+"/server_snmp")

        cli.flush()
        kill_serial(sub_cli)
        srv.flush()
        kill_serial(sub_srv)
        pro.flush()
        kill_serial(sub_pro)

        cli.close()
        srv.close()
        pro.close()


        if crash_in_serial(look_for, must_be_client, "client", bug):
                failed = True
                print "+++ CRASH IN CLIENT"

        if crash_in_serial(look_for, must_be_router, "router", bug):
                failed = True
                print "+++ CRASH IN PROXY"

        if crash_in_serial(look_for, must_be_server, "server", bug):
                failed = True
                print "+++ CRASH IN SERVER"

        if ping_test(client):
                failed = True
                print "+++ PING FAILED IN CLIENT"
	elif tcpdump:
                do_ssh(client, "killall tshark")
                time.sleep(5)
                os.system("scp root@"+client+":/tmp/client.dump "+bug+"/")


        if ping_test(router):
                failed = True
                print "+++ PING FAILED IN PROXY"

        if ping_test(server):
                failed = True
                print "+++ PING FAILED IN SERVER"
	elif tcpdump:
                do_ssh(server, "killall tshark")
                time.sleep(5)
                os.system("scp root@"+server+":/tmp/server.dump "+bug+"/")

        return failed

def host_limit_bw(host, itf, rate, burst, delay, limit):
        do_ssh(host, "tc qdisc add dev "+itf+" root handle 1: htb default 12")
        do_ssh(host, "tc class add dev "+itf+" parent 1:1 classid 1:12 htb rate "+str(rate)+"mbit burst "+str(burst))
        do_ssh(host, "tc qdisc add dev "+itf+" parent 1:12 netem delay "+str(delay)+"ms limit "+str(limit))


def set_rbuf_params(rmem, rate1, rate2, mdelay1, mdelay2, bdelay1, bdelay2, mss = 1400):
        rmem = int (rmem * 1024 * 1024)
        wmem = rmem

        if 87380 > rmem:
                do_ssh(client, "sysctl -w net.ipv4.tcp_rmem='4096 "+str(rmem)+" "+str(rmem)+"' ")
                do_ssh(client, "sysctl -w net.ipv4.tcp_wmem='4096 "+str(wmem)+" "+str(wmem)+"' ")
                do_ssh(server, "sysctl -w net.ipv4.tcp_rmem='4096 "+str(rmem)+" "+str(rmem)+"' ")
                do_ssh(server, "sysctl -w net.ipv4.tcp_wmem='4096 "+str(wmem)+" "+str(wmem)+"' ")
        else:
                do_ssh(client, "sysctl -w net.ipv4.tcp_rmem='4096 87380 "+str(rmem)+"' ")
                do_ssh(client, "sysctl -w net.ipv4.tcp_wmem='4096 87380 "+str(wmem)+"' ")
                do_ssh(server, "sysctl -w net.ipv4.tcp_rmem='4096 87380 "+str(rmem)+"' ")
                do_ssh(server, "sysctl -w net.ipv4.tcp_wmem='4096 87380 "+str(wmem)+"' ")

        do_ssh(router, "tc qdisc del dev "+router_itf11+" root")
        do_ssh(router, "tc qdisc del dev "+router_itf12+" root")
        do_ssh(router, "tc qdisc del dev "+router_itf21+" root")
        do_ssh(router, "tc qdisc del dev "+router_itf22+" root")
        do_ssh(client, "tc qdisc del dev "+client_itf1+" root")
        do_ssh(client, "tc qdisc del dev "+client_itf2+" root")
        do_ssh(server, "tc qdisc del dev "+server_itf1+" root")
        do_ssh(server, "tc qdisc del dev "+server_itf2+" root")
        time.sleep(5)

        if rate1 < 1000:
                burst = int(math.ceil(float(rate1) * 1000 * 1000 / HZ / 8))
                if burst < mss + 200:
                        burst = mss + 200

                # bdelay1 * 4, because we have one hop -> thus * 2 and it's the RTT -> * 2
                # Then * 2 to account for full buffers
                # Then / 1000.0 because the argument is in ms, but we need s
                # rate1 * 1024 * 1024 because it is in mbit but we need bit
                # Then / 8.0 because we need bytes
                # Then / (mss+100) because we need packets and not bytes . + 100 is roughly the MTU
                limit = (bdelay1 * 4 * 2 / 1000.0) * rate1 * 1024 * 1024 / 8.0 / (mss+100)

                host_limit_bw(router, router_itf11, rate1, burst, bdelay1, limit)
                host_limit_bw(router, router_itf21, rate1, burst, bdelay1, limit)
                host_limit_bw(server, server_itf1, rate1, burst, bdelay1, limit)
                host_limit_bw(client, client_itf1, rate1, burst, bdelay1, limit)
        if rate2 < 1000:
                burst = int(math.ceil(float(rate2) * 1000 * 1000 / HZ / 8))
                if burst < 2000:
                        burst = 2000
                # bdelay2 * 4, because we have one hop -> thus * 2 and it's the RTT -> * 2
                # Then * 2 to account for full buffers
                # Then / 1000.0 because the argument is in ms, but we need s
                # rate1 * 1024 * 1024 because it is in mbit but we need bit
                # Then / 8.0 because we need bytes
                # Then / (mss+100) because we need packets and not bytes . + 100 is roughly the MTU
                limit = (bdelay2 * 4 * 2 / 1000.0) * rate2 * 1024 * 1024 / 8.0 / (mss+100)

                host_limit_bw(router, router_itf12, rate2, burst, bdelay2, limit)
                host_limit_bw(router, router_itf22, rate2, burst, bdelay2, limit)
                host_limit_bw(server, server_itf2, rate2, burst, bdelay2, limit)
                host_limit_bw(client, client_itf2, rate2, burst, bdelay2, limit)


def verif_iperf(fname, mingb, times):
        failed = False
        speed = 0

        if slow:
                mingb = 0.01

        # If only one iperf has been launched, only one line should be in the results-file
        if times == 1:
                times = 0

        f = open(fname)
        i = 0
        for l in f:
                if i < times:
                        i += 1
                        continue
                l = l.rstrip("\n")
                l = l.rstrip("\r")
                s = l.split(",")

                speed = int(s[len(s)-1])

        wanted = int(mingb * 1024 * 1024 * 1024)
        if speed < wanted:
                print "+++ iperf was too slow: "+str(speed)+" wanted: "+str(wanted)
                failed = True

        if i != times:
                print "+++ iperf_res is empty"
                failed = True

        f.close()

        return failed

def bug_cheng_sbuf():
        # SETUP
        failed = False
        ifile = "bug_cheng_sbuf/iperf_res"

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s &")

        do_ssh(client, "sysctl -w net.ipv4.tcp_wmem='1000000 167772160 268435456'")
        do_ssh(server, "sysctl -w net.ipv4.tcp_rmem='1000000 167772160 268435456'")
        do_ssh(client, "sysctl -w net.mptcp.mptcp_ndiffports=16")

        start_bug("bug_cheng_sbuf")

        time.sleep(10)

        # DO EXP

        do_ssh_back(client, "iperf -c "+server_ip+" -y c > "+ifile+" &")

        time.sleep(20)

        do_ssh_back(client, "netstat -n | grep FIN_WAIT2 | grep 5001 > bug_cheng_sbuf/finwait2-socks")

        f = open("bug_cheng_sbuf/finwait2-socks")
        found = 0
        for l in f:
                if l.find("5001") == -1:
                        continue

                found += 1

        if found > 0:
                print "+++ found more than 0 fin-wait2-sockets"
                failed = True

        # FINISH
        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("bug_cheng_sbuf"):
                failed = True

        if verif_iperf(ifile, 0.5, 1):
                failed = True

        return failed

def simple_iperf():
        failed = False
        ifile = "simple_iperf/iperf_res"
        num = 4

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s -l 500K &")
        do_ssh(client, "sysctl -w net.mptcp.mptcp_mss=8500")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_mss=8500")

        start_bug("simple_iperf")
        time.sleep(10)

        do_ssh_back(client, "iperf -c "+server_ip+" -t 30 -l 500K -y c -P "+str(num)+" > "+ifile+" &")

        time.sleep(40)
        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("simple_iperf"):
                failed = True

        if verif_iperf(ifile, 1.6, num):
                failed = True

        return failed

def simple_iperf_limited():
        failed = False
        ifile = "simple_iperf_limited/iperf_res"
        num = 4

        set_rbuf_params(4, 8, 8, 100, 100, 10, 10)

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s &")

        start_bug("simple_iperf_limited")
        time.sleep(10)

        do_ssh_back(client, "iperf -c "+server_ip+" -t 30 -y c -P "+str(num)+" > "+ifile+" &")

        time.sleep(40)
        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("simple_iperf_limited"):
                failed = True

        if verif_iperf(ifile, 0.001, num):
                failed = True

        do_ssh(client, "/root/kill_tc.sh")
        do_ssh(router, "/root/kill_tc.sh")
        do_ssh(server, "/root/kill_tc.sh")

        return failed

def simple_iperf_lossy():
        failed = False
        ifile = "simple_iperf_lossy/iperf_res"
        num = 4

        do_ssh(router, "tc qdisc add dev "+router_itf11+" root netem loss 1%")
        do_ssh(router, "tc qdisc add dev "+router_itf12+" root netem loss 1%")
        do_ssh(router, "tc qdisc add dev "+router_itf21+" root netem loss 1%")
        do_ssh(router, "tc qdisc add dev "+router_itf22+" root netem loss 1%")

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s &")

        start_bug("simple_iperf_lossy")
        time.sleep(10)

        do_ssh_back(client, "iperf -c "+server_ip+" -t 30 -y c -P "+str(num)+" > "+ifile+" &")

        time.sleep(40)
        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("simple_iperf_lossy"):
                failed = True

        if verif_iperf(ifile, 0.001, num):
                failed = True

        do_ssh(client, "/root/kill_tc.sh")
        do_ssh(router, "/root/kill_tc.sh")
        do_ssh(server, "/root/kill_tc.sh")

        return failed

def remove_addr():
        failed = False
        ifile = "remove_addr/iperf_res"
        num = 4

        set_rbuf_params(16, 1000, 1000, 100, 100, 1, 1)

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s &")
        do_ssh(client, "sysctl -w net.mptcp.mptcp_mss=1400")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_mss=1400")
        #do_ssh(client, "sysctl -w net.mptcp.mptcp_debug=1")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_debug=1")

        start_bug("remove_addr")
        time.sleep(10)

        fd = open(ifile, 'w')
        subprocess.Popen("ssh root@"+client+" iperf -c "+server_ip+" -t 15 -y c -P "+str(num), stdout=fd, stderr=fd, shell=True)

        time.sleep(3)
        print "ifconfig "+server_itf1+" down"
        do_ssh(server, "ip addr del "+server_ip+"/24 dev "+server_itf1)

        time.sleep(20)
        fd.close()
        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("remove_addr"):
                failed = True

        if verif_iperf(ifile, 0.5, num):
                failed = True

        do_ssh(client, "/root/kill_tc.sh")
        do_ssh(router, "/root/kill_tc.sh")
        do_ssh(server, "/root/kill_tc.sh")

        do_ssh(server, "/etc/init.d/networking restart")
        do_ssh(server, "ip link set dev "+server_itf3+" multipath off")
        do_ssh(server, "ip link set dev "+server_itf4+" multipath off")

        return failed

def bbm():
        failed = False
        ifile = "bbm/iperf_res"
        num = 4

        set_rbuf_params(16, 1000, 1000, 100, 100, 1, 1)

#	do_ssh(client, "sysctl -w net.mptcp.mptcp_debug=1")

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s &")
        do_ssh(client, "sysctl -w net.mptcp.mptcp_mss=1400")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_mss=1400")
        do_ssh(server, "ifconfig "+server_itf2+" down")
	do_ssh(client, "ip route add 10.0.0.0/16 dev eth0")
	do_ssh(client, "ip route del default")

        start_bug("bbm")

        fd = open(ifile, 'w')
        subprocess.Popen("ssh root@"+client+" iperf -c "+server_ip+" -t 15 -y c -P "+str(num), stdout=fd, stderr=fd, shell=True)

        time.sleep(3)
        do_ssh(client, "ip addr del "+client_ip+"/24 dev "+client_itf1)
	do_ssh(client, "ip route del 10.2.1.0/24 via 10.1.1.2")
        time.sleep(0.5)
	do_ssh(client, "ip addr add "+client_ip+"/24 dev "+client_itf1)
        do_ssh(client, "ip route add 10.2.1.0/24 via 10.1.1.2")

        time.sleep(20)
        fd.close()
        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("bbm"):
                failed = True

        if verif_iperf(ifile, 0.5, num):
                failed = True

	do_ssh(client, "ip route del 10.0.0.0/16")
	do_ssh(client, "ip route add default via 10.0.0.1")
        do_ssh(client, "/root/kill_tc.sh")
        do_ssh(router, "/root/kill_tc.sh")
        do_ssh(server, "/root/kill_tc.sh")

	do_ssh(server, "/etc/init.d/networking restart")

        do_ssh(server, "ip link set dev "+server_itf3+" multipath off")
        do_ssh(server, "ip link set dev "+server_itf4+" multipath off")

        return failed

def add_addr():
        failed = False
        ifile = "add_addr/iperf_res"
        num = 4

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s &")
        do_ssh(client, "sysctl -w net.mptcp.mptcp_mss=1400")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_mss=1400")

        start_bug("add_addr")
        time.sleep(10)

        fd = open(ifile, 'w')
        subprocess.Popen("ssh root@"+client+" iperf -c "+server_ip+" -t 40 -y c -P "+str(num), stdout=fd, stderr=fd, shell=True)

        time.sleep(5)
        print "Remove ip from "+client_itf1
        do_ssh(client, "ip addr del dev "+client_itf1+" "+client_ip+"/24")
        time.sleep(5)
        print "Add ip from "+client_itf1
        do_ssh(client, "ip addr add dev "+client_itf1+" "+client_ip+"/24")
        do_ssh(client, "ip route add 10.2.1.0/24 via "+router_ip)
        time.sleep(5)
        print "Remove ip from "+client_itf2
        do_ssh(client, "ip addr del dev "+client_itf2+" "+client_ip2+"/24")

        time.sleep(40)
        fd.close()
        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        do_ssh(client, "/root/kill_tc.sh")
        do_ssh(router, "/root/kill_tc.sh")
        do_ssh(server, "/root/kill_tc.sh")

        if stop_bug("add_addr"):
                failed = True

        if verif_iperf(ifile, 0.5, num):
                failed = True

        do_ssh(client, "/etc/init.d/networking restart")

        return failed

def add_addr2():
        failed = False
        clifile = "add_addr2/cli_file"
        num = 1

        do_ssh(client, "sysctl -w net.mptcp.mptcp_debug=1")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_debug=1")
        do_ssh_back(server, "/root/simple_server/server &")

        start_bug("add_addr2")
        time.sleep(10)

        fd = open(clifile, 'w')
        subprocess.Popen("ssh root@"+client+" /root/simple_client/client ", stdout=fd, stderr=fd, shell=True)

        time.sleep(5)
        print "Remove ip from "+client_itf1
        do_ssh(client, "ip addr del dev "+client_itf1+" "+client_ip+"/24")
        time.sleep(5)
        print "Add ip from "+client_itf1
        do_ssh(client, "ip addr add dev "+client_itf1+" "+client_ip+"/24")
        do_ssh(client, "ip route add 10.2.1.0/24 via "+router_ip)
        time.sleep(5)
        print "Remove ip from "+client_itf2
        do_ssh(client, "ip addr del dev "+client_itf2+" "+client_ip2+"/24")

        time.sleep(20)
        fd.close()

        fd = open(clifile)
        for l in fd:
                if l.find("DONE") == -1:
                        print "+++ client did not finish!!!"
                        failed = True

                break

        fd.close()

        do_ssh(client, "killall client")
        do_ssh(server, "killall server")

        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("add_addr2"):
                failed = True

        do_ssh(client, "/etc/init.d/networking restart")

        return failed

def add_addr_3():
        failed = False
        ifile = "add_addr_3/iperf_res"
        num = 4

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s &")
        do_ssh(client, "ip link set dev "+client_itf3+" multipath on")
        do_ssh(client, "ip link set dev "+client_itf4+" multipath on")
        do_ssh(server, "ip link set dev "+server_itf3+" multipath on")
        do_ssh(server, "ip link set dev "+server_itf4+" multipath on")
        do_ssh(client, "ip addr del dev "+client_itf2+" "+client_ip2+"/24")
        do_ssh(client, "ip addr del dev "+client_itf3+" "+client_ip3+"/24")
        do_ssh(client, "ip addr del dev "+client_itf4+" "+client_ip4+"/24")

        start_bug("add_addr_3")
        time.sleep(10)

        fd = open(ifile, 'w')
        subprocess.Popen("ssh root@"+client+" iperf -c "+server_ip+" -t 40 -y c -P "+str(num), stdout=fd, stderr=fd, shell=True)

        time.sleep(5)
        print "Add ip from "+client_itf2
        do_ssh(client, "ip addr add dev "+client_itf2+" "+client_ip2+"/24")
        do_ssh(client, "ip route add 10.2.2.0/24 via "+router_ip2)
        time.sleep(1)
        print "Remove ip from "+client_itf1
        do_ssh(client, "ip addr del dev "+client_itf1+" "+client_ip+"/24")

        time.sleep(5)
        print "Add ip from "+client_itf3
        do_ssh(client, "ip addr add dev "+client_itf3+" "+client_ip3+"/24")
        do_ssh(client, "ip route add 10.2.3.0/24 dev "+client_itf3+" scope link")
        time.sleep(1)
        print "Remove ip from "+client_itf2
        do_ssh(client, "ip addr del dev "+client_itf2+" "+client_ip2+"/24")

        time.sleep(5)
        print "Add ip from "+client_itf4
        do_ssh(client, "ip addr add dev "+client_itf4+" "+client_ip4+"/24")
        do_ssh(client, "ip route add 10.2.4.0/24 dev "+client_itf4+" scope link")
        time.sleep(1)
        print "Remove ip from "+client_itf3
        do_ssh(client, "ip addr del dev "+client_itf3+" "+client_ip3+"/24")
        time.sleep(5)

        print "Add ip from "+client_itf1
        do_ssh(client, "ip addr add dev "+client_itf1+" "+client_ip+"/24")
        do_ssh(client, "ip route add 10.2.1.0/24 via "+router_ip)
        time.sleep(1)
        print "Remove ip from "+client_itf4
        do_ssh(client, "ip addr del dev "+client_itf4+" "+client_ip4+"/24")


        time.sleep(40)
        fd.close()
        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        do_ssh(client, "/root/kill_tc.sh")
        do_ssh(router, "/root/kill_tc.sh")
        do_ssh(server, "/root/kill_tc.sh")

        if stop_bug("add_addr_3"):
                failed = True

        if verif_iperf(ifile, 0.5, num):
                failed = True

        do_ssh(client, "/etc/init.d/networking restart")
        do_ssh(client, "ip link set dev "+client_itf3+" multipath off")
        do_ssh(client, "ip link set dev "+client_itf4+" multipath off")
        do_ssh(server, "ip link set dev "+server_itf3+" multipath off")
        do_ssh(server, "ip link set dev "+server_itf4+" multipath off")

        return failed

def add_addr_4():
        failed = False
        ifile = "add_addr_4/iperf_res"
        num = 1

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s &")
        do_ssh(client, "ip link set dev "+client_itf3+" multipath on")
        do_ssh(client, "ip link set dev "+client_itf4+" multipath on")
        do_ssh(client, "ip addr del dev "+client_itf2+" "+client_ip2+"/24")
        do_ssh(client, "ip addr del dev "+client_itf3+" "+client_ip3+"/24")
        do_ssh(client, "ip addr del dev "+client_itf4+" "+client_ip4+"/24")

        start_bug("add_addr_4")
        time.sleep(10)

        fd = open(ifile, 'w')
        subprocess.Popen("ssh root@"+client+" iperf -c "+server_ip+" -t 40 -y c -P "+str(num), stdout=fd, stderr=fd, shell=True)

        time.sleep(5)
        print "Add ip from "+client_itf2
        do_ssh(client, "ip addr add dev "+client_itf2+" "+client_ip2+"/24")
        do_ssh(client, "ip route add 10.2.2.0/24 via "+router_ip2)
        time.sleep(1)
        print "Remove ip from "+client_itf1
        do_ssh(client, "ip addr del dev "+client_itf1+" "+client_ip+"/24")

        time.sleep(5)
        print "Add ip from "+client_itf3
        do_ssh(client, "ip addr add dev "+client_itf3+" "+client_ip3+"/24")
        do_ssh(client, "ip route add 10.2.3.0/24 dev "+client_itf3+" scope link")
        time.sleep(1)
        print "Remove ip from "+client_itf2
        do_ssh(client, "ip addr del dev "+client_itf2+" "+client_ip2+"/24")

        time.sleep(5)
        print "Add ip from "+client_itf4
        do_ssh(client, "ip addr add dev "+client_itf4+" "+client_ip4+"/24")
        do_ssh(client, "ip route add 10.2.4.0/24 dev "+client_itf4+" scope link")
        time.sleep(1)
        print "Remove ip from "+client_itf3
        do_ssh(client, "ip addr del dev "+client_itf3+" "+client_ip3+"/24")
        time.sleep(5)

        print "Add ip from "+client_itf1
        do_ssh(client, "ip addr add dev "+client_itf1+" "+client_ip+"/24")
        do_ssh(client, "ip route add 10.2.1.0/24 via "+router_ip)
        time.sleep(1)
        print "Remove ip from "+client_itf4
        do_ssh(client, "ip addr del dev "+client_itf4+" "+client_ip4+"/24")


        time.sleep(40)
        fd.close()
        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        do_ssh(client, "/root/kill_tc.sh")
        do_ssh(router, "/root/kill_tc.sh")
        do_ssh(server, "/root/kill_tc.sh")

        if stop_bug("add_addr_4"):
                failed = True

        if verif_iperf(ifile, 0.4, num):
                failed = True

        do_ssh(client, "/etc/init.d/networking restart")
        do_ssh(client, "ip link set dev "+client_itf3+" multipath off")
        do_ssh(client, "ip link set dev "+client_itf4+" multipath off")

        return failed

def link_failure():
        failed = False
        ifile = "link_failure/iperf_res"
        num = 1

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s &")
        do_ssh(client, "sysctl -w net.mptcp.mptcp_mss=1400")
        do_ssh(client, "sysctl -w net.mptcp.mptcp_debug=1")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_mss=1400")

        #start_bug("link_failure", cliport=5001)
        start_bug("link_failure")
        time.sleep(10)

        fd = open(ifile, 'w')
        subprocess.Popen("ssh root@"+client+" iperf -c "+server_ip+" -t 30 -y c -P "+str(num), stdout=fd, stderr=fd, shell=True)

        time.sleep(5)
        do_ssh(router, "iptables -A FORWARD -s "+client_ip+" -j DROP")

        time.sleep(50)
        fd.close()
        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("link_failure", tcpdump=False):
                failed = True

        if verif_iperf(ifile, 0.5, num):
                failed = True

        do_ssh(router, "iptables -F FORWARD")

        return failed

def link_failure_2():
        failed = False
        scpfile = "link_failure_2/scp_progress"
        start_bug("link_failure_2")

        do_ssh(client, "rm 500MB")
        time.sleep(5)

        fd = open(scpfile, 'w')
        subprocess.Popen("ssh root@"+client+" scp root@"+server_ip+":/var/www/500MB . ", stdout=fd, stderr=fd, shell=True)

        time.sleep(3)
        do_ssh(router, "iptables -A FORWARD -s "+client_ip+" -j DROP")

        time.sleep(50)

        fd.close()

        if stop_bug("link_failure_2"):
                failed = True

        do_ssh_back(client, "ls -l -h 500MB > link_failure_2/ls-l")

        fd = open("link_failure_2/ls-l")
        for l in fd:
                if l.find("root 500M") == -1:
                        print "+++ 500MB file did not reach the client"
                        print l
                        if not slow:
                                failed = True

                break

        fd.close()

        do_ssh(router, "iptables -F FORWARD")
        do_ssh(router, "tc qdisc del dev "+router_itf12+" root")
        do_ssh(router, "tc qdisc del dev "+router_itf22+" root")

        return failed


def link_failure_3():
        failed = False
        clifile = "link_failure_3/clifile"
        do_ssh(client, "sysctl -w net.mptcp.mptcp_debug=1")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_debug=1")
        do_ssh(client, "sysctl -w net.ipv4.tcp_retries2=3")
        do_ssh(server, "sysctl -w net.ipv4.tcp_retries2=3")

        do_ssh(router, "tc qdisc add dev "+router_itf12+" root netem delay 100ms limit 1000")
        do_ssh(router, "tc qdisc add dev "+router_itf22+" root netem delay 100ms limit 1000")
        do_ssh_back(server, "/root/simple_server/server &")

        start_bug("link_failure_3", cliport=2002, srvport=2002)


        fd = open(clifile, 'w')
        subprocess.Popen("ssh root@"+client+" /root/simple_client/client ", stdout=fd, stderr=fd, shell=True)

        time.sleep(5)
        do_ssh(router, "iptables -A FORWARD -s "+client_ip+" -j DROP")

        time.sleep(40)

        fd.close()

        #if stop_bug("link_failure_3",must_be_client=["destroying meta-sk"], must_be_server=["destroying meta-sk"]):
        if stop_bug("link_failure_3", tcpdump=True):
                failed = True

        fd = open(clifile)
        for l in fd:
                if l.find("DONE") == -1:
                        print "+++ client did not finish!!!"
                        failed = True

                break

        fd.close()

        do_ssh(client, "killall client")
        do_ssh(server, "killall server")

        do_ssh(client, "sysctl -w net.mptcp.mptcp_debug=0")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_debug=0")
        do_ssh(client, "sysctl -w net.ipv4.tcp_retries2=15")
        do_ssh(server, "sysctl -w net.ipv4.tcp_retries2=15")

        do_ssh(router, "iptables -F FORWARD")
        do_ssh(router, "/root/kill_tc.sh")

        return failed

def pre_close():
        failed = False
        ifile = "pre_close/iperf_res"
        num = 1

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s &")
        do_ssh(client, "sysctl -w net.mptcp.mptcp_mss=8500")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_mss=8500")
        do_ssh(client, "sysctl -w net.mptcp.mptcp_debug=1")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_debug=1")

        start_bug("pre_close")
        time.sleep(10)

        fd = open(ifile, 'w')
        subprocess.Popen("ssh root@"+client+" iperf -c "+server_ip+" -t 20 -y c -P "+str(num), stdout=fd, stderr=fd, shell=True)

        time.sleep(10)

        fd.close()

        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")

        # Give the meta some time
        time.sleep(10)
        if stop_bug("pre_close", must_be_client=["destroying meta-sk"], must_be_server=["destroying meta-sk"]):
                failed = True

        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        return failed

def fast_close():
        failed = False
        num = 1

        do_ssh(client, "sysctl -w net.mptcp.mptcp_debug=1")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_debug=1")
        do_ssh_back(server, "/root/simple_server/server_fclose &")

        start_bug("fast_close")
        time.sleep(3)

        do_ssh(client, "/root/simple_client/client_fclose")

        # Give the meta some time
        time.sleep(10)
        if stop_bug("fast_close", must_be_client=["destroying meta-sk"], must_be_server=["destroying meta-sk"]):
                failed = True

        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        return failed

def so_linger():
        failed = False
        num = 1

        do_ssh(client, "sysctl -w net.mptcp.mptcp_debug=1")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_debug=1")
        do_ssh_back(server, "/root/simple_server/server_linger &")

        start_bug("so_linger")
        time.sleep(3)

        do_ssh(client, "/root/simple_client/client_linger")

        # Give the meta some time
        time.sleep(10)
        if stop_bug("so_linger", must_be_client=["destroying meta-sk"], must_be_server=["destroying meta-sk"]):
                failed = True

        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        return failed

def srr():
        failed = False
        num = 1

        do_ssh(client, "sysctl -w net.mptcp.mptcp_debug=1")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_debug=1")
        do_ssh(client, "sysctl -w net.ipv4.conf.all.accept_source_route=1")
        do_ssh(router, "sysctl -w net.ipv4.conf.all.accept_source_route=1")
        do_ssh(server, "sysctl -w net.ipv4.conf.all.accept_source_route=1")
        do_ssh_back(server, "/root/simple_server/server_srr &")

        start_bug("srr")
        time.sleep(3)

        do_ssh(client, "/root/simple_client/client_srr")

        # Give the meta some time
        time.sleep(10)
        if stop_bug("srr", must_be_client=["destroying meta-sk"], must_be_server=["destroying meta-sk"]):
                failed = True

        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        return failed

def time_wait_ab():
        failed = False

        start_bug("time_wait_ab")

        # We wait 60 seconds, to allow previous tw-sockets to timeout and get destroyed
        time.sleep(60)

        ret = do_ssh(client, "ab -c 100 -n 1000 "+server_ip+"/1KB")

        time.sleep(5)
        do_ssh_back(client, "netstat -n | grep TIME_WAIT > time_wait_ab/timewait-socks")

        f = open("time_wait_ab/timewait-socks")
        found = 0
        for l in f:
                if l.find("80") == -1:
                        continue

                found += 1

        if found > 100:
                print "+++ found more than 100 time-wait-sockets"
                failed = True
        f.close()

        if ret != 0:
                failed = True
                print "+++ apache-benchmark failed"

        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("time_wait_ab"):
                failed = True

        return failed


def simple_ab():
        failed = False

        start_bug("simple_ab")
        time.sleep(5)

        ret = do_ssh(client, "ab -c 100 -n 100000 "+server_ip+"/1KB")

        if ret != 0 and not slow:
                failed = True
                print "+++ apache-benchmark failed"

        ret = do_ssh(client, "ab -c 100 -n 100000 "+server_ip+"/50KB")

        if ret != 0 and not slow:
                failed = True
                print "+++ apache-benchmark failed"

        ret = do_ssh(client, "ab -c 100 -n 10000 "+server_ip+"/300KB")

        if ret != 0 and not slow:
                failed = True
                print "+++ apache-benchmark failed"

        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("simple_ab"):
                failed = True

        return failed

def ab_300():
        failed = False

        start_bug("ab_300")
        time.sleep(5)

        ret = do_ssh(client, "ab -c 100 -n 10000 "+server_ip+"/300KB")

        if ret != 0 and not slow:
                failed = True
                print "+++ apache-benchmark failed"

        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("ab_300"):
                failed = True

        return failed

def bug_google():
        # SETUP
        failed = False
        ifile = "bug_google/iperf_res"

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s &")

        do_ssh(client, "/root/setup_rfs")
        do_ssh(server, "/root/setup_rfs")

        #do_ssh(server, "sysctl -w net.mptcp.mptcp_debug=1")
        #do_ssh(client, "sysctl -w net.mptcp.mptcp_debug=1")

        do_ssh(client, "sysctl -w net.ipv4.tcp_wmem='4096    16384   4194304'")
        do_ssh(server, "sysctl -w net.ipv4.tcp_rmem='4096    16384   4194304'")
#       do_ssh(client, "ip link set dev "+client_itf3+" multipath on")
#       do_ssh(client, "ip link set dev "+client_itf4+" multipath on")
#       do_ssh(server, "ip link set dev "+server_itf3+" multipath on")
#       do_ssh(server, "ip link set dev "+server_itf4+" multipath on")

        start_bug("bug_google")

        time.sleep(10)

        # DO EXP

        do_ssh_back(client, "iperf -c "+server_ip+" -y c -t 30 > "+ifile+" &")

        time.sleep(40)

        # FINISH
        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("bug_google"):
                failed = True

        if verif_iperf(ifile, 1.2, 1):
                failed = True

        do_ssh(client, "ip link set dev "+client_itf3+" multipath off")
        do_ssh(client, "ip link set dev "+client_itf4+" multipath off")
        do_ssh(server, "ip link set dev "+server_itf3+" multipath off")
        do_ssh(server, "ip link set dev "+server_itf4+" multipath off")

        do_ssh(client, "/root/stop_rfs")
        do_ssh(server, "/root/stop_rfs")

        return failed

def bug_haproxy():
        failed = False
        do_ssh(router, "/usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg_2 -D")

        ret = basic_tests(cli1="off", cli2="off", pr11="off", pr12="off", pr21="off", pr22="off", srv1="off", srv2="off", conc="100", num="100000", bug="bug_haproxy", opts=" -X "+router_ip+":3129")

        if ret != 0:
                print "+++ ab on 1KB failed"
                failed = True

        time.sleep(5)

        ret = basic_tests(cli1="off", cli2="off", pr11="off", pr12="off", pr21="off", pr22="off", srv1="off", srv2="off", conc="100", num="10000", bug="bug_haproxy", opts=" -X "+router_ip+":3129", size="300KB")

        if ret != 0:
                print "+++ ab on 1KB failed"
                failed = True

        time.sleep(5)

        do_ssh(router, "killall -9 haproxy")
        time.sleep(5)
        return failed

def bug_haproxy_limited():
        failed = False
        do_ssh(router, "/usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg_2 -D")

        set_rbuf_params(4, 8, 8, 100, 100, 10, 10)

        ret = basic_tests(cli1="off", cli2="off", pr11="off", pr12="off", pr21="off", pr22="off", srv1="off", srv2="off", conc="10", num="10000", bug="bug_haproxy_limited", opts=" -X "+router_ip+":3129", cliport=3129, srvport=80)

        if ret != 0:
                print "+++ ab on 1KB failed"
                failed = True

        time.sleep(5)

        if not failed:
                ret = basic_tests(cli1="off", cli2="off", pr11="off", pr12="off", pr21="off", pr22="off", srv1="off", srv2="off", conc="10", num="100", bug="bug_haproxy_limited", opts=" -X "+router_ip+":3129", size="300KB", cliport=3129, srvport=80)

                if ret != 0:
                        print "+++ ab on 1KB failed"
                        failed = True

                time.sleep(5)

        do_ssh(router, "killall -9 haproxy")

        do_ssh(client, "/root/kill_tc.sh")
        do_ssh(router, "/root/kill_tc.sh")
        do_ssh(server, "/root/kill_tc.sh")

        return failed

def bug_ab_limited():
        failed = False

        set_rbuf_params(4, 8, 8, 100, 100, 10, 10)

        if not failed:
                ret = basic_tests(cli1="off", cli2="off", pr11="off", pr12="off", pr21="off", pr22="off", srv1="off", srv2="off", conc="100", num="1000", bug="bug_ab_limited", opts=" -v 1 ", cliport=80, srvport=80)

                if ret != 0:
                        print "+++ ab on 1KB failed"
                        failed = True

        if not failed:
                ret = basic_tests(cli1="off", cli2="off", pr11="off", pr12="off", pr21="off", pr22="off", srv1="off", srv2="off", conc="100", num="1000", bug="bug_ab_limited", size="50KB", opts=" -v 1 ")

                if ret != 0:
                        print "+++ ab on 50KB failed"
                        failed = True

        do_ssh(client, "/root/kill_tc.sh")
        do_ssh(router, "/root/kill_tc.sh")
        do_ssh(server, "/root/kill_tc.sh")

        return failed


def bug_ab_lossy():
        failed = False
        ret = 0

        do_ssh(router, "tc qdisc add dev "+router_itf11+" root netem loss 1%")
        do_ssh(router, "tc qdisc add dev "+router_itf12+" root netem loss 1%")
        do_ssh(router, "tc qdisc add dev "+router_itf21+" root netem loss 1%")
        do_ssh(router, "tc qdisc add dev "+router_itf22+" root netem loss 1%")

        if not failed:
                ret = basic_tests(cli1="off", cli2="off", pr11="off", pr12="off", pr21="off", pr22="off", srv1="off", srv2="off", conc="100", num="100000", bug="bug_ab_lossy", cliport=80, srvport=80)

                if ret != 0:
                        print "+++ ab on 1KB failed"
                        failed = True

        if not failed:
                ret = basic_tests(cli1="on", cli2="on", pr11="off", pr12="off", pr21="off", pr22="off", srv1="on", srv2="on", conc="100", num="10000", bug="bug_ab_lossy", size="50KB")

                if ret != 0:
                        print "+++ ab on 50KB failed"
                        failed = True

        do_ssh(client, "/root/kill_tc.sh")
        do_ssh(router, "/root/kill_tc.sh")
        do_ssh(server, "/root/kill_tc.sh")

        return failed



def bug_delay():
        failed = False
        ifile = "bug_delay/iperf_res"


        do_ssh(client, "sysctl -w net.ipv4.tcp_rmem='4096    87380  16777216'")
        do_ssh(client, "sysctl -w net.ipv4.tcp_wmem='4096    16384  16777216'")
        do_ssh(server, "sysctl -w net.ipv4.tcp_rmem='4096    87380  16777216'")
        do_ssh(server, "sysctl -w net.ipv4.tcp_wmem='4096    16384  16777216'")

        do_ssh(client, "ip link set dev "+client_itf2+" multipath off")
        do_ssh(server, "ip link set dev "+server_itf2+" multipath off")
        start_bug("bug_delay")

        do_ssh(router, "tc qdisc add dev "+router_itf11+" root netem delay 20ms limit 4000")
        do_ssh(router, "tc qdisc add dev "+router_itf21+" root netem delay 20ms limit 4000")

        do_ssh_back(server, "iperf -s &")

        time.sleep(5)

        ret = do_ssh_back(client, "iperf -c "+server_ip+" -y c -t 30 > "+ifile)

        # FINISH
        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if verif_iperf(ifile, 0.001, 1):
                failed = True

        do_ssh(client, "ip link set dev "+client_itf2+" multipath on")
        do_ssh(server, "ip link set dev "+server_itf2+" multipath on")

        do_ssh(router, "tc qdisc del dev "+router_itf11+" root")
        do_ssh(router, "tc qdisc del dev "+router_itf21+" root")

        do_ssh(router, "/root/kill_tc.sh")

        if stop_bug("bug_delay"):
                failed = True

        return failed

def basic_tests(climpc="1", srvmpc="1", cli1="on", cli2="on", pr11="on", pr12="on", pr21="on", pr22="on", srv1="on", srv2="on", conc="1", num="1", bug = "basic_tests", size="1KB", opts="", cliport=0, srvport=0):
        failed = False

        do_ssh(client, "sysctl -w net.mptcp.mptcp_enabled="+climpc)
        do_ssh(router, "sysctl -w net.mptcp.mptcp_enabled=1")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_enabled="+srvmpc)

        do_ssh(client, "ip link set dev "+client_itf1+" multipath "+cli1)
        do_ssh(client, "ip link set dev "+client_itf2+" multipath "+cli2)
        do_ssh(router, "ip link set dev "+router_itf11+" multipath "+pr11)
        do_ssh(router, "ip link set dev "+router_itf12+" multipath "+pr12)
        do_ssh(router, "ip link set dev "+router_itf21+" multipath "+pr21)
        do_ssh(router, "ip link set dev "+router_itf22+" multipath "+pr22)
        do_ssh(server, "ip link set dev "+server_itf1+" multipath "+srv1)
        do_ssh(server, "ip link set dev "+server_itf2+" multipath "+srv2)

        start_bug(bug, cliport=cliport, srvport=srvport)
        time.sleep(5)

        ret = do_ssh(client, "ab -c "+conc+" -n "+num+" "+opts+"  http://"+server_ip+"/"+size)

        if ret != 0:
                print "+++ apache-benchmark failed"
                failed = True

        do_ssh(client, "ip link set dev "+client_itf1+" multipath on")
        do_ssh(client, "ip link set dev "+client_itf2+" multipath on")
        do_ssh(router, "ip link set dev "+router_itf11+" multipath on")
        do_ssh(router, "ip link set dev "+router_itf12+" multipath on")
        do_ssh(router, "ip link set dev "+router_itf21+" multipath on")
        do_ssh(router, "ip link set dev "+router_itf22+" multipath on")
        do_ssh(server, "ip link set dev "+server_itf1+" multipath on")
        do_ssh(server, "ip link set dev "+server_itf2+" multipath on")

        if stop_bug(bug, tcpdump=True if cliport != 0 or srvport != 0 else False):
                failed = True
        return failed

def brute_force_ab():
        nums = ["1", "10", "100", "1000", "10000", "100000"]
        s = "1KB"
        for n in nums:
                cint = min(int(n), 100)
                c = str(cint)
                print "========================================="
                print 'DOING: basic_tests(cli2="off", srv1="off", srv2="off", conc='+c+', num='+n+', size='+s+')'
                print "========================================="
                ret = basic_tests(cli2="off", srv1="off", srv2="off", conc=c, num=n, bug="brute_force_ab_"+n+"_"+c, size=s)
                if ret:
                        print "========================================="
                        print "IT FAILED"
                        print "========================================="
                        return ret
                time.sleep(2)

def iperf_10g():
        failed = False
        ifile = "iperf_10g/iperf_res"
        num = 1

        if not oneinl:
                return False

        do_ssh(router, "/root/setup_rfs")
        do_ssh(server, "/root/setup_rfs")
        do_ssh(router, "sysctl -w net.ipv4.tcp_rmem='4096    87380  16777216'")
        do_ssh(router, "sysctl -w net.ipv4.tcp_wmem='4096    16384  16777216'")
        do_ssh(server, "sysctl -w net.ipv4.tcp_rmem='4096    87380  16777216'")
        do_ssh(server, "sysctl -w net.ipv4.tcp_wmem='4096    16384  16777216'")
#        do_ssh(router, "sysctl -w net.ipv4.tcp_rmem='4096    16777216  16777216'")
#        do_ssh(router, "sysctl -w net.ipv4.tcp_wmem='4096    16777216  16777216'")
#        do_ssh(server, "sysctl -w net.ipv4.tcp_rmem='4096    16777216  16777216'")
#        do_ssh(server, "sysctl -w net.ipv4.tcp_wmem='4096    16777216  16777216'")

        do_ssh(router, "ip link set dev "+router_itf11+" multipath off")
        do_ssh(router, "ip link set dev "+router_itf12+" multipath off")
        do_ssh(router, "ip link set dev "+router_itf21+" multipath off")
        do_ssh(router, "ip link set dev "+router_itf22+" multipath off")
        do_ssh(router, "ip link set dev "+router_10gitf1+" multipath on")
        do_ssh(router, "ip link set dev "+router_10gitf2+" multipath on")
        do_ssh(server, "ip link set dev "+server_10gitf1+" multipath on")
        do_ssh(server, "ip link set dev "+server_10gitf2+" multipath on")
        do_ssh(server, "ip link set dev "+server_itf1+" multipath off")
        do_ssh(server, "ip link set dev "+server_itf2+" multipath off")

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s -l 500K &")
        do_ssh(router, "sysctl -w net.mptcp.mptcp_mss=8500")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_mss=8500")
        do_ssh(router, "sysctl -w net.mptcp.mptcp_checksum=0")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_checksum=0")

        start_bug("iperf_10g")
        time.sleep(10)

        do_ssh_back(router, "iperf -c "+server_ip_10g+" -t 30 -l 500K -y c -P "+str(num)+" > "+ifile+" &")

        time.sleep(40)
        do_ssh(router, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(router, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("iperf_10g"):
                failed = True

        if verif_iperf(ifile, 13, num):
                failed = True

        do_ssh(router, "ip link set dev "+router_itf11+" multipath on")
        do_ssh(router, "ip link set dev "+router_itf12+" multipath on")
        do_ssh(router, "ip link set dev "+router_itf21+" multipath on")
        do_ssh(router, "ip link set dev "+router_itf22+" multipath on")
        do_ssh(router, "ip link set dev "+router_10gitf1+" multipath off")
        do_ssh(router, "ip link set dev "+router_10gitf2+" multipath off")
        do_ssh(server, "ip link set dev "+server_10gitf1+" multipath off")
        do_ssh(server, "ip link set dev "+server_10gitf2+" multipath off")
        do_ssh(server, "ip link set dev "+server_itf1+" multipath on")
        do_ssh(server, "ip link set dev "+server_itf2+" multipath on")
        do_ssh(router, "/root/stop_rfs")
        do_ssh(server, "/root/stop_rfs")

        return failed

def do_test(bug):
        print "========================================="
        print bug.__name__+" is under test!"
        print "========================================="
        if bug():
                failed_bugs.append(bug.__name__)
                print "========================================="
                print bug.__name__+" FAILED!!!"
                print "========================================="
                return True

        return False


def test_all():
        if do_test(bug_cheng_sbuf):
                return True
        if do_test(bug_google):
                return True
        if do_test(bug_haproxy):
                return True
        if do_test(simple_iperf):
                return True
        if do_test(remove_addr):
                return True
        if do_test(bbm):
                return True
        if do_test(add_addr):
                return True
        if do_test(add_addr2):
                return True
        if do_test(add_addr_3):
                return True
        if do_test(add_addr_4):
                return True
        if do_test(link_failure):
                return True
        if do_test(link_failure_2):
                return True
        if do_test(link_failure_3):
                return True
        if do_test(simple_ab):
                return True
        if do_test(time_wait_ab):
                return True
        if do_test(ab_300):
                return True
        if do_test(pre_close):
                return True
        if do_test(fast_close):
                return True
        if do_test(so_linger):
                return True
        if do_test(srr):
                return True
        if do_test(iperf_10g):
                return True
        if do_test(bug_haproxy_limited):
                return True
        if do_test(simple_iperf_limited):
                return True
        if do_test(bug_ab_lossy):
                return True
        if do_test(simple_iperf_lossy):
                return True
        if do_test(bug_delay):
                return True

        return False

failed_bugs = []

do_ssh(router, "sysctl -w net.ipv4.ip_forward=1")

# Global prepare setup
do_ssh(client, "iptables -F")
do_ssh(client, "iptables -A OUTPUT -s 10.1.1.1 -d 10.1.2.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.1.1 -d 10.2.2.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.1.1 -d 10.2.3.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.1.1 -d 10.2.4.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.1.1 -d 10.2.10.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.1.1 -d 10.2.11.0/24 -j DROP")

do_ssh(client, "iptables -A OUTPUT -s 10.1.2.1 -d 10.1.1.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.2.1 -d 10.2.1.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.2.1 -d 10.2.3.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.2.1 -d 10.2.4.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.2.1 -d 10.2.10.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.2.1 -d 10.2.11.0/24 -j DROP")

do_ssh(client, "iptables -A OUTPUT -s 10.1.3.1 -d 10.2.1.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.3.1 -d 10.2.2.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.3.1 -d 10.2.4.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.3.1 -d 10.2.10.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.3.1 -d 10.2.11.0/24 -j DROP")

do_ssh(client, "iptables -A OUTPUT -s 10.1.4.1 -d 10.2.1.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.4.1 -d 10.2.2.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.4.1 -d 10.2.3.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.4.1 -d 10.2.10.0/24 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.4.1 -d 10.2.11.0/24 -j DROP")

do_ssh(router, "iptables -A OUTPUT -s 10.2.10.0/24 -d 10.2.11.0/24 -j DROP")
do_ssh(router, "iptables -A OUTPUT -s 10.2.11.0/24 -d 10.2.10.0/24 -j DROP")

do_ssh(client, "ip link set dev "+client_itf1+" multipath on")
do_ssh(client, "ip link set dev "+client_itf2+" multipath on")
do_ssh(client, "ip link set dev "+client_itf3+" multipath off")
do_ssh(client, "ip link set dev "+client_itf4+" multipath off")

do_ssh(router, "ip link set dev "+router_10gitf1+" multipath off")
do_ssh(router, "ip link set dev "+router_10gitf2+" multipath off")
do_ssh(server, "ip link set dev "+server_itf1+" multipath on")
do_ssh(server, "ip link set dev "+server_itf2+" multipath on")
do_ssh(server, "ip link set dev "+server_itf3+" multipath off")
do_ssh(server, "ip link set dev "+server_itf4+" multipath off")

do_ssh(server, "ip link set dev "+server_10gitf1+" multipath off")
do_ssh(server, "ip link set dev "+server_10gitf2+" multipath off")


# Run specified experiments
for i in range(0,len(bugs)):
        print "========================================="
        print bugs[i]+" is under test!"
        print "========================================="
        current = bugs[i]
        if vars()[bugs[i]]():
                print "========================================="
                print bugs[i]+" failed!!!"
                print "========================================="
                break


print "========================================="
print " SUMMARY"
print "========================================="
for i in failed_bugs:
        print i+" failed"

print bugs

sys.exit(len(failed_bugs))

