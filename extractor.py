##############################
##Author:  Sushma Kalle     ##
##@Input:  PCAP file        ##
##@Output: Ladder Logic	    ##
##############################

import pyshark
import sys
import os,errno
import numpy as np

ladder_logic = ""
meta_data = ""
config_data = ""
try:
	#print "Getting Ladder logic from file " + sys.argv[1] + ":"
	#Get the packets into cap1
	cap1 = pyshark.FileCapture(sys.argv[1], display_filter='modbus', disable-protocol="opensafety")
	#Make cap1 as a list to get the number of packets in the file
	cap = list(cap1)
	
except IndexError as e2:
	# File name is not given in the argument list
	sys.exit("You need to give a valid filename to get the ladder logic")
except Exception as e3:
	#Wrong file name is given in the argument list
	sys.exit("Not a valid file")

def readLadderLogic(cap1, i):
	global ladder_logic
	#Ladder logic is in the next responce packet
	llogic = cap1[i+2].modbus.data
	logic_string = str(llogic)
	#length = logic_string[18:23] 
	#Ladder Logic ends with 02	
	last_byte = logic_string[-2:]
	if last_byte == "02":
		#print i
		ladder_logic = ladder_logic + cap1[i+2].modbus.data[24:]
		#print cap1[i+2].modbus.data[24:]
		#sys.exit("Done")
	else:
		#If the packet doesn't have 02, 
		#that means the ladder logic continues in the next packet
		#print "else"
		ladder_logic = ladder_logic + cap1[i+2].modbus.data[24:]		
		#print cap1[i+2].modbus.data[24:]
		readLadderLogic(cap1, i+2)

def readMetaData(cap1, i):
	global meta_data
	raw_mdata = cap1[i-2].modbus.data
	mdata = str(raw_mdata)
	length = mdata[18:23]
	if length == "ec:00":
		meta_data = meta_data + cap[i-2].modbus.data[24:]
		readMetaData(cap1, i-2)
	else:
		print "end"

#Tracing the PCAP file
for i in range (0, len(cap)):
    try:	
	data = cap1[i].modbus.data
	#Searching for the packet which contains M221, as the Ladder Logic starts in the next response packet  
	if "09:be:09:ff" in str(data):
		#Sending the packet to read the next response packet for ladder logic
		config_data = cap1[i].modbus.data[24:]
		readLadderLogic(cap1,i)
		readMetaData(cap1,i)
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
f = open(llfilename, "a")
ladder_logic = ladder_logic.replace(":","")
f.write(ladder_logic.decode('hex'))

#print ladder_logic

mdfilename = "HexCodes/MetaData/" + capture_name[len(capture_name) - 1] + "-Metadata"
f = open(mdfilename, "a")
meta_data = meta_data.replace(":","")
f.write(meta_data.decode('hex'))


mdfilename = "HexCodes/Config/" + capture_name[len(capture_name) - 1] + "-Config"
f = open(mdfilename, "a")
meta_data = config_data.replace(":","")
f.write(meta_data.decode('hex'))