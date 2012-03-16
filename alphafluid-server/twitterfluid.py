
import time,threading
import twitter
import random

class twitterfluid(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.version = '0.0.1'
		self.api = twitter.Api()
		self.api = twitter.Api(
				consumer_key='jxZEgWDVdwvvq6QcvzB73w',
				consumer_secret='Wq03yUGV8v0ix5TIjYPEwYkxErNxBIEuTslPQbRE',
				access_token_key='518774696-2UtNmYWXkOp5FZjYvNpITNemUEf0m6K6Xi7TisxV',
				access_token_secret='oEulflrYiisN7zFoZV3vnWyLpMev82BDeH6n3vqKQpc')
		self.mentionid = 0
		self.lastmention = "forever alone"
		self.connection = None
		self.lastmentionchanged = 0

	def setConnection(self, conn):
		self.connection = conn
		
		self.start()
	
	def setDisconnected(self):
		self.connection = None
	
	def run(self):
		count = 0
		while (self.connection != None):
			time.sleep(1)
			count += 1
			if count>=30 and self.connection != None:
				count = 0
				print "checking mentions ",
				self.lastmentionchanged = 0
				ment = self.fetch_mention()
				print "current: " + ment
				if self.lastmentionchanged:
					print "sending mentions"
					self.connection.send("/i/t/"+ment+"\r\n")
			

	def map_shaft(self, shaft_number):
		self.shafts = ["Water", "TradeWinds", "Afri Cola", "Lift", "Club Mate", "Club Mate"]
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
			self.api.PostUpdate("Seems like someone just bought a Bottle of " + drink + "."  + meta)
		elif (rnd == 1):
			self.api.PostUpdate("Oh yeah! That's one nice " + drink + " you just pulled out of me."  + meta)
		elif (rnd == 2):
			self.api.PostUpdate("That guy just put his filthy coins into my slit and asked me for a " + drink + "."  + meta)
		elif (rnd == 3):
			self.api.PostUpdate("Seems like someone really craved for " + drink + "."  + meta)
		elif (rnd == 4):
			self.api.PostUpdate("Next time be more gently when pulling out your " + drink + ", please!"  + meta)
		elif (rnd == 5):
			self.api.PostUpdate("I noticed your really soft skin when you pressed my button for " + drink + "."  + meta)
		elif (rnd == 6):
			self.api.PostUpdate("Your awesome appeareance made some " + drink + " drop out of me!"  + meta)
		elif (rnd == 7):
			self.api.PostUpdate("Here's your change, there's your " + drink + "! Have a nice day."  + meta)
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
			self.api.PostUpdate("Hey @tensau! How about sticking some bottles of " + drink + " inside me?"  + meta)
		elif (rnd == 2):
			self.api.PostUpdate("I hereby invite @tensau to fill me up with whatever liquid he wants, as long as it looks like " + drink + "."  + meta)
		elif (rnd == 3):
			self.api.PostUpdate("I'm thirsty. So are my customers. @tensau should really fill me up with " + drink + "."  + meta)
		elif (rnd == 4):
			self.api.PostUpdate("I'm so horny, I could take at least ten bottles of " + drink + " up my shaft. And I want @tensau to do it!"  + meta)
		elif (rnd == 5):
			self.api.PostUpdate("Dear customers. Because @tensau is a lazy *******, I have no more " + drink + "!"  + meta)
		


