#!/usr/bin/python

import sys
import os
from shutil import *

def usage():
	print "USAGE: ./setup_n950.py directory"

if len(sys.argv) != 2:
	usage()
	exit()

directory = sys.argv[1]

if not os.path.exists(directory):
	print "ERROR: Your path: "+directory+" does not exist!!!"
	exit()

os.chdir(directory)

print "========================================================================"
print "Downloading everything"

os.system("wget -N http://192.135.168.249/data/n950/modules.tar")
os.system("wget -N http://192.135.168.249/data/n950/zImage")

os.system("wget -N http://192.135.168.249/data/n950/clean_modules.tar")
os.system("wget -N http://192.135.168.249/data/n950/clean_zImage")

os.system("wget -N http://192.135.168.249/data/n950/flash_n950.sh")
os.system("chmod u+x flash_n950.sh")
os.system("wget -N http://192.135.168.249/data/n950/flash_n950_clean.sh")
os.system("chmod u+x flash_n950_clean.sh")
os.system("wget -N http://192.135.168.249/data/n950/n950_insmod.sh")
os.system("chmod u+x n950_insmod.sh")

os.system("wget -N http://192.135.168.249/data/n950/setup_mptcp_routing.sh")
os.system("chmod u+x setup_mptcp_routing.sh")
os.system("wget -N http://192.135.168.249/data/n950/install_opera_browser.sh")
os.system("chmod u+x install_opera_browser.sh")
