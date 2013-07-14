#!/usr/bin/python

import time, datetime
import matplotlib.pyplot as plt


lastdate = None
test = []
for i in range(6):
	test.append(0)

times = []
nums = []

colors = ['ro', 'go', 'bo', 'co', 'mo', 'y']

def parse(line, date):
	global lastdate
	global test
	if (not lastdate or date.tm_yday != lastdate.tm_yday):
		lastdate = date
		if (1):
			print date.tm_year, date.tm_mon, date.tm_mday, "BUYS:", test
			times.append(datetime.datetime( date.tm_year, date.tm_mon, date.tm_mday))
			nums.append(test[:])
		for i in range(6):
			test[i] = 0
	
	if(line.startswith("Gekauft:")):
		numstr = line.split(":")[1][1:]
		numstr = numstr.split(" ")[0]
		print numstr
		num = int(numstr)
		if(num == 5):
			num = 4
		test[num] += 1
	
	
	
	


f = open("fluid.log","r")

for line in f.readlines():
	date = time.strptime(line[:24])
	parse(line[27:],date)

print len(nums), len(times)
for i in range(6):
	plt.plot_date(times, map(lambda x: x[i], nums), colors[i], label="Schacht " + str(i+1))
plt.legend()
plt.show()

