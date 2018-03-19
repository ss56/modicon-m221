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
from operator import itemgetter


def rreplace(s, old, new, occurrence):
	li = s.rsplit(old, occurrence)
	return new.join(li)

def llToRungs(ll,rows,delimiters):
	ll 		= ll[:-2]
	ends 	= []
	rungs 	= []
	end_l	= ''
	start_l	= ''
	ins_e	= ''
	cut_iter= 0
#	print len(ll)
	for row in rows:
		temp = []
		if row[0] in ll and row[2] == 1:
			temp = [m.start() for m in re.finditer(row[0],ll)]
			for te in temp:
				ends.append((te,len(row[0])))

	ends = sorted(ends, key=lambda ends: ends[0])
#	print ends
	for de in delimiters:
		if de[2] == 1: 	
			end_blk = [m.start() for m in re.finditer(de[0],ll)]
			end_l = de[0]	
			ins_e = de[1]
		if de[2] == 0:
			start_l = de[1]
	end_blk = end_blk[1::2]	
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
rungs,start_l = llToRungs(ll,rows,delimiters)
print start_l
#rungs_count = len(rungs)
#print rungs
#for offset,rung in rungs:
	#print "'" + row[0] + "'"
for rung in rungs:
	blk_t = 0;
	if rung != '':	
		j = 0
		#rung = "LD" + rung.strip()
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


