#!/usr/bin/python

import apt
import apt.package
import platform
import sys
import os
from shutil import *
import getopt

def pkg_check(pkg):
	packet = cache[pkg]
	if not packet.is_installed:
		print "ERROR: Package "+pkg+" is not installed - install it!!!"
		exit()

def usage():
	print "USAGE: ./setup.py [-f] directory"
	print "       -f / --full : Full install (filesystems, scripts, images)"
	print "       directory : The directory to install to"
	print "=============================== OR ============================="
	print "USAGE: ./setup.py [-u] directory"
	print "       -u / --update : Just update the images to the latest daily build"
	print "       directory : The directory to install to"

global cache

if len(sys.argv) != 3:
	usage()
	exit()

try:
	opts, args = getopt.getopt(sys.argv[1:2], "fu", ["full", "update"])
except getopt.GetoptError, err:
	# print help information and exit:
	print str(err) # will print something like "option -a not recognized"
	usage()
	sys.exit(2)

full = 0
update = 0
for o, a in opts:
	if o in ("-f", "--full"):
		full = 1
	elif o in ("-u", "--update"):
		update = 1
	else:
		assert False, "unhandled option"

directory = sys.argv[2]

if not os.path.exists(directory):
	print "ERROR: Your path: "+directory+" does not exist!!!"
	exit()

os.chdir(directory)

cache = apt.Cache()

# Sanity checks for installed packages
print "========================================================================"
print "Checking installed Debian-packages"

pkg_check("uml-utilities")
pkg_check("iptables")
pkg_check("bzip2")

print "Package-check succeeded"
print "========================================================================"
print "Downloading binaries and filesystems"

if platform.machine() == "x86_64":
	arch = "64"
elif platform.machine() == "i386" or platform.machine() == "i686":
	arch = "32"
else:
	print "ERROR: Did not recognize the platform: "+platform.machine()
	exit()

if full == 1 or update == 1:
	os.system("wget http://mptcp.info.ucl.ac.be/data/uml/vmlinux_"+arch+" -O vmlinux")
	os.system("chmod u+x vmlinux")

if full == 1:
	os.system("wget http://mptcp.info.ucl.ac.be/data/uml/client.sh")
	os.system("chmod u+x client.sh")
	os.system("wget http://mptcp.info.ucl.ac.be/data/uml/server.sh")
	os.system("chmod u+x server.sh")
	os.system("wget http://mptcp.info.ucl.ac.be/data/uml/fs_client_"+arch+".bz2"+" -O fs_client.bz2")
	os.system("wget http://mptcp.info.ucl.ac.be/data/uml/fs_server_"+arch+".bz2"+" -O fs_server.bz2")

	os.system("bunzip2 fs_client.bz2")
	os.system("bunzip2 fs_server.bz2")

	os.system("wget http://mptcp.info.ucl.ac.be/data/uml/README")

print "========================================================================"
print "FINISHED"
