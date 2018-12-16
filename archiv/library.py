#!/usr/bin/env python

from operator import itemgetter, attrgetter
from random import shuffle

class Library:
	def __init__(self):
		self.deck = []
	
	def loadLibrary(self):
		with open("library.txt") as f:
			d = 0 # counter for decks
			for line in f:
				if line.startswith('D!'):
					c = 0 #counter for cards
					d += 1
					line = line.replace('D!', "")
					end = line.find(':')			
					self.addDeck(line[:end])
#					line = line[end+1:]
#					self.deck[d-1].number = line[:end]
				else:
					c += 1
					self.deck[d-1].addCard()
					end = line.find(':')
					self.deck[d-1].card[c-1].question = line[:end]
					line = line[end+1:]
					end = line.find(':')
					self.deck[d-1].card[c-1].answer = line[:end]
					line = line[end+1:]
					end = line.find(':')
					self.deck[d-1].card[c-1].learnedStatus = int(line[:end])

	def saveLibrary(self):
		with open("library.txt", "w") as f:
			d=0 # counter for decks
			for x1 in self.deck:
				if x1.card:
					f.write("D!"+x1.name+"\n")
				else:
					f.write("D!"+x1.name+"\n")					
				for x2 in self.deck[d].card:
					f.write(x2.question+":"+x2.answer+":"+str(x2.learnedStatus)+"\n")
				d+=1
		f.close()
		print("saved")
	
	def giveName(self, name):
		self.name = name
	
	def addDeck(self, name):
		self.deck.append(Deck(name))
		print(str(len(self.deck)))
#		self.deck[-1].number = len(self.deck)-1

class Deck:
	def __init__ (self, name):
		self.name = name
		self.number = 0
		self.card = []
		self.status = "" #status can be "learned" or "no cards"
	
	def addCard(self):
		self.card.append(Card())
	
	def sortDeck(self):
		#sorts deck from not learned to learned
		if self.card:
			self.card.sort(key=attrgetter('learnedStatus'))

	def resetDeck(self):
		#sorts deck from not learned to learned
		for x in self.card:
			x.learnedStatus = 0
				
	def shuffleDeck(self):
		# Shuffles first few cards of the deck to prevent to much repetition
		# also checks if all cards have been learned or not
		if self.card:
			i=0
			lastStatus = self.card[i].learnedStatus
			while i < 5:
				i+=1
				try:
					if self.card[i].learnedStatus != lastStatus:
						break
				except:
					break
			x=self.card[0:i]				
			shuffle(x)
			self.card[0:i] = x
			if self.card[0].learnedStatus == 4:
				self.status = "Deck learned"
			else:
				self.status = ""

class Card:
	def __init__ (self):
		self.question = ""
		self.answer = ""
		self.learnedStatus = 0 
		# learned status has 5 states. 0--> not studied yet. 1-4 level of learning with 1 beeing
		# not knowing the card and 4 beeing knowing the card very well

if __name__=="__main__":
	myLibrary = Library()
	myLibrary.loadLibrary()
	myLibrary.deck[1].resetDeck()
	myLibrary.saveLibrary()
