#!/usr/bin/python

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

current = "default"

def usage():
	print "./testing.py [--gig] [bug_xx [bug_xx [bug_xx...]]]"
	print "--gig means one-gig testbed on hen"
	print "--inl means one-gig testbed on inl"

try:
	optlist, bugs = getopt.getopt(sys.argv[1:], '', ['gig'])
except  getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

onehen = False 
oneinl = True

for o, a in optlist:
	if o == "--gig":
		onehen = True
	if o == "--inl":
		oneinl = True

if onehen:
	clientidx = "48"
	client_itf0 = "eth0"
	client_itf1 = "eth2"
	client_itf2 = "eth3"

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
	client = "computer"+clientidx
	router = "computer"+routeridx
	server = "computer"+serveridx
elif oneinl:
        clientidx = "48"
        client_itf0 = "eth0"
        client_itf1 = "eth2"
        client_itf2 = "eth3"

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

router_ip = "10.1.1.2"
server_ip = "10.2.1.1"

def do_ssh(host, cmd):
        return os.system("ssh -o ServerAliveInterval=10 root@"+host+" \""+cmd+"\"")

def do_ssh_back(host, cmd):
        return os.system("ssh -o ServerAliveInterval=10 root@"+host+" "+cmd)

def get_netstat(host, f):
	os.system("echo '====== netstat from "+host+" ======' >> "+f)
	do_ssh_back(host, "netstat -n >> "+f)
	do_ssh_back(host, "netstat -s >> "+f)

def crash_in_serial(look_for, host, bug):
        f = open(bug+"/"+host+"_serial")

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

	f.close()

        return stop

def ping_test(host):
        ret = os.system("ping -c 1 -W 3 "+host)
        return ret != 0

def start_bug(bug):
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

        get_netstat(client, bug+"/client_ns_before")
        get_netstat(router, bug+"/router_ns_before")
        get_netstat(server, bug+"/server_ns_before")

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
                os.system("kill -9 "+s.split(" ")[1])

        f.close()

	proc.kill()

def stop_bug(bug, look_for=["Call Trace:", "kmemleak"]):
        failed = False

        get_netstat(client, bug+"/client_ns_after")
        get_netstat(router, bug+"/router_ns_after")
        get_netstat(server, bug+"/server_ns_after")

	cli.flush()
	kill_serial(sub_cli)
	srv.flush()
	kill_serial(sub_srv)
	pro.flush()
	kill_serial(sub_pro)

        cli.close()
        srv.close()
        pro.close()

        if crash_in_serial(look_for, "client", bug):
                failed = True
                print "+++ CRASH IN CLIENT"

        if crash_in_serial(look_for, "router", bug):
                failed = True
                print "+++ CRASH IN PROXY"

        if crash_in_serial(look_for, "server", bug):
                failed = True
                print "+++ CRASH IN SERVER"

        if ping_test(client):
                failed = True
                print "+++ PING FAILED IN CLIENT"

        if ping_test(router):
                failed = True
                print "+++ PING FAILED IN PROXY"

        if ping_test(server):
                failed = True
                print "+++ PING FAILED IN SERVER"

        return failed


def set_rbuf_params(rmem, rate1, rate2, mdelay1, mdelay2, bdelay1, bdelay2):
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
                print "Burst 1 is "+str(burst)
                if burst < 2000:
                        burst = 2000
                print "Burst 1 is "+str(burst)
                do_ssh(router, "tc qdisc add dev "+router_itf11+" root tbf rate "+str(rate1)+"mbit burst "+str(burst)+"b latency "+str(mdelay1 - bdelay1)+"ms")
                do_ssh(router, "tc qdisc add dev "+router_itf12+" root tbf rate "+str(rate1)+"mbit burst "+str(burst)+"b latency "+str(mdelay1 - bdelay1)+"ms")
                bdel1 = int(math.ceil(float(bdelay1)/2))
                print "bdel1:"+str(bdel1)
                do_ssh(client, "tc qdisc add dev "+client_itf1+" root netem delay "+str(bdel1)+"ms")
                do_ssh(server, "tc qdisc add dev "+server_itf1+" root netem delay "+str(bdel1)+"ms")

        if rate2 < 1000:
                burst = int(math.ceil(float(rate2) * 1000 * 1000 / HZ / 8))
                print "Burst 2 is "+str(burst)
                if burst < 2000:
                        burst = 2000
                print "Burst 2 is "+str(burst)
                do_ssh(router, "tc qdisc add dev "+router_itf21+" root tbf rate "+str(rate2)+"mbit burst "+str(burst)+"b latency "+str(mdelay2 - bdelay2)+"ms")
                do_ssh(router, "tc qdisc add dev "+router_itf22+" root tbf rate "+str(rate2)+"mbit burst "+str(burst)+"b latency "+str(mdelay2 - bdelay2)+"ms")
                bdel2 = int(math.ceil(float(bdelay2)/2))
                print "bdel2:"+str(bdel2)
                do_ssh(client, "tc qdisc add dev "+client_itf2+" root netem delay "+str(bdel2)+"ms")
                do_ssh(server, "tc qdisc add dev "+server_itf2+" root netem delay "+str(bdel2)+"ms")

