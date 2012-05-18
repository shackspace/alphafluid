import time


def log(msg):
	f = open("fluid.log","a")
	f.write(time.asctime(time.localtime(time.time()+3600*1)))
	f.write(" ] " + msg + "\n")
	f.close()
	print msg


