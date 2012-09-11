
import time,threading
import twitter
import random
import conf
import sys
from tools import *

class twitterfluid(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.version = '0.0.1'
		self.api = twitter.Api()
		self.api = twitter.Api(
				consumer_key=conf.read('key.cfg','twitter_consumer_key'),
				consumer_secret=conf.read('key.cfg','twitter_consumer_secret'),
				access_token_key=conf.read('key.cfg','twitter_access_token_key'),
				access_token_secret=conf.read('key.cfg','twitter_access_token_secret'))
		self.mentionid = 0
		self.lastmention = "forever alone"
		self.connection = None
		self.lastmentionchanged = 0
		self.running = True

	def stop(self):
		self.running = False

	def setConnection(self, conn):
		self.connection = conn
		
		#self.start()
	
	def setDisconnected(self):
		self.connection = None
	
	def run(self):
		count = 0
		while (self.running):
			time.sleep(1)
			count += 1
			if count>=60 and self.connection != None and self.running:
				count = 0
				print "checking mentions ",
				self.lastmentionchanged = 0
				ment = self.fetch_mention()
				print "current: " + ment
				if self.lastmentionchanged:
					print "sending mention: " + ment
				try:
					self.connection.send("/i/t/"+ment.encode('ascii','ignore')+"\r\n")
				except:
					log(str(sys.exc_info()[0]))
					log(str(sys.exc_info()[1]))
					#log(sys.exc_info()[2])
					log("sending mention to matomat failed!")

			

	def map_shaft(self, shaft_number):
		self.shafts = ["Water", "Mountain Dew", "Afri Cola", "Lift", "Club Mate", "Club Mate"]
		return self.shafts[shaft_number]
	
	def fetch_mention(self):
		
		if (self.lastmentionchanged):
			return self.lastmention
		ments = self.api.GetMentions(since_id = self.mentionid)
		if len(ments)>0:
			ment = ments[0]
			self.mentionid = ment.GetId()
			self.lastmention = ment.GetUser().GetScreenName()+ " - " +ment.GetText()
			if len(self.lastmention) > 159:
				self.lastmention = self.lastmention[0:158]
			self.lastmentionchanged = 1
		return self.lastmention
		
	
	def tweet_bought(self, shaft_number, count):
		meta = " (S " + str(shaft_number+1) + ", R " + str(count) + ", Time: " + str(time.time()) + ")"
		drink = self.map_shaft(shaft_number)
		rnd = random.randint(0,11) 
		
		if (rnd == 0):
			self.api.PostUpdate("Seems like someone just bought a bottle of " + drink + "."  + meta)
		elif (rnd == 1):
			self.api.PostUpdate("Oh yeah! That's one nice " + drink + " you just pulled out of me."  + meta)
		elif (rnd == 2):
			self.api.PostUpdate("Someone just put his filthy coins into my money slot and asked me for a " + drink + "."  + meta)
		elif (rnd == 3):
			self.api.PostUpdate("Seems like someone really craved a " + drink + "."  + meta)
		elif (rnd == 4):
			self.api.PostUpdate("Next time be more gentle pulling out your " + drink + ", please!"  + meta)
		elif (rnd == 5):
			self.api.PostUpdate("I noticed your really soft skin when you pressed my " + drink + " button."  + meta)
		elif (rnd == 6):
			self.api.PostUpdate("Your awesome appeareance made some " + drink + " drop out of me!"  + meta)
		elif (rnd == 7):
			self.api.PostUpdate("Here's your change, here's your " + drink + "! Have a nice day."  + meta)
		elif (rnd == 8):
			self.api.PostUpdate("Please stop touching my buttons! You made a bottle of " + drink + " come out of my slot!"  + meta)
		elif (rnd == 9):
			self.api.PostUpdate("Really just a " + drink + "? :( No hugs? No kisses?"  + meta)
		elif (rnd == 10):
			self.api.PostUpdate("Thanks for touching me there! It's been a while since someone touched my " + drink + " spot."  + meta)
		elif (rnd == 11):
			self.api.PostUpdate("I made that bottle of " + drink + " you just bought at least 20% cooler!"  + meta)



	def tweet_empty(self, shaft_number):
		meta = " (S " + str(shaft_number+1) + ", Time: " + str(time.time()) + ")"
		drink = self.map_shaft(shaft_number)
		rnd = random.randint(0,10) 
		if (rnd == 0):
			self.api.PostUpdate("Oh noes! I ran out of " + drink + "! Help me @tensau!"  + meta)
		elif (rnd == 1):
			self.api.PostUpdate("Hey @tensau! How about filling me up with some " + drink + " bottles?"  + meta)
		elif (rnd == 2):
			self.api.PostUpdate("I hereby invite @tensau to fill me up with whatever liquid he wants, as long as it looks like " + drink + "."  + meta)
		elif (rnd == 3):
			self.api.PostUpdate("I'm thirsty. So are my customers. @tensau should really refill " + drink + "."  + meta)
		elif (rnd == 4):
			self.api.PostUpdate("I'm so horny, I could take at least ten bottles of " + drink + " up my shaft. And I want @tensau to do it!"  + meta)
		elif (rnd == 5):
			self.api.PostUpdate("Dear customers. Because @tensau is a lazy *******, I have no more " + drink + "!"  + meta)
		


