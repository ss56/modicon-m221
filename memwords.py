##################################
##Author:  Sushma Kalle    	 	##
##@Input:  Ladder Logic	   	 	##
##@Output: Instruction List   	##
##################################

import pyshark
import sys
import os,errno
import numpy as np
#import extractor_refined
import re
import MySQLdb

temp = "c490"
line = []
templ = ''

def convert(hexcode,htype):
	ret = ''
	if(htype == '14'):
		if hexcode != temp:
			number = hexcode[2:4] + hexcode[0:2]
			number = int(number,16)
			number = (number - 0x8100) / 2
			ret = "%MW" + str(number)
		else:
			ret = 'temp'
	else:
		number = hexcode[2:4] + hexcode[0:2]
		number = int(number,16)
		ret = str(number)
	return ret
def parseMemWords(s):
	#7F1A05141A028102810100
	three = 0
	length = s[2:4]
	operation = s[8:10]
	first_type = s[10:12]
	second_type = s[12:14]
	first = s[14:18]
	second = s[18:22]
	operation_options = {	'04' : '+',
							'05' : '-',
							'06' : '*',
							'07' : '/',
							'1e' : ':=',
							'25' : '<',
							'26' : '<=',
							'27' : '>',
							'28' : '>=',
							'29' : '<>',
							'2a' : '='
						}
						
	if int(length,16) > 11:
		third = s[22:26]
		lhs = convert(first, '14')
		first = convert(second, first_type)
		second = convert(third, second_type)
		
		result = '[ ' + lhs + ' := ' + first + "  " + operation_options[operation] + '  ' + second + ' ]'
	else:
		first = convert(first,first_type)
		second = convert(second,second_type)
		result =  '[ ' + first + "  " + operation_options[operation] + '  ' + second + ' ]'
	return result

def parseEqs(st):
	length = len(st)
	if length < 5:
		print 'error'
	elif length <= 26:
		res = parseMemWords(st)
		line.append(res)
	else:
		prev= ''
		fl_len = int(st[2:4],16) * 2
		linepart = st[0:fl_len]
		templ = parseMemWords(linepart)
		parseEqs(st[fl_len:])
		line.append(templ)
#230D7F1A061A1AC49002000400230B7F1A2A14140281C49003 #[ %MW1 = 2 * 4 ]
parseEqs("230d7f1a061a1ac49002000400230b7f1a2a14140281c49003") #[ %MW1 := %MW1 / %MW2 ]
#print line
try:
	for i in range(len(line)):
		if 'temp :=' in line[i+1]:
			lines = line[i].replace('temp', line[i+1][9:-2])
except IndexError as e2:
	pass
print lines