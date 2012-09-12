#!/usr/bin/python

import time

lastdate = None
test = 0

def parse(line, date):
	global lastdate
	global test
	if (not lastdate or date.tm_yday != lastdate.tm_yday):
		lastdate = date
		print date.tm_year, date.tm_mon, date.tm_mday, "BUYS:", test
		test = 0
	
	if(line.startswith("Gekauft:")):
		test += 1
	
	
	
	


f = open("fluid.log","r")

for line in f.readlines():
	date = time.strptime(line[:24])
	parse(line[27:],date)
