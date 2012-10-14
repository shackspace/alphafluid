#!/usr/bin/python
#-*- coding: utf-8 -*-

import signal
import socket
import sys
import time
import urllib2
import subprocess
import random
import twitterfluid
import conf
import traceback
from tools import *

#soundlist = ["dank.wav", "zelda.wav", "suit.wav", "hlbroken.wav"]
#ambientlist = ["alien_blipper.wav", "computalk1.wav", "noise2.mp3", "computalk2.wav", "steamburst1.wav"]

nextambient = time.time() + 10
nextcheckplaying = time.time() + 2

tw = twitterfluid.twitterfluid()
running = True
connected = False

apikey = conf.read('key.cfg','lick_api_key')


mapping = (1,2,3,4,26,27)

def handler(signum, frame):
	tw.setDisconnected()
	tw.stop()
	running = False
	print "Trying to stop!"

signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

def get_sounds(value):
	return conf.read("sound.cfg",value).split(",")

def mat_checkplaying():
	check = subprocess.Popen(["./isplaying"], stdout=subprocess.PIPE, shell=True)
	check.wait()
	res = check.stdout.readline()
	if res.startswith("[playing]"):
		return
	
	subprocess.Popen(["./set_volume 10"], stdout=subprocess.PIPE, shell=True)
	
	subprocess.Popen(["./playstream"], stdout=subprocess.PIPE, shell=True)

def mat_play(file, volume):
	check = subprocess.Popen(["./isplaying"], stdout=subprocess.PIPE, shell=True)
	check.wait()
	res = check.stdout.readline()
	if res.startswith("[playing]"):
		print "skipping sound, something's already playing"
		return
	
	
	subprocess.Popen(["./set_volume "+str(volume)], stdout=subprocess.PIPE, shell=True)
	subprocess.Popen(["./play_remote "+file], stdout=subprocess.PIPE, shell=True)


def mat_checkambient():
	global nextambient
	global nextcheckplaying
	if (time.time() > nextcheckplaying):
		nextcheckplaying = time.time() + 2
		if (mat_checkplaying()):
			return
	if (time.time() > nextambient):
		rnd = random.randint(5*60,15*60)
		nextambient = time.time() + rnd 
		sound = random.choice(get_sounds("randomsounds"))
		mat_play(sound, 3)
		print "played ambient sound: " + sound + ", next after: " + str(rnd)

def send_bought(st):
	try:
		urllib2.urlopen("https://appserv.tutschonwieder.net:8443/apex/prod/sellProduct?apikey="+apikey+"&automat_id=1&schacht_id=" + str(mapping[int(st)]) + "&anzahl=1")
	except:
		log("!!!!!!!!!!!!!!!!!!!!!! LICK DOWN !!!!!!!!!!!!!!!!!!!!!")

def send_empty(st):
	try:
		urllib2.urlopen("https://appserv.tutschonwieder.net:8443/apex/prod/schachtLeer?apikey="+apikey+"&automat_id=1&schacht_id=" + str(mapping[int(st)]))
	except:
		log("!!!!!!!!!!!!!!!!!!!!!! LICK DOWN !!!!!!!!!!!!!!!!!!!!!")

def lick_get_level(shaft):
	try:
		lines = urllib2.urlopen("https://appserv.tutschonwieder.net:8443/apex/prod/getFuellstand?automat_id=1&schacht_id="+str(shaft)).readlines()
		for line in lines:
			print line
			#if line.startswith('{"\"tensai-prod\".lick_api.getfuellstand(/*in:automat_id*/:1,/*in:schacht_id*/:2)":'):
			if line.find("tensai-prod") >= 0 and line.find(".lick_api.getfuellstand(") >= 0 and line.find("in:automat_id"):
				rpart = line.split(":")[-1]
				#print rpart
				if(rpart[-1] == "}"):
					numonly = rpart[0:-1]
					print numonly
					num = int(numonly)
					if num < 0:
						num = 0
					return num
	except:
		log("!!!!!!!!!!!!!!!!!!!!!! LICK DOWN !!!!!!!!!!!!!!!!!!!!!")


def mat_send_values(conn):
	log("sending values")
	
	try:
		for i in range(0,6):
			time.sleep(0.2)
			conn.send("/i/s/"+str(i)+" "+str(lick_get_level(mapping[i]))+"\r\n")
	except:
		log(str(sys.exc_info()[0]))
		log(str(sys.exc_info()[1]))
		#log(sys.exc_info()[2])
		log("sending values to matomat failed!")
		log("FORCE DISCONNECT " + client_address[0])
		connected = False


def mat_send_mention(conn):
	log("sending mentions")
	txt = tw.fetch_mention()
	try:
		conn.send("/i/t/"+txt.encode('ascii','ignore')+"\r\n")
	except:
		log(str(sys.exc_info()[0]))
		log(str(sys.exc_info()[1]))
		#log(sys.exc_info()[2])
		log("sending mention to matomat failed!")
		log("FORCE DISCONNECT " + client_address[0])
		connected = False

def parse(line, conn):
	if not line.startswith("/o/"):
		line = ""
		return
	if line[3] == 'b':		#buy
		send_bought(line[5])
		log("Gekauft: " + line[5])
		mat_play(random.choice(get_sounds("buysounds")), 10)
		tw.tweet_bought(int(line[5]), "")
		mat_send_values(conn)
	elif line[3] == 'o': 	#offline buys (no connection)
		send_bought(line[5])
		log("Offline log: " + line[5])

	elif line[3] == 'e':	#empty
		send_empty(line[5])
		log("Leer: " + line[5])
		tw.tweet_empty(int(line[5]))

	elif line[3] == 'i':	#login
		conn.send("/i/w/\r\n")
		log("welcomed client")
		mat_send_values(conn)
		mat_send_mention(conn)
	elif line[3] == 'd':	#door
		if(line[5] == '0'):
			log("Door Closed")
			mat_play(random.choice(get_sounds("closesounds")), 5)
		else:
			log("Door Opened")
			mat_play(random.choice(get_sounds("opensounds")), 5)


	line = ""
	return



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('', 1337)
sock.bind(server_address)
print 'starting up on %s port %s' % sock.getsockname()
sock.listen(1)
tw.start()
while running:
	print 'waiting for a connection'
	log('waiting for a connection')
	connection, client_address = sock.accept()
	line = ""
	print 'client connected:', client_address
	log("CONNECT " + client_address[0])
	tw.setConnection(connection)
	connected = True;
	while (running and connected):
		data = connection.recv(1)
		mat_checkambient()
		if data:
			line += data[0]
			
			if data[0] == '\n' or data[0] == '\r':
				if line[0] != 'd' and line[0] != '\n' and line[0] != '\r':
					print line
				parse(line,connection)
				line = ""
		else:
			connected = False
			break
	tw.setDisconnected()
	print 'client disconnected:', client_address
	log("DISCONNECT " + client_address[0])
	connection.close()
sock.close()

