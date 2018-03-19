###################################
##Author:  Sushma Kalle    	 ##
##@Input:  Ladder Logic	   	 ##
##@Output: Instruction List   	 ##
###################################

import pyshark
import sys
import os,errno
import numpy as np
import extractor
import re
import MySQLdb

#global j
def findCode(opcode):
	result = ''
	#print opcode
	cur.execute("select instruction from instructions where op_code= '"+opcode+"'")
	rows = cur.fetchall()
	for row in rows:
		print row[0]
		#j = j+1
	

def form_code(code_list):
	temp = ""
	j=0
	print "LD"
	for i in range(0, len(code_list)):
		
		if code_list[i] == "fc" or code_list[i] == "fd":
			print "ST"
		elif code_list[i] == "23":
			print "AND"
		elif code_list[i] == "22":
			print "OR"
		else:
			temp = code_list[i] + code_list[i+1]
			findCode(temp)
			temp = ""
			'''boolean, instruction = findCode(temp)
			if boolean == 1:
				print instruction'''
ll = extractor.ladder_logic

db = MySQLdb.connect(host="localhost",  # host 
                     user="root",       # username
                     passwd="12345",    # password
                     db="modicon")   	# name of the database

cur = db.cursor() 

code_list = []

try:
	for i in range(0, len(ll),2):
		code_list.append(ll[i] + ll[i+1])
except IndexError as e2:
        #ignoring out of index packets
        print i

print code_list

form_code(code_list)

