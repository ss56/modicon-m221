#sudo tshark --disable-protocol opensafety -Y "mbtcp" -T fields -e modbus.data -r "PCAP/na chavu.pcapng"
##############################
##Author:  Sushma Kalle     ##
##@Input:  PCAP file        ##
##@Output: Ladder Logic	    ##
##############################

import pyshark
import sys
import os,errno
import numpy as np
import subprocess
import re

ladder_logic = ""
meta_data = ""
config_data = ""
try:
	#print "Getting Ladder logic from file " + sys.argv[1] + ":"
	#Get the packets into cap1
	cap1 = subprocess.check_output("tshark --disable-protocol opensafety -Y mbtcp -T fields -e modbus.data -r \"" + sys.argv[1] + "\"", shell=True)
	#Make cap1 as a list to get the number of packets in the file
	cap =''
	cap1 = cap1.split("\n")
	for row in cap1:
		cap = cap+row[24:]
	
except IndexError as e2:
	# File name is not given in the argument list
	sys.exit("You need to give a valid filename to get the ladder logic")
except Exception as e3:
	#Wrong file name is given in the argument list
	sys.exit("Not a valid file")

offsets = [m.start() for m in re.finditer("50:4b",cap)]
cap = cap[offsets[0]:offsets[2]+60]

capture_name = sys.argv[1].split(".")
capture_name = capture_name[0].split("/")
llfilename = "HexCodes/PCAP-hex/" + capture_name[len(capture_name) - 1] + "-to-Text"
f = open(llfilename, "w")
cap1 = cap.replace(":","")
f.write(cap1.decode('hex'))
