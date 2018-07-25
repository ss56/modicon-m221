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

ladder_logic = ""
meta_data = ""
config_data = ""
try:
	#print "Getting Ladder logic from file " + sys.argv[1] + ":"
	#Get the packets into cap1
	cap1 = subprocess.check_output("tshark --disable-protocol opensafety -Y mbtcp -T fields -e modbus.data -r \"" + sys.argv[1] + "\"", shell=True)
	#Make cap1 as a list to get the number of packets in the file
	cap = cap1.split("\n")
	
except IndexError as e2:
	# File name is not given in the argument list
	sys.exit("You need to give a valid filename to get the ladder logic")
except Exception as e3:
	#Wrong file name is given in the argument list
	sys.exit("Not a valid file")

def readLadderLogic(cap1, i):
	global ladder_logic
	#Ladder logic is in the next responce packet
	llogic = cap1[i+2]
	logic_string = llogic
	#length = logic_string[18:23] 
	#Ladder Logic ends with 02	
	last_byte = logic_string[-2:]
	if last_byte == "02":
		ladder_logic = ladder_logic + cap1[i+2][24:]
		
	else:
		#If the packet doesn't have 02, 
		#that means the ladder logic continues in the next packet
		ladder_logic = ladder_logic + cap1[i+2][24:]		
		readLadderLogic(cap1, i+2)

def readMetaData(cap1, i):
	global meta_data
	raw_mdata = cap[i-2]
	mdata = str(raw_mdata)
	length = mdata[18:23]
	if length == "ec:00":
		meta_data = meta_data + cap[i-2][24:]
		readMetaData(cap1, i-2)
	else:
		pass
		#print "end"

#Tracing the PCAP file
for i in range (0, len(cap)):
    try:	
	data = cap[i]
	#Searching for the packet which contains M221, as the Ladder Logic starts in the next response packet  
	if "be:09:ff" in str(data):
		#Sending the packet to read the next response packet for ladder logic
		config_data = cap[i][24:]
		readLadderLogic(cap,i)
		readMetaData(cap,i)
		break
    except AttributeError as e:
        #ignore packets that aren't ENIP
        pass
    except IndexError as e2:
        #ignoring out of index packets
        pass



capture_name = sys.argv[1].split(".")
capture_name = capture_name[0].split("/")
llfilename = "HexCodes/Ladder/" + capture_name[len(capture_name) - 1] + "-ladderlogic"
f = open(llfilename, "w")
ladder_logic = ladder_logic.replace(":","")
f.write(ladder_logic.decode('hex'))

#print ladder_logic

mdfilename = "HexCodes/MetaData/" + capture_name[len(capture_name) - 1] + "-Metadata"
f = open(mdfilename, "w")
meta_data = meta_data.replace(":","")
f.write(meta_data.decode('hex'))


mdfilename = "HexCodes/Config/" + capture_name[len(capture_name) - 1] + "-Config"
f = open(mdfilename, "w")
meta_data = config_data.replace(":","")
f.write(meta_data.decode('hex'))