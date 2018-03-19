###################################
##Author:  Sushma Kalle    	 ##
##@Input:  Ladder Logic	   	 ##
##@Output: Instruction List   	 ##
###################################

import pyshark
import sys
import os,errno
import numpy as np
import extractor_refined
import re
import MySQLdb


def llToRungs(ll,rows,delimiters):
	ll = ll[:-2]
	offset = offset1 = blk = 0
	rungs = end_blk = start_blk = []
	end = ins_e = ''
	start = ins_s = ''
	ends = []
	for de in delimiters:
		if de[2] == 1: 	
			end_blk = [m.start() for m in re.finditer(de[0],ll)]
			end = de[0]	
			ins_e = de[1]
		if de[2] == 0:	
			start_blk = [m.start() for m in re.finditer(de[0],ll)]
			start = de[0]
			ins_s = de[1]
	end_blk = end_blk[1::2]	
	#ends = [m.start() for m in re.finditer(row[0],ll)]	
	for row in rows:
		if row[0] in ll and row[2] == 1:
		    ends = [m.start() for m in re.finditer(row[0],ll)]
		    for end in ends:
			end_of_rungs = end+len(row[0])+offset
			ll = ll[0:end_of_rungs] + "<>" + ll[end_of_rungs:]
			offset = offset + 2
		if row[0] in ll and row[2] == 4:
		    print row[0] + str(len(row[0]))
		    ends = [m.start() for m in re.finditer(row[0],ll)]			
		    for i in range(1, len(ends),2):			
			end_of_rungs = ends[i]+len(row[0])+offset1 + blk
			ll = ll[0:end_of_rungs-6] + "END_BLK<>" + ll[end_of_rungs:]
			ll = ll.replace(row[0], row[1])
			offset1 = offset1 + 3
			offset = offset + 3
			
		rungs = ll.split("<>")
	#print rungs
	return rungs
'''	
	for i in range(len(end_blk)):
		offset = end_blk[i]+len(end)
		rung = ll[start_blk[i]:offset]
		ll = ll[:start_blk[i]] + ll[offset:]
		rung = rung.replace(start,ins_s)
		rung = rung.replace(end,ins_e)
		rungs.append((start_blk[i],rung))
		#print rungs
	for row in rows:
		if row[0] in ll and row[2] == 1:
			ends.append([m.start() for m in re.finditer(row[0],ll)])
			for i in range(0, len(ends)):
				#print int(ends[i][0])
				ends[i][0] = int(ends[i][0]) + len(row[0])
	ends = sorted(ends)		
	for i in range(0, len(ends)):
		if i == 0:
			rungs.append((0,ll[0:ends[i][0]]))
			ll = ll[ends[i][0]:]
		else:
			rungs.append((ends[i-1][0],ll[ends[i-1][0]:ends[i][0]]))
			ll = ll[:ends[i-1][0]] + ll[ends[i][0]:]
		#print rungs
	print rungs
	print "====\n" + ll + 'its ll \n ===='	
	'''
	
	

start = 0
ll = extractor_refined.ladder_logic

db = MySQLdb.connect(host="localhost",  # host 
                     user="root",       # username
                     passwd="12345",    # password
                     db="modicon")   	# name of the database

cur = db.cursor() 

code_list = ''
#print ll
print "*****************************************"
cur.execute("select op_code,instruction,output from instructions")
rows = cur.fetchall()
cur.execute("select op_code,delimiter,category from delimiters")
delimiters = cur.fetchall()
#ll = "LD" + ll
rungs = llToRungs(ll,rows,delimiters)
rungs_count = len(rungs)
#print rungs
#for offset,rung in rungs:
	#print "'" + row[0] + "'"
for rung in rungs:
	if rung != '':	
		j = 0
		rung = "LD" + rung.strip()
		for row in rows:
			if row[0] in rung and row[2] == 0:
				rung = rung.replace(row[0],row[1]+"\n")
			if row[0] in rung and row[2] ==1:	
				rung = rung.replace(row[0], row[1] )
			if row[0] in rung and row[2] == 2:
				rung = re.sub(r''+row[0]+'..', row[1], rung)
			if row[0] in rung and row[2] == 3:
				rung = rung.replace(row[0], row[1])
		ins = rung.split("\n")
		for inst in ins:
			print  "%04d  | " % j + inst 
			j = j+1
		print "---------------------------"	
		
#print code_list

print "*****************************************"



