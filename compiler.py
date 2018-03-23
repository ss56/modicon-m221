##############################
##Author:  Sushma Kalle     ##
##@Input:  Instruction List ##
##@Output: binary			##
##############################

import struct
import mapper_refined
import re
import MySQLdb


IL = mapper_refined.returnIns
IL = IL.split('\n')
final = ''
def float_to_hex(f):
	return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def tuple_to_array(arr):
	splitspace = []
	for ar in arr:
		splitspace.append(ar[0])
	return splitspace

db = MySQLdb.connect(host="localhost",  # host 
                     user="root",       # username
                     passwd="12345",    # password
                     db="modicon")   	# name of the database

cur = db.cursor() 
cur.execute("select instruction from instructions where output=2")
thisone = cur.fetchall()
cur.execute("select instruction from instructions where output=3")
thistwo = cur.fetchall()
cur.execute("select op_code,delimiter,category from delimiters")
delimiters = cur.fetchall()
cur.execute("select operation from operations")
operations = cur.fetchall()

binary = ''
twospaces = tuple_to_array(thisone)
splitspace = tuple_to_array(thistwo)

print twospaces

print IL

def get_binary(ins):
	cur.execute("select op_code from instructions where instruction = '" + ins +"'")
	#print "select op_code from instructions where instruction = '" + ins +"'"
	ret = cur.fetchone()
	return ret
for ils in IL:
	try:
		if any(term+' ' in ils for term in twospaces):
			parts = ils.split(' ')
			instrution = get_binary(' '+parts[1])
			andor = get_binary(parts[0])[0] + str(format(((len(instrution[0])/2 )+2),'02x'))
			final = final+andor+instrution[0]
			
		elif any(term in ils for term in splitspace):
			parts = ils.split(' ')
			final = final + get_binary(parts[0])[0]
			final = final + get_binary(' '+parts[1])[0]
			
		else:
			final = final + get_binary(ils)[0]
	except TypeError as te:
		pass
	except IndexError as ie:
		pass
print final