def verif_iperf(fname, mingb, times):
	failed = False
	speed = 0

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
	num = 2

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

	if verif_iperf(ifile, 1.7, num):
		failed = True

        return failed

def remove_addr():
        failed = False
        ifile = "remove_addr/iperf_res"
        num = 2

        do_ssh(server, "killall -9 iperf")
        do_ssh_back(server, "iperf -s &")
        do_ssh(client, "sysctl -w net.mptcp.mptcp_mss=8500")
        do_ssh(server, "sysctl -w net.mptcp.mptcp_mss=8500")

        start_bug("remove_addr")
        time.sleep(10)

        do_ssh_back(client, "iperf -c "+server_ip+" -t 30 -y c -P "+str(num)+" > "+ifile+" &")

        time.sleep(10)
	do_ssh(server, "ifconfig "+server_itf1+" down")

	time.sleep(40)
        do_ssh(client, "killall -9 iperf")
        do_ssh(server, "killall -9 iperf")
        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("remove_addr"):
                failed = True

        if verif_iperf(ifile, 0.9, num):
                failed = True

	do_ssh(server, "/etc/init.d/networking restart")

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

	if found > 50:
		print "+++ found more than 50 time-wait-sockets"
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

	if ret != 0:
		failed = True
		print "+++ apache-benchmark failed"	

        ret = do_ssh(client, "ab -c 250 -n 10000 "+server_ip+"/50KB")

        if ret != 0:
                failed = True
                print "+++ apache-benchmark failed"

        ret = do_ssh(client, "ab -c 500 -n 1000 "+server_ip+"/300KB")

        if ret != 0:
                failed = True
                print "+++ apache-benchmark failed"

        do_ssh(client, "sysctl -p")
        do_ssh(server, "sysctl -p")

        if stop_bug("simple_ab"):
                failed = True

        return failed

def basic_tests(climpc="1", srvmpc="1", cli1="on", cli2="on", pr11="on", pr12="on", pr21="on", pr22="on", srv1="on", srv2="on", conc="1", num="1", bug = "basic_tests", size="1KB"):
        failed = False

        do_ssh(client, "ip link set dev "+client_itf1+" multipath "+cli1)
        do_ssh(client, "ip link set dev "+client_itf2+" multipath "+cli2)
        do_ssh(server, "ip link set dev "+server_itf1+" multipath "+srv1)
        do_ssh(server, "ip link set dev "+server_itf2+" multipath "+srv2)

        start_bug(bug)
        time.sleep(5)

        ret = do_ssh(client, "ab -c "+conc+" -n "+num+" "+server_ip+"/"+size)

        if ret != 0:
                print "+++ apache-benchmark failed"
                failed = True

        do_ssh(client, "ip link set dev "+client_itf1+" multipath on")
        do_ssh(client, "ip link set dev "+client_itf2+" multipath on")
        do_ssh(server, "ip link set dev "+server_itf1+" multipath on")
        do_ssh(server, "ip link set dev "+server_itf2+" multipath on")

        if stop_bug(bug):
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


def do_test(bug):
	print "========================================="
        print bug.__name__+" is under test!"
        print "========================================="
	if bug():
		failed_bugs.append(bug.__name__)
		print "========================================="
		print bug.__name__+" FAILED!!!"
		print "========================================="
	

def test_all():
	if do_test(bug_cheng_sbuf):
		return True
	if do_test(simple_iperf):
		return True
	if do_test(remove_addr):
		return True
	if do_test(simple_ab):
		return True
	if do_test(time_wait_ab):
		return True

	return False

failed_bugs = []

# Global prepare setup
do_ssh(client, "iptables -F")
do_ssh(client, "iptables -A OUTPUT -s 10.1.1.1 -d 10.2.2.1 -j DROP")
do_ssh(client, "iptables -A OUTPUT -s 10.1.2.1 -d 10.2.1.1 -j DROP")

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


print "========================================="
print " SUMMARY"
print "========================================="
for i in failed_bugs:
	print i+" failed"

sys.exit(len(failed_bugs))
