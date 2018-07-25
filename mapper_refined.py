##################################
##Author:  Sushma Kalle    	 	##
##@Input:  Ladder Logic	   	 	##
##@Output: Instruction List   	##
##################################

import pyshark
import sys
import os,errno
import numpy as np
import extractor_refined
import re
import MySQLdb
import memwords
from operator import itemgetter


thisline = ''
# Replace function for repeated occurances
def rreplace(s, old, new, occurrence):
	li = s.rsplit(old, occurrence)
	return new.join(li)

# Returns Rung end addresses
def llToRungs(ll,rows,delimiters,inputs):
	ll 		= ll[:-2]
	ends 	= []
	rungs 	= []
	end_l	= start_l	= ins_e	= ''
	cut_iter= 0
	input_addresses = []


	# To get the addresses of every end instruction
	for row in rows:
		temp = []
		if row[0] in ll and row[2] == 1:
			temp = [m.start() for m in re.finditer(row[0],ll)]
			for te in temp:
				ends.append((te,len(row[0])))

	ends = sorted(ends, key=lambda ends: ends[0])
	
	
	# The rungs with block instruction has a delimiter at the end
	for de in delimiters:
		if de[2] == 1: 	
			end_blk = [m.start() for m in re.finditer(de[0],ll)]
			end_l = de[0]	
			ins_e = de[1]
		if de[2] == 0:
			start_l = de[1]
	end_blk = end_blk[1::2]	
	
	
	# Getting the addresses of Input instructions
	for ip in inputs:
		if ip[0] in ll:
			temp = [m.start() for m in re.finditer(ip[0],ll)]
			for tem in temp:
				input_addresses.append(tem)
	
	cut = 0

	#Getting the rung end addresses from the control logic 
	for end, length in ends:
		if end+length in end_blk:
			cut = end + length + len(end_l)
		elif end+length in input_addresses:
			cut = end+length
		rung = rreplace(ll[:cut-cut_iter], end_l , "\n" +ins_e, 1)
		rungs.append(rung)
	
		ll = ll[cut-cut_iter:]
		cut_iter = cut
	rungs.append(ll)
	return rungs,start_l
		
'''=======
#	print end_blk
	for end, length in ends:
		if end+length in end_blk:
			cut = end + length + len(end_l)
		else:
			cut = end+length
#		print ll[:cut-cut_iter].count(end_l)-1
		rung = rreplace(ll[:cut-cut_iter], end_l , "\n" +ins_e, 1)
		rungs.append(rung)
		
#		print rungs
		ll = ll[cut-cut_iter:]
		cut_iter = cut
#		print ll
#		print cut
#		print cut_iter
#		print len(ll)
#	print rungs
	return rungs,start_l
		
#	print ends

>>>>>>> 3c17f8e8ee5173d8f8be86a9ff66f628f7f9441b'''
	

start = 0
flag = 0
ll = extractor_refined.ladder_logic
print ll
db = MySQLdb.connect(host="localhost",  # host 
                     user="root",       # username
                     passwd="12345",    # password
                     db="modicon")   	# name of the database

cur = db.cursor() 

code_list = ''

print "*****************************************"
cur.execute("select op_code,instruction,output from instructions ORDER BY CHAR_LENGTH(op_code) DESC")
rows = cur.fetchall()
cur.execute("select op_code,delimiter,category from delimiters")
delimiters = cur.fetchall()
cur.execute("select operation from operations")
operations = cur.fetchall()
cur.execute("select op_code,instruction,output from instructions where output=\'0\' ORDER BY CHAR_LENGTH(op_code) DESC")
inputs = cur.fetchall()
rungs,start_l = llToRungs(ll,rows,delimiters,inputs)

def memOperationRung(rung,op):
	global thisline
	global flag
	length = ''
	try:
		length = rung[rung.find(op)-2:rung.find(op)]
		if rung[rung.find(op)-6:rung.find(op)-4] == '03' or flag == 1:
			flag = 1
			offset = rung.find(op)+int(length,16)*2 - 4 
			thisline = thisline + rung[rung.find(op)-4:offset]
			
			if rung[offset:offset+2] == '03' or not rung.find('7f1a',offset):
				return thisline
			else:
				n_op =rung.find('7f1a',offset)
				return memOperationRung(rung[n_op-6:],rung[n_op:n_op+6])
		else:
			offset = rung.find(op)+int(length,16)*2 -4
			thisline = rung[rung.find(op)-4:offset]
			return thisline
	except:
#		continue
		pass
returnIns = ''

# Decompiling one rung at a item
for rung in rungs:
	global line
	global flag
	global thisline	 
	blk_t = 0
	if rung != '':	
		j = 0
		if_OP = 100000
		first_op = ''
		for op in operations:
			if op[0] in rung:
				op_pos = rung.find(op[0])
				if if_OP > op_pos:
					if_OP = op_pos
					first_op = op[0]
			st = memOperationRung(rung,first_op)
			flag = 0
			thisline = ''
			rep = memwords.parse(st)
			#print rep
			try:
				if rung[rung.find(first_op)-8:rung.find(first_op)-4] == '0303':
					rep = "OPER "+rep
					which = r'....'+st+'..'
				elif rung[rung.find(first_op)-8:rung.find(first_op)-4] == '03':
				 	rep = "AND "+rep
				 	which = r'..'+st+'..'
				else:
					which = r''+st
				rung = re.sub(which, rep + '\n', rung)
			except TypeError:
					continue
		
		for row in rows:				
			if row[0] in rung and row[2] ==1:	
				rung = rung.replace(row[0], row[1] )
			if row[0] in rung and row[2] == 0:
				rung = rung.replace(row[0],row[1]+"\n")

			if row[0] in rung and row[2] == 2:
				rung = re.sub(r''+row[0]+'..', row[1], rung)
			if row[0] in rung and row[2] == 3:
				rung = rung.replace(row[0], row[1])
		ins = rung.split("\n")
		returnIns = returnIns + "\n" + rung
		if start_l in ins[0]:
			ins[1] = "LD" + ins[1]
		else:
			ins[0] = "LD" + ins[0]
		for inst in ins: 
			print  "%04d  | " % j + inst 
			j = j+1
		print "---------------------------"	
		#print code_list

print "*****************************************"